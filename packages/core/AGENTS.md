# packages/core: agent notes

Read `packages/core/SPEC.md` and the module `SPEC.md` (`text`, `engine`, `scoring`, `voices`).

- Every function here is pure and deterministic. Time arrives in event fields; output depends only on input.
- The package runs in browsers, React Native (Hermes), and Node 22 with zod as its only dependency.
- The CLI (`apps/cli/plume.py`) is the reference for text rules; golden tests in `test/golden/` capture its behavior.
- Each change to rules or scoring comes with golden tests and property tests (invariants listed in `specs/1-system/testing.md`).
- `apply` stays fast: it touches the current word (and the previous word on backspace) and shares the rest of the state.
- The server replays logs with this same code, so any behavior change also bumps the log version in `engine/log.ts`.
