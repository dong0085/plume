# functions: agent notes

Read `functions/SPEC.md`, then the L3 `SPEC.md` of the function group you work on.

- Every callable goes through `src/lib/callable.ts` for auth, App Check, zod input parsing, error codes, and logging.
- Scoring and text rules come from `packages/core`; book and session shapes come from `packages/schema`.
- Quota changes happen in transactions through `src/lib/quota.ts`: reserve before calling Claude, commit on success, refund on failure or refusal.
- Claude calls go through `src/lib/claude.ts`, which handles streaming, stop reasons, and cost accounting.
- Logs hold the hashed uid, function name, duration, outcome, and token counts.
- Run against emulators with `CLAUDE_FAKE=1` for local work and tests.
- New Firestore or Storage paths get rules and rules tests in `firebase/` in the same change.
