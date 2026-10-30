# apps/cli

Level: L2 Folder · Status: Review
Parent specs: `specs/0-product/vision.md#where-it-starts`, `specs/decisions.md` (D14)

## Purpose

The original Plume: a terminal app that picks a passage from a French classic, checks your typing word by word, streams a Claude lesson, answers follow-up questions, saves sessions (`--resume`, `--history`), and reads passages aloud with macOS voices (`/l`, `/slow`).

## Plan

- At M0, `plume.py` moves here unchanged (`git mv plume.py apps/cli/plume.py`); the `~/.local/bin/plume` symlink is updated to the new path.
- It stays standalone: no Firebase, no account. It keeps its own cache in `~/.cache/plume/`.
- It serves as the **reference behavior** for `packages/core` text rules and word comparison (golden tests are generated from it).

## Later (only if the owner asks)

- Sign in with a device code and sync sessions to the same account.
- Use the same `nextPassage` API so CLI and apps share the library and uploaded books.
