# firebase

Level: L2 Folder · Status: Review
Parent specs: `specs/1-system/security.md`, `data-model.md`, `tech-stack.md#environments`

## Purpose

Everything Firebase needs that is not function code: security rules, indexes, emulator settings, Remote Config defaults, and the rules tests.

## Layout

```
firestore.rules              rules from security.md (outline → full rules)
firestore.indexes.json       indexes from data-model.md
storage.rules                Storage rules from security.md
remoteconfig.template.json   defaults: lessonModel, quotas, claudePrices, dailySpendCapUsd, flags, maintenanceBanner
test/
├── firestore.rules.test.ts  every allow and deny case
└── storage.rules.test.ts
```

Root files (repo root, because the CLI expects them there): `firebase.json` (hosting for `apps/web/dist`, functions source `functions`, rules and indexes paths here, emulator ports), `.firebaserc` (aliases `dev`, `prod`).

## Hosting config (in `firebase.json`)

- `public: apps/web/dist`, SPA rewrite `** → /index.html`
- Cache: hashed assets `immutable, max-age=31536000`; `index.html` `no-cache`
- Headers from `security.md#web-hardening`
- Preview channels for PRs (7-day expiry)

## Remote Config keys

| Key | Default | Used by |
|---|---|---|
| `lessonModel` | `claude-opus-5-5` | functions |
| `lessonEffort` | `low` | functions |
| `lessonsPerDay` | 5 | functions, clients (display) |
| `followUpsPerDay` | 20 | functions, clients |
| `dailySpendCapUsd` | 25 | functions |
| `claudePrices` | JSON per model (input, output, cache read, cache write per million) | functions |
| `uploadMaxBooks` | 20 | functions, clients |
| `maintenanceBanner` | "" | clients |
| `features` | JSON flags (dictee, wordMeaning, commandPalette, …) | clients |

## Emulators

Auth 9099 · Firestore 8080 · Storage 9199 · Functions 5001 · UI 4000. Project ID `demo-plume` (demo projects never touch real resources). Seed data for local dev comes from `tools/seed-library --emulator`.

## Rules tests

Use `@firebase/rules-unit-testing`. Cases include: a user reading another user's session (deny); writing `plan` on own profile (deny); creating a book with `status: "ready"` (deny); updating a session's `result` (deny); updating `lesson.feedback` (allow); uploading a 26 MB file (deny); uploading to another uid's path (deny); unverified email upload (deny).
