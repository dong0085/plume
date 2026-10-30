# Data model

Level: L1 System · Status: Review
Shapes are defined once in `packages/schema` (zod) and used by every app and function.

## Firestore tree

```
library/{bookId}                                   public read · server write
library/{bookId}/passages/{passageId}              public read · server write

users/{uid}                                        owner read/write (whitelisted fields)
users/{uid}/books/{bookId}                         owner read · owner create (status "uploading") · owner edit title/author · server write
users/{uid}/books/{bookId}/passages/{passageId}    owner read · server write
users/{uid}/sessions/{sessionId}                   owner read · owner edits lesson.feedback only · server write
users/{uid}/words/{wordId}                         owner read/write (P1)
users/{uid}/private/stats                          owner read · server write
users/{uid}/private/recent                         server only
usage/{uid}/days/{yyyy-mm-dd}                      owner read · server write
```

## Documents

### `library/{bookId}` and `users/{uid}/books/{bookId}`

| Field | Type | Notes |
|---|---|---|
| `title` | string | |
| `author` | string | |
| `year` | number? | Library only |
| `blurb` | string? | Library only; 1–2 sentences |
| `lang` | `"fr"` | Language code; French only at launch |
| `langScore` | number | 0–1, how French the text looks |
| `coverTint` | string | Token name for the generated cover |
| `passageCounts` | `{short, medium, long}` | numbers |
| `status` | `"uploading" \| "processing" \| "ready" \| "failed"` | Library books are always `ready` |
| `statusStep` | `"reading" \| "cutting" \| "checking"`? | For the progress UI |
| `failReason` | `"drm" \| "too_large" \| "unsupported" \| "no_text" \| "not_french" \| "parse_error"`? | |
| `format` | `"epub" \| "txt" \| "pdf"` | Uploads |
| `sizeBytes` | number | Uploads |
| `sha256` | string | Uploads; duplicate check |
| `storagePath` | string | Uploads |
| `source` | `{type: "gutenberg", id: number}`? | Library only |
| `chapters` | `{title, firstOrder}[]`? | P1 |
| `createdAt`, `updatedAt` | timestamp | |

### `…/passages/{passageId}`

| Field | Type | Notes |
|---|---|---|
| `text` | string | Cleaned passage (see `packages/core/src/text/SPEC.md`) |
| `size` | `"short" \| "medium" \| "long"` | One passage per size bucket |
| `chars` | number | |
| `order` | number | Position in the book; used by "type in order" (P1) |
| `chapter` | number? | P1 |
| `rand` | number | 0–1, for random picks |
| `cefr` | `"A1"…"C2"`? | P2 |

Passage IDs are deterministic: `{size}-{order}` so re-ingesting a book is idempotent.

### `users/{uid}`

| Field | Type | Who writes |
|---|---|---|
| `displayName` | string | owner |
| `level` | `"A1"…"C2"` | owner |
| `onboarded` | boolean | owner |
| `settings` | object (below) | owner |
| `createdAt` | timestamp | owner on create |
| `plan` | `"free"` | server only (rules block client changes) |

`settings`:

```ts
{
  typing: { mode: "passage" | "time" | "words", time: 15|30|60|120, words: 10|25|50|100,
            length: "short"|"medium"|"long", accentRule: "strict"|"lenient",
            punctuationRule: "strict"|"ignore", stopOnError: "off"|"letter"|"word",
            confidence: boolean, liveStats: { wpm: boolean, acc: boolean, timer: boolean },
            caret: "line"|"block"|"underline"|"off", smoothCaret: boolean,
            focusMode: boolean, sounds: "off"|string },
  appearance: { theme: "system"|string, font: "serif"|"sans"|"mono", textSize: number },
  listening: { voiceURI: string | null, rate: number },   // per device; see below
  source: { type: "all" | "book" | "mine", bookId?: string },
  lessons: { moreFrench: boolean }
}
```

`listening.voiceURI` depends on the device. It is stored per device in local storage and mirrored here only as a preference hint (`preferredVoiceName`).

### `users/{uid}/sessions/{sessionId}`

| Field | Type | Notes |
|---|---|---|
| `createdAt` | timestamp | |
| `passage` | `{id, bookId, source: "library"\|"mine", bookTitle, author, text}` | Text copied so the session survives book deletion |
| `config` | typing config used | Snapshot of the relevant settings |
| `result` | `Result` (below) | Server-computed |
| `log` | string | Packed keystroke log (see `packages/core/src/engine/SPEC.md`) |
| `lesson` | `{status: "none"\|"generating"\|"ready"\|"failed", model, level, startedAt, finishedAt, feedback?: {vote: 1\|-1, note?}}` | |
| `messages` | `{role: "user"\|"assistant", content, at}[]` | Lesson prompt is not stored; `messages[0]` is the lesson. Max 60 entries |
| `questionCount` | number | For the history list |
| `deviceType` | `"web" \| "ios" \| "android"` | |

`Result`:

```ts
{ wpm: number, raw: number, acc: number, consistency: number, durationMs: number,
  chars: { correct, incorrect, extra, missed, slips },
  words: { status: "ok"|"slip"|"wrong"|"missed"|"extra", expected?: string, typed?: string }[],
  samples: { wpm: number[], raw: number[], errors: number[] }   // one entry per second
}
```

### `users/{uid}/private/stats`

```ts
{ tests: number, timeMs: number, chars: number, wpmSum: number, accSum: number,
  best: { [modeKey: string]: { wpm, acc, sessionId, at } },   // modeKey e.g. "passage-medium-strict", "time-60-lenient"
  accents: { [letter: string]: { seen: number, missed: number } },   // é è ê à ç ù î ô û ë ï œ
  streak: { current: number, longest: number, lastDay: "yyyy-mm-dd" },
  days: { [yyyyMMdd: string]: { tests: number, timeMs: number } }   // last 365 days, for the calendar
}
```

### `usage/{uid}/days/{yyyy-mm-dd}`

`{ lessons: number, followUps: number, inputTokens: number, outputTokens: number, costMicros: number }`. Days use the person's time zone sent with each call, capped to ±14 h of UTC.

### `users/{uid}/words/{wordId}` (P1)

`{ fr, en, note?, pos?, gender?, example?, sessionId, createdAt, review?: {due, interval, ease} }`

## Cloud Storage

```
uploads/{uid}/{bookId}/original.{epub|txt|pdf}   owner write once (≤ 25 MB, allowed types) · owner read · server delete
exports/{uid}/{exportId}.json                    server write · owner read (P1, signed link, 24 h)
tts/{passageHash}.mp3                            server write · signed-in read (P2 cloud voices)
```

## Indexes

| Collection | Fields | For |
|---|---|---|
| `passages` (collection group off) | `size` asc, `rand` asc | Random pick per size |
| `passages` | `size` asc, `order` asc | Type in order (P1) |
| `sessions` | `createdAt` desc | History |
| `sessions` | `passage.bookId` asc, `createdAt` desc | History filter by book |
| `books` | `createdAt` desc | My books |

## Limits

| Limit | Value | Where enforced |
|---|---|---|
| Upload size | 25 MB | Storage rules + `ingestBook` |
| Uploaded books per account | 20 (see `decisions.md`) | `ingestBook` + rules count check via a counter on `users/{uid}` |
| Passages per book | 20,000 | `ingestBook` |
| Messages per session | 60 | `followUp` |
| Follow-up length | 1,000 characters | `followUp` + schema |
| Keystroke log | 200 KB | `finishTest` |
