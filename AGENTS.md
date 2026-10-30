# Plume: agent guide

Plume is a French-learning typing app. People type passages of French literature, see exactly what they got right, and get a short lesson from Claude. It has a web app, an iOS and Android app, Firebase on the server, and the original Python CLI.

## Current phase: planning

The project is in the planning phase. Work happens in `specs/` and the `SPEC.md` files. Coding starts when the owner says so in a message. Until then, changes go to specs, agent docs, and the design system.

## Read first

1. `specs/README.md`: how specs are organized, reading order, glossary
2. The `SPEC.md` at the root of the folder you work in (L2)
3. The `SPEC.md` in the feature or module folder you work in (L3)
4. `specs/decisions.md`: settled decisions and open questions

Higher-level specs win. When code and spec differ, update the spec in the same change, or raise it in `specs/decisions.md`.

## Repo map

| Folder | What lives there |
|---|---|
| `apps/web` | React + Vite single-page app (Firebase Hosting) |
| `apps/mobile` | Expo app for iOS and Android |
| `apps/cli` | The original Python CLI, the reference for text rules |
| `functions` | Cloud Functions (Node 22, TypeScript) |
| `packages/core` | Typing engine, scoring, French text rules, voice ranking: pure TypeScript |
| `packages/schema` | zod schemas for every stored doc and function payload |
| `packages/tokens` | Design tokens and their build |
| `firebase` | Security rules, indexes, Remote Config defaults, rules tests |
| `tools/seed-library` | Script that loads public-domain books |
| `design` | Exported design tokens; the live design system is the Plume Design System artifact |
| `specs` | L0 product and L1 experience/system specs |

## Commands (from M0 on)

| Task | Command |
|---|---|
| Install | `pnpm install` |
| Run everything locally | `pnpm dev` (web, mobile dev server, functions watch, emulators) |
| Typecheck, lint, test | `pnpm typecheck` · `pnpm lint` · `pnpm test` |
| One package | `pnpm --filter <name> <task>` |
| Emulators only | `pnpm emulators` |
| Rules tests | `pnpm --filter firebase test` |
| Web end-to-end | `pnpm --filter web e2e` |
| Seed the local library | `pnpm seed-library --project emulator` |

## How we write code

- TypeScript strict everywhere. Types for stored data come from `packages/schema`.
- `packages/core` stays pure: plain functions, time passed in, runs in browsers, React Native, and Node.
- All text and scoring rules live in `packages/core`. Apps and functions call it.
- UI uses token names from `packages/tokens` (`--text-untyped`, `slip`), so themes work everywhere.
- Each feature lives in its own folder with its L3 `SPEC.md`, components, hooks, and tests side by side.
- Tests sit next to the code they test; end-to-end tests live in each app's `e2e/` or `.maestro/`.
- Match the style of the surrounding code: naming, comment density, file layout.

## Claude API

- Lessons use the official `@anthropic-ai/sdk` with `claude-opus-5-5`, read from Remote Config. Details: `specs/1-system/ai-lessons.md`.
- The API key lives in Secret Manager (`ANTHROPIC_API_KEY` via `defineSecret`) and reaches only the lesson functions.
- Local work uses the fake Claude stream (`CLAUDE_FAKE=1`).

## Privacy and security

- Logs and analytics carry IDs, counts, and timings. Passage text, book text, questions, and lessons stay out of them.
- Every new Firestore or Storage path gets rules and rules tests in the same change.
- Uploaded books belong to their uploader alone.

## Commits and PRs

- One feature or fix per branch and PR, named after the feature ID when there is one (`typ-7-accent-rule`).
- Commit messages and PR descriptions describe the project change in plain words. They contain project content only.
- PRs list the spec files they touch and the feature IDs they complete.

## Writing docs and specs

- Use simple, plain language.
- Write in positive framing: say what things are and what to do.
- Keep each spec's status line current: Draft, Review, Approved, Built.
