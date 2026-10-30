# functions/lessons: lesson, followUp, wordMeaning

Level: L3 Module · Status: Review
Parent: `functions/SPEC.md` · System spec: `specs/1-system/ai-lessons.md` · Features: LES-1–3, 5, 6, 9 (P1: LES-4, 7, 8)

## lesson

1. Auth: signed in, not anonymous. Load the session; owner only.
2. If `lesson.status == "ready"`: stream `messages[0].content` as one chunk; finish.
3. If `generating` and `startedAt` under 90 s ago: return `failed-precondition: generating` (client listens to the doc).
4. Quota reserve (transaction on `usage/{uid}/days/{date}`): `lessons + 1 ≤ limit`, and the global daily spend is under the cap. Else `resource-exhausted` with `resetsAt`.
5. Set `lesson.status = "generating"`, `startedAt`, `model`, `level` (from the profile).
6. Build the request (`ai-lessons.md`): system prompt, one user message with the tagged passage, book, level, typing summary.
7. Stream with `client.beta.messages.stream(...)`: forward each text delta via `response.sendChunk(text)` when the client accepts streaming; accumulate the full text.
8. On finish, by `stop_reason`:
   - `end_turn` → save `messages = [{role: "assistant", content, at}]`, `lesson.status = "ready"`, `finishedAt`; commit usage (tokens, cost)
   - `max_tokens` → same, plus `lesson.truncated = true`
   - `refusal` → `lesson.status = "failed"`, `failReason: "refusal"`; refund quota
9. On error (after SDK retries): `lesson.status = "failed"`; refund; `unavailable`.
10. If the client disconnects, keep going to step 8 (the function runs to completion).

Note: `messages[0]` stores only the assistant's lesson. The lesson user message is rebuilt from the session each time it is needed (it is deterministic from stored fields), keeping the doc small and the prompt editable.

## followUp

1. Same auth and ownership. `lesson.status` must be `ready`; `messages.length < 60`.
2. Quota reserve: `followUps + 1 ≤ limit` (and global cap). "Please finish the lesson." on a truncated lesson is free.
3. Messages for Claude: `[user: rebuilt lesson message, assistant: messages[0], …stored turns…, user: question]`. Top-level `cache_control: {type: "ephemeral"}`.
4. Stream as above; on success append `{user: question}` and `{assistant: answer}` in one update (`arrayUnion` is unsafe for duplicates, so use a transaction that reads and appends), `questionCount + 1`.
5. On refusal or error: append nothing; refund; error code.

## wordMeaning (P1)

- Cache key `wordCache/{sha256(passageText)}-{wordIndex}` (shared across users for library passages; per-user path for uploaded books).
- Model per `decisions.md` Q2; short JSON answer via structured outputs (`output_config.format` with a JSON schema: word, lemma, meaning, pos, gender, note).
- Counted against a separate, larger quota (e.g. 100/day).

## Cost accounting

`lib/claude.ts` computes cost from `usage` (input, output, cache read, cache write tokens) with prices from Remote Config (`claudePrices`), and writes it to `usage/{uid}/days/{date}.costMicros` and a global `usageGlobal/{date}` doc (server-only) used for the daily cap.

## Tests

Fake Anthropic stream fixtures: normal, `max_tokens`, `refusal`, network error mid-stream, overloaded then success. Check quota reserve/refund under concurrent calls, the 90 s generating guard, and that a disconnected client still gets a saved lesson.
