# API: Cloud Functions

Level: L1 System · Status: Review
Payload and response shapes live in `packages/schema/src/api.ts`. Every callable checks App Check, validates input with zod, and returns `HttpsError` codes from the table at the end.

## Callables

### `nextPassage`

Pick a passage for the next test.

| | |
|---|---|
| Auth | Signed in (anonymous allowed) |
| Input | `{ source: {type: "all"\|"book"\|"mine", bookId?}, size: "short"\|"medium"\|"long", count?: 1–10 }` |
| Output | `{ passages: {id, bookId, source, bookTitle, author, text}[] }` |
| Rules | Random by `rand`; skips the last 50 IDs in `private/recent`; `mine` needs a `ready` book; `count > 1` fills the offline buffer (P1) |
| Errors | `not-found` (book missing or not ready), `failed-precondition` (no passages of that size) |

### `finishTest`

Verify a finished test and save it.

| | |
|---|---|
| Auth | Signed in (anonymous allowed; guest sessions move with the account on link) |
| Input | `{ testId, passageRefs: [{passageId, bookId, source}], config, log, clientResult, tz }` (time mode can span several passages) |
| Output | `{ sessionId, result, personalBest?: boolean }` |
| Rules | Loads the passage text, replays `log` through `packages/core`, compares with `clientResult` (logs mismatches), writes the session with the server result, updates `private/stats` in a transaction |
| Saves only if | at least 5 words typed and the log is valid |
| Errors | `invalid-argument` (bad log), `not-found` (passage) |

### `lesson` (streaming)

Generate the lesson for a session.

| | |
|---|---|
| Auth | Signed in, not anonymous |
| Input | `{ sessionId, tz }` |
| Stream | text chunks |
| Final | `{ status: "ready", quota: {lessonsLeft, resetsAt} }` |
| Rules | If `lesson.status` is `ready`, returns the saved text at once. If `generating` and started under 90 s ago, the client listens to the session doc instead. Checks and counts quota only when a new generation starts. Saves the text as `messages[0]` |
| Errors | `resource-exhausted` (quota), `unavailable` (Claude down; retry), `permission-denied` |

### `followUp` (streaming)

Answer a question in a session.

| | |
|---|---|
| Auth | Signed in, not anonymous |
| Input | `{ sessionId, question (1–1000 chars), tz }` |
| Stream | text chunks |
| Final | `{ quota: {followUpsLeft, resetsAt} }` |
| Rules | Appends the question and the answer to `messages` only after the answer finishes (a failed answer leaves no half turn). Max 60 messages |
| Errors | `resource-exhausted`, `failed-precondition` (no lesson yet, or session full), `unavailable` |

### `wordMeaning` (P1)

| | |
|---|---|
| Input | `{ passageId, bookId, source, wordIndex }` |
| Output | `{ word, lemma, meaning, pos, gender?, note? }` |
| Rules | Cached per `(passageId, wordIndex)` in `wordCache/`; uses `claude-haiku-5-5` (cheap, short) if the owner approves in `decisions.md` |

### `deleteBook`

| | |
|---|---|
| Input | `{ bookId }` |
| Rules | Deletes passages in batches, the Storage file, then the book doc. Sessions keep their copied passage text |

### `deleteAccount`

| | |
|---|---|
| Input | `{}` (requires a recent sign-in: `auth_time` within 5 minutes) |
| Rules | Deletes Storage `uploads/{uid}/`, every doc under `users/{uid}` and `usage/{uid}` (recursive delete), then the Auth user |

### `exportData` (P1)

Writes a JSON file to `exports/{uid}/` and returns a 24-hour signed link.

## Triggers

| Function | Trigger | Job |
|---|---|---|
| `ingestBook` | Storage `onObjectFinalized` for `uploads/**` | Parse, cut passages, check language, write passages, set status. See `functions/src/books/SPEC.md` |
| `sweepStaleUploads` | Scheduled daily, 03:00 America/Toronto | Cleans up uploads stuck in `uploading` or `processing`. See `functions/src/books/SPEC.md` |
| `onAccountLinked` | Called by the client right after anonymous → full account linking | Nothing to move: the uid stays the same when linking. Marks `users/{uid}.onboarded = false` so onboarding runs |

## Streaming transport

**Primary:** streaming callables (`httpsCallable(fn).stream(data)` on the client; `response.sendChunk(text)` in the function).

**Fallback** (only if the primary fails on React Native at M0): `POST /api/lesson` and `/api/followUp` as HTTPS functions returning `text/event-stream`. Headers: `Authorization: Bearer <ID token>`, `X-Firebase-AppCheck: <token>`. Events: `chunk`, `done`, `error`. Same rules as above.

## Error codes

| Code | When | Client shows |
|---|---|---|
| `unauthenticated` | No or bad sign-in | Sign-in prompt |
| `permission-denied` | Not the owner, or anonymous on a lesson | Sign-up prompt or "not found" |
| `invalid-argument` | Schema check failed | "Something went wrong" + report |
| `not-found` | Book, passage, or session missing | Friendly not-found |
| `failed-precondition` | Book not ready, session full | Specific message |
| `resource-exhausted` | Quota reached | Quota message with reset time |
| `unavailable` | Claude or Firebase busy | "Try again" with Retry |
| `internal` | Bug | "Something went wrong" + Sentry event |
