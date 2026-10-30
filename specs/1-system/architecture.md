# Architecture

Level: L1 System · Status: Review

## Big picture

```
┌──────────────────────┐        ┌──────────────────────┐
│ Web app (React SPA)  │        │ Mobile app (Expo)    │
│  packages/core       │        │  packages/core       │
│  Web Speech API      │        │  expo-speech         │
└─────────┬────────────┘        └──────────┬───────────┘
          │  Firebase JS SDK (Auth, Firestore, Storage, Functions, App Check, Remote Config)
          ▼                                ▼
┌───────────────────────────────────────────────────────────────────────┐
│ Firebase (northamerica-northeast1)                                    │
│                                                                       │
│  Auth ── users, providers, anonymous guests                           │
│                                                                       │
│  Firestore ── users/{uid}/…  library/…  (rules enforce ownership)     │
│                                                                       │
│  Storage ── uploads/{uid}/{bookId}/original.*                         │
│                 │ object finalized                                    │
│                 ▼                                                     │
│  Functions ── ingestBook (Storage trigger) → passages into Firestore   │
│            ── lesson / followUp (streaming callables) ──► Claude API  │
│            ── nextPassage (callable)                                  │
│            ── finishTest (callable: verify + save result + stats)     │
│            ── deleteAccount, deleteBook (callables)                   │
│            ── onUserCreate (Auth trigger: profile + defaults)         │
│                                                                       │
│  Remote Config ── model, quotas, flags                                │
│  App Check ── protects Functions, Firestore, Storage                  │
└───────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                         Anthropic Claude API
```

## What runs where

| Concern | Client | Server |
|---|---|---|
| Typing engine, live marks, live stats | ✓ (core) | |
| Final result numbers | ✓ shows them at once | ✓ `finishTest` recomputes from the keystroke log with the same core code and stores the trusted copy |
| Picking the next passage | | ✓ `nextPassage` (random, by source, avoids recent repeats) |
| Prefetching the next passage | ✓ asks for it at test start | |
| Lessons and follow-ups | shows the stream | ✓ builds the prompt, calls Claude, saves the result, counts quota |
| Book parsing | | ✓ `ingestBook` |
| Read aloud | ✓ device voices | P2: cloud voices |
| Settings | ✓ writes directly (rules check shape) | |
| Stats totals | | ✓ updated in `finishTest` (a transaction) |

**Why the server recomputes results:** client numbers are instant but can be faked. Stats, personal bests, and later leaderboards use only server-checked numbers. Because the same `packages/core` runs on both sides, the numbers match.

## Key sequences

### Start a test

```
Client                          nextPassage            Firestore
  │ app open / restart              │                      │
  │──── call {source, size} ───────►│                      │
  │                                 │── random query ─────►│ library/{book}/passages or users/{uid}/books/{book}/passages
  │                                 │◄─────────────────────│
  │◄─── {passageId, text, book} ────│                      │
  │ render, start typing; meanwhile prefetch the next passage
```

Random pick: each passage doc has `rand` (0–1). Query `rand >= r` ordered by `rand`, limit 1; wrap to `rand < r` if empty. A small per-user "recent" list (last 50 passage IDs) avoids repeats.

Guests call `nextPassage` with an anonymous Firebase account (signed in silently), so App Check and quotas still apply.

### Finish a test and get a lesson

```
Client                     finishTest           lesson (stream)            Claude
  │ test ends                  │                      │                       │
  │── {passageId, log, cfg} ──►│ recompute result     │                       │
  │                            │ write session + stats│                       │
  │◄── {sessionId, result} ────│                      │                       │
  │── lesson {sessionId} ──────────────────────────► │ check quota           │
  │                                                   │── messages.stream ──►│
  │◄──────── chunks ───────────────────────────────── │◄──── text deltas ────│
  │                                                   │ save lesson to session│
  │◄──────── done {quotaLeft} ─────────────────────── │                       │
```

The lesson keeps generating and saving even if the client disconnects. A client that reconnects reads the saved session; if the lesson is still `generating`, it listens to the session doc until it becomes `ready`.

### Upload a book

```
Client ── upload to uploads/{uid}/{bookId}/original.epub (Storage, resumable)
       ── creates users/{uid}/books/{bookId} {status: "uploading"} first
Storage finalize ──► ingestBook
       status "processing" → parse → cut passages (core) → language check
       → batch write passages → status "ready" (or "failed" + reason)
Client listens to the book doc and shows each step.
```

## Offline and sync

- Firestore offline persistence on (web: IndexedDB; mobile: memory cache + AsyncStorage for settings).
- Tests work offline with the prefetched passage plus a small offline buffer (10 passages, P1). Results queue in a local outbox and call `finishTest` when back online.
- Lessons need the network; the UI says so.

## Analytics

P1. Events (Google Analytics for Firebase), no passage text or personal content:

| Event | Params |
|---|---|
| `test_start` | mode, length, accent_rule, source_type |
| `test_finish` | mode, length, wpm_bucket, acc_bucket, slips |
| `lesson_view` | level, streamed_ms |
| `lesson_feedback` | up/down |
| `follow_up_ask` | count_in_session |
| `listen` | slow, voice_quality |
| `book_upload` | format, size_bucket, result |
| `sign_up` | provider, from_guest |

## Observability

- Sentry in web, mobile, and functions with release tags and source maps.
- Functions log structured JSON: `uid` hash, function, duration, Claude input/output tokens, cost estimate.
- Budget alerts on the Google Cloud project and a monthly spend limit on the Anthropic account.

## Scaling notes

- Firestore reads per test: about 2 (passage + session write). Stats use one aggregate doc per user.
- Lessons: one function instance handles many concurrent streams (concurrency 40). Max instances capped to protect cost.
- Book ingest: memory 1 GiB, timeout 540 s, max file 25 MB. Larger books fail cleanly.
