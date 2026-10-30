# apps/web

Level: L2 Folder · Status: Review
Parent specs: `specs/1-experience/*`, `specs/1-system/tech-stack.md`, `specs/1-system/architecture.md`

## Purpose

The Plume web app: the typing test, results, lessons and follow-ups, library and uploads, history, stats, settings, and auth. A static single-page app on Firebase Hosting.

## Stack

React · Vite · TypeScript strict · TanStack Router (file routes) · TanStack Query (server state) · Tailwind CSS with the `packages/tokens` preset · Radix UI primitives · uPlot · a Markdown renderer with raw HTML off (`react-markdown` without `rehype-raw`) · Firebase JS SDK (modular) · Sentry.

## Layout

```
src/
├── main.tsx                    boot: Firebase, App Check, Sentry, router, theme
├── routes/                     TanStack file routes (map in information-architecture.md)
│   ├── __root.tsx              shell: top bar, footer, toasts, command palette (P1)
│   ├── index.tsx               Type (home)
│   ├── s.$sessionId.tsx        Session
│   ├── library/…               Library, Book, Upload
│   ├── history.tsx · stats.tsx · words.tsx (P1) · settings.tsx
│   ├── auth/…                  sign-in, sign-up, reset
│   └── welcome.tsx             onboarding
├── features/                   one folder per feature, each with an L3 SPEC.md
│   ├── typing/                 typing surface, config bar, live stats, focus mode
│   ├── results/                result card, speed chart, word review
│   ├── lesson/                 streamed lesson, follow-up chat, quota badge, feedback
│   ├── listen/                 Web Speech API, voice picker, listen controls
│   ├── library/                library and my-books lists, book page, upload
│   ├── history/                history list, stats page
│   ├── settings/               settings page and the settings store
│   └── auth/                   sign-in/up, guest linking, onboarding
├── ui/                         design-system components (Button, SegmentedControl, …)
├── lib/
│   ├── firebase.ts             app, auth, db, storage, functions, appCheck, remoteConfig
│   ├── api.ts                  typed wrappers for callables (schemas from packages/schema)
│   ├── queries.ts              TanStack Query keys and fetchers
│   └── shortcuts.ts            global keyboard shortcuts
└── styles/
    ├── fonts.css               self-hosted Literata, Inter, JetBrains Mono
    └── global.css              tokens.css import, base styles
public/fonts/                   woff2 files
e2e/                            Playwright tests (flows, visual, perf)
```

## Cross-cutting rules

- **State:** server data through TanStack Query (Firestore listeners feed the cache for live docs: session, book status). Settings in a small store (Zustand) synced to Firestore with a 500 ms debounce; guests keep settings in `localStorage`.
- **Typing performance:** the typing surface renders outside React's normal update path for each keystroke (see `features/typing/SPEC.md`). Nothing else on the page re-renders per keystroke.
- **Theming:** `data-theme` on `<html>`, set before first paint from settings or `prefers-color-scheme` (inline script in `index.html`) to avoid a flash.
- **Routing:** the Type page preloads the next passage; Session pages load by ID and listen for lesson updates.
- **Accessibility:** follow `ui-design.md#accessibility`; axe checks in Playwright.
- **Errors:** an error boundary per route with a friendly message; Sentry captures with route and feature tags. Never log passage text or chat content.
- **Bundle budget:** first load under 180 KB gzipped JS for `/`; uPlot, Markdown, and the upload code load lazily.

## Environment config

`VITE_FIREBASE_*` keys per environment, `VITE_RECAPTCHA_ENTERPRISE_KEY`, `VITE_SENTRY_DSN`. In local dev, the app connects to emulators when `VITE_USE_EMULATORS=true`.

## Done for this app

All P0 web features from `features.md` pass their L3 specs, Playwright flows F1–F8 pass in Chromium, WebKit, and Firefox, and the performance budget in `testing.md` holds.
