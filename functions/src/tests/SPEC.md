# functions/tests: nextPassage and finishTest

Level: L3 Module · Status: Review
Parent: `functions/SPEC.md` · Contracts: `specs/1-system/api.md` · Features: TYP-9, 10, 14, 26, RES-1, 4, LIB-3

## nextPassage

1. Resolve the collection: `library/*/passages` (all classics), `library/{bookId}/passages`, `users/{uid}/books/{bookId}/passages`, or "mine" (random ready book of the user, weighted by passage count).
2. For "all classics": pick a book at random weighted by its passage count for the size, then a passage.
3. Random passage: `where size == S, where rand >= r, orderBy rand, limit 1`; if empty, `rand < r` ordered by rand. Skip IDs in `private/recent.ids`; retry up to 3 times.
4. Return `count` passages (default 1). Do **not** update `recent` here (prefetches may go unused); `finishTest` records it.

Rate limit: 120 per minute per uid (in-memory token bucket per instance + Firestore counter only if abuse is seen).

## finishTest

Input: `{ testId, passageRefs: [{passageId, bookId, source}], config, log, clientResult, tz }`. Time mode can span several passages, so it takes a list.

1. Load the passage texts. Time mode: join them in order as the engine did with `append`.
2. `unpackLog` → `replay` → `score` with `packages/core`.
3. Reject when: log over 200 KB, events out of order, duration under 1 s or over the mode's limit + 10 s, typed characters above 25 per second sustained (bot-like). Rejected tests return `invalid-argument` and are not saved.
4. Compare with `clientResult`; a difference above 0.5 WPM or 0.5% accuracy logs a warning with the version of core on each side.
5. Skip saving (return the result with `sessionId: null`) if fewer than 5 words were typed.
6. Transaction:
   - create `users/{uid}/sessions/{testId}` with passage copy, config, result, log, `lesson.status: "none"`, `questionCount: 0`
   - update `private/stats`: totals, accents map (from per-word slips and wrong accented letters), best for the mode key (if not `tooShort`), streak and `days` using `tz`
   - push passage IDs to `private/recent.ids` (keep the last 50)
7. Return `{ sessionId, result, personalBest }`.

## Tests

Replays of golden logs; tampered logs rejected; idempotent repeat; stats transaction under concurrent calls; streak across midnight in America/Toronto and Pacific/Auckland.
