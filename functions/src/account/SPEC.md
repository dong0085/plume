# functions/account: deleteAccount, exportData

Level: L3 Module · Status: Review
Parent: `functions/SPEC.md` · Features: ACC-9 (P1: ACC-10) · Privacy: `specs/1-system/security.md#privacy`

## deleteAccount

1. Auth required; `auth_time` within the last 5 minutes, else `failed-precondition: reauth` (client re-authenticates and retries).
2. Delete Storage prefix `uploads/{uid}/` and `exports/{uid}/`.
3. `recursiveDelete` on `users/{uid}` and `usage/{uid}`.
4. Delete the Auth user (`admin.auth().deleteUser(uid)`).
5. Log only "account deleted" with the uid hash.

If a step fails, retry it up to 3 times; the function is safe to call again (every step tolerates already-deleted data). The client signs out after success.

## exportData (P1)

1. Gather `users/{uid}` (profile, settings), `books` metadata (not passages), `sessions` (including lessons and chat), `words`, `private/stats`.
2. Write `exports/{uid}/{exportId}.json` and return a signed URL valid for 24 h.
3. One export per hour per user.

## Tests

Emulator test: create a full fixture account (books with passages, sessions, usage, Storage files) → delete → nothing remains under any path for that uid; repeat call succeeds.
