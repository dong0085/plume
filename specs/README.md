# Plume specs

Plume is a French-learning typing app. You type a real passage of French literature, see exactly what you got right, and get a short lesson from Claude on what the passage means and how its French works. You can ask follow-up questions, listen to the passage read aloud, and type from books you upload yourself.

This folder holds the plan. Code starts only after the plan is approved.

## How the specs are organized

The specs come in four levels. Each level adds detail and points up to the level above it.

| Level | Answers | Lives in |
|---|---|---|
| **L0 Product** | Why are we building this, for whom, and what is in it? | `specs/0-product/` |
| **L1 Experience** | What does the person see and do? | `specs/1-experience/` |
| **L1 System** | How is it built, where does data live, how do parts talk? | `specs/1-system/` |
| **L2 Folder** | What does this app or package own, and what is its public surface? | `SPEC.md` at the root of each app and package |
| **L3 Module** | How does this one feature or module behave, in detail? | `SPEC.md` inside each feature or module folder |

When two levels disagree, the higher level wins. Fix the lower one, or raise the change in `specs/decisions.md`.

## Reading order

1. [0-product/vision.md](0-product/vision.md): the problem, the people, the goals
2. [0-product/features.md](0-product/features.md): every feature, with priority
3. [0-product/roadmap.md](0-product/roadmap.md): milestones and what "done" means for each
4. [1-experience/information-architecture.md](1-experience/information-architecture.md): screens, navigation, URLs, objects
5. [1-experience/ux-flows.md](1-experience/ux-flows.md): the key journeys, step by step
6. [1-experience/ui-design.md](1-experience/ui-design.md): layouts, the typing screen, motion, accessibility
7. [1-experience/design-system.md](1-experience/design-system.md): tokens, type, color, components. Live preview: [Plume Design System](https://claude.ai/artifact/4tw9Z76BdBMRzu2ZyCg3co)
8. [1-system/tech-stack.md](1-system/tech-stack.md): tools and why
9. [1-system/architecture.md](1-system/architecture.md): how the parts fit
10. [1-system/data-model.md](1-system/data-model.md): Firestore, Storage, indexes
11. [1-system/api.md](1-system/api.md): Cloud Function contracts
12. [1-system/security.md](1-system/security.md): auth, rules, App Check, privacy, copyright
13. [1-system/ai-lessons.md](1-system/ai-lessons.md): Claude prompts, streaming, cost, quotas
14. [1-system/speech.md](1-system/speech.md): read-aloud on web and mobile
15. [1-system/testing.md](1-system/testing.md): test plan, CI, definition of done
16. [decisions.md](decisions.md): decisions made, and decisions waiting on the owner

## Project folders and their specs

```
plume/
├── AGENTS.md                      agent guide for the whole repo
├── CLAUDE.md                      points Claude Code at AGENTS.md
├── specs/                         L0 + L1 (this folder)
├── design/
│   └── tokens.json                tokens exported from the Plume Design System artifact
├── apps/
│   ├── web/                       L2 SPEC.md · React web app
│   │   └── src/features/*/        L3 SPEC.md per feature
│   ├── mobile/                    L2 SPEC.md · Expo iOS + Android app
│   │   └── src/features/*/        L3 SPEC.md per feature
│   └── cli/                       L2 SPEC.md · the original Python CLI
├── functions/                     L2 SPEC.md · Cloud Functions
│   └── src/*/                     L3 SPEC.md per function group
├── packages/
│   ├── core/                      L2 SPEC.md · typing engine, scoring, text tools
│   │   └── src/*/                 L3 SPEC.md per module
│   ├── schema/                    L2 SPEC.md · shared data shapes (zod)
│   └── tokens/                    L2 SPEC.md · design tokens
├── firebase/                      L2 SPEC.md · rules, indexes, emulator config
└── tools/
    └── seed-library/              L2 SPEC.md · imports the public-domain library
```

## Status words

Each spec starts with a status line:

- **Draft**: being written
- **Review**: ready for the owner to read
- **Approved**: the owner said yes; build from it
- **Built**: code matches the spec

Every spec here starts at **Review**.

## Glossary

| Word | Meaning |
|---|---|
| **Passage** | A short run of text (about 100–550 characters) cut from a book, the unit you type |
| **Test** | One typing attempt on a passage or a timed run |
| **Session** | A test plus its lesson and follow-up chat, saved so you can resume it |
| **Accent slip** | A word typed with the right letters but wrong or missing accents (`eleve` for `élève`) |
| **Lesson** | Claude's explanation of a passage: meaning, words, grammar, book context, typing tips |
| **Follow-up** | A question you ask after the lesson, answered in the same conversation |
| **Dictée** | A mode where you hear the passage and type it without seeing it |
| **Library** | Public-domain books everyone can use |
| **My books** | Books a person uploads; private to them |
| **Lenient / strict** | Typing rules for accents and French punctuation (see `packages/core/src/text/SPEC.md`) |
| **Level** | The learner's French level on the CEFR scale (A1–C2); it shapes lessons |
