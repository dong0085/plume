# functions

Level: L2 Folder · Status: Review
Parent specs: `specs/1-system/architecture.md`, `api.md`, `ai-lessons.md`, `security.md`

## Purpose

All server code: picking passages, verifying and saving results, lessons and follow-ups with Claude, book ingestion, and account/book deletion. Cloud Functions for Firebase (2nd gen), Node.js 22, region `northamerica-northeast1`.

## Layout

```
src/
├── index.ts               exports every function (names match api.md)
├── tests/                 nextPassage, finishTest            ← L3 SPEC.md
├── lessons/               lesson, followUp, wordMeaning (P1) ← L3 SPEC.md
├── books/                 ingestBook, deleteBook, sweep      ← L3 SPEC.md
├── account/               deleteAccount, exportData (P1)     ← L3 SPEC.md
├── lib/
│   ├── admin.ts           firebase-admin init (one instance)
│   ├── callable.ts        wrapper: App Check, auth checks, zod input, error mapping, logging
│   ├── config.ts          Remote Config server template reads (model, quotas, flags) with 60 s cache
│   ├── quota.ts           daily usage transaction: reserve, commit, refund
│   ├── claude.ts          Anthropic client (secret), stream helper, cost math
│   └── log.ts             structured logger (hashes uid; never logs content)
test/                      Vitest + emulators; fixtures/ for books
evals/                     lesson eval set and rubric runner
```

## Function settings

| Function | Type | Memory | Timeout | Concurrency | Max instances | Secrets |
|---|---|---|---|---|---|---|
| `nextPassage` | callable | 256 MiB | 10 s | 80 | 20 | — |
| `finishTest` | callable | 256 MiB | 15 s | 80 | 20 | — |
| `lesson` | streaming callable | 512 MiB | 120 s | 40 | 10 | `ANTHROPIC_API_KEY` |
| `followUp` | streaming callable | 512 MiB | 90 s | 40 | 10 | `ANTHROPIC_API_KEY` |
| `ingestBook` | Storage finalize | 1 GiB | 540 s | 1 | 5 | — |
| `deleteBook` | callable | 256 MiB | 120 s | 10 | 5 | — |
| `deleteAccount` | callable | 512 MiB | 300 s | 5 | 3 | — |
| `sweepStaleUploads` | scheduled, daily 03:00 America/Toronto | 256 MiB | 300 s | 1 | 1 | — |

`enforceAppCheck: true` on every callable from M5 (monitor-only before).

## Shared rules

- Every callable goes through `lib/callable.ts`: verify auth (and non-anonymous where `api.md` says), parse input with the zod schema from `packages/schema`, run, map known errors to `HttpsError` codes, log duration and outcome.
- Writes that must agree (session + stats; quota reserve) use transactions.
- Reads `packages/core` for all text and scoring logic; no copy of those rules here.
- Idempotency: `finishTest` takes a client-generated `testId` (UUID); a repeat call returns the stored session instead of creating a second one.

## Local development

`pnpm --filter functions dev` builds in watch mode; `firebase emulators:start` runs Auth, Firestore, Storage, Functions. A fake Claude (`CLAUDE_FAKE=1`) streams canned lessons so local work costs nothing.
