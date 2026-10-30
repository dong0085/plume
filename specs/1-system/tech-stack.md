# Technology stack

Level: L1 System · Status: Review

Exact versions get pinned at M0 to the latest stable releases. The choices below are the decisions; `decisions.md` records why.

## Summary

| Layer | Choice |
|---|---|
| Language | TypeScript (strict) everywhere except the existing Python CLI |
| Repo | One monorepo: **pnpm** workspaces + **Turborepo** |
| Web app | **React** + **Vite** (single-page app), **TanStack Router**, **TanStack Query** |
| Web styling | **Tailwind CSS** reading CSS variables from `packages/tokens`; **Radix UI** primitives for menus, dialogs, tooltips |
| Mobile app | **Expo** (React Native) with **Expo Router**, built with **EAS** |
| Mobile styling | `StyleSheet` + typed tokens from `packages/tokens` |
| Shared logic | `packages/core` (typing engine, scoring, French text rules, passage cutting) |
| Shared data shapes | `packages/schema` (**zod**) for Firestore docs and function payloads |
| Auth | **Firebase Authentication**: email/password, Google, Apple, anonymous (guests) |
| Database | **Cloud Firestore** (native mode), region `northamerica-northeast1` (Montréal) |
| Files | **Cloud Storage for Firebase**, same region |
| Server code | **Cloud Functions for Firebase (2nd gen)**, Node.js 22 LTS, same region |
| AI lessons | **Claude API** through the official `@anthropic-ai/sdk`, model `claude-opus-5-5` |
| Secrets | Firebase `defineSecret` (Google Secret Manager) for `ANTHROPIC_API_KEY` |
| Abuse protection | **Firebase App Check**: reCAPTCHA Enterprise (web), App Attest (iOS), Play Integrity (Android) |
| Config + flags | **Firebase Remote Config** |
| Web hosting | **Firebase Hosting** (static SPA + CDN), preview channels per PR |
| Read aloud | Web Speech API (`speechSynthesis`) on web; **expo-speech** on mobile |
| Charts | **uPlot** on web (fast, tiny); **victory-native** on mobile |
| Book parsing | `jszip` + `htmlparser2` for EPUB; `chardet` for TXT encodings; `pdfjs-dist` for PDF (P1) |
| Errors | **Sentry** (web, mobile, functions) |
| Analytics (P1) | Google Analytics for Firebase |
| Unit tests | **Vitest** |
| Web end-to-end | **Playwright** |
| Mobile end-to-end | **Maestro** |
| Backend tests | **Firebase Emulator Suite** + `@firebase/rules-unit-testing` |
| CI/CD | **GitHub Actions**; Firebase Hosting preview channels; EAS Build + Submit |
| Lint/format | ESLint (typescript-eslint) + Prettier |

## Why these choices

**Monorepo with shared core.** The typing engine, scoring, and French text rules must behave the same on web, mobile, and the server (the server re-checks results for stats and later leaderboards). One TypeScript package used by all three keeps them in step.

**React + Vite SPA, not a server-rendered framework.** The app is a fast, client-side typing tool behind sign-in, with no SEO-critical pages except the landing and legal pages. A static SPA on Firebase Hosting is the simplest, fastest, and cheapest fit. The landing and legal pages are prerendered at build time for search engines.

**Expo for mobile.** It shares React and TypeScript with the web, so `packages/core`, `packages/schema`, and `packages/tokens` work unchanged. EAS handles builds, signing, and store submission. `expo-speech` reaches the native iOS and Android voices.

**Firebase JS SDK on mobile.** It works in Expo with React Native auth persistence and keeps one Firebase API across web and mobile. Native-only Firebase features (Crashlytics) are not needed because Sentry covers crashes.

**Cloud Functions 2nd gen.** Longer timeouts (lessons can stream for 30–60 s), concurrency per instance (cheaper for streaming), and Secret Manager support.

**Callable functions with streaming** for lessons. The client calls `httpsCallable(...).stream()` and gets text chunks; the function sends them with `response.sendChunk()`. Auth and App Check tokens are verified automatically. Confirm the minimum `firebase` and `firebase-functions` versions for streaming at M0. **Fallback** if streaming callables fall short on React Native: an HTTPS function that streams Server-Sent Events and verifies the ID token and App Check token by hand (see `api.md`).

**Montréal region.** The owner is in Ottawa; Montréal gives the lowest latency to the first users and keeps data in Canada. Firestore, Storage, and Functions all share the region.

**Claude Opus 5.5.** The model behind the CLI's lessons, giving the best explanation quality. Cost and quota are in `ai-lessons.md`. The model name lives in Remote Config so it can change without a release.

## Repo layout

```
plume/
├── apps/
│   ├── web/          Vite + React SPA
│   ├── mobile/       Expo app
│   └── cli/          Python CLI (existing plume.py, unchanged)
├── functions/        Cloud Functions (TypeScript)
├── packages/
│   ├── core/         engine, scoring, text rules, passage cutting (no I/O, no React)
│   ├── schema/       zod schemas + inferred types
│   └── tokens/       design tokens → CSS vars + TS object
├── firebase/         firestore.rules, storage.rules, indexes, emulator config
├── tools/
│   └── seed-library/ script that loads public-domain books
├── design/           tokens.json (exported from the Plume Design System artifact)
├── specs/            L0 + L1 specs
├── firebase.json, .firebaserc
├── turbo.json, pnpm-workspace.yaml, package.json
├── AGENTS.md, CLAUDE.md
└── README.md
```

## Dependency rules

```
apps/web ─────┐
apps/mobile ──┼──► packages/schema ──► (zod)
functions ────┤
              ├──► packages/core   ──► (no runtime deps)
apps/web, apps/mobile ──► packages/tokens
```

- `packages/core` has no dependencies on React, Firebase, or the DOM. It runs in browsers, React Native, and Node.
- Apps never import from each other.
- `functions` never imports from apps.

## Environments

| Env | Firebase project | Web URL | Mobile |
|---|---|---|---|
| local | emulators (`demo-plume`) | localhost:5173 | Expo dev client against emulators |
| dev | `plume-dev` | `plume-dev.web.app` + PR preview channels | EAS "development" and "preview" builds |
| prod | `plume-prod` | production domain (see `decisions.md`) | EAS "production" builds, stores |
