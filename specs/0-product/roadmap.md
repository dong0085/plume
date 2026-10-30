# Roadmap

Level: L0 Product · Status: Review

Each milestone ends with something people can use. Feature IDs come from `features.md`.

## M0: Foundations (about 1 week)

**Goal:** an empty but real project that builds, tests, and deploys.

- Monorepo with pnpm + Turborepo; `apps/web`, `apps/mobile`, `functions`, `packages/*`, `firebase/`
- `apps/cli` holds the existing Python CLI, still working
- Firebase project with dev and prod environments; Emulator Suite runs locally
- CI: typecheck, lint, unit tests on each push; preview deploy of web on each PR
- Design tokens package and the two launch themes

**Done when:** `pnpm dev` starts web, mobile, and emulators together, and a "hello" page deploys to a preview URL.

## M1: Typing core (about 2 weeks)

**Goal:** the best possible typing test, no account needed.

- `packages/core`: engine, text normalization, scoring, keystroke log (TYP-1, 3–7, 9, 10, 14, 26; RES-1)
- Web typing screen with smooth caret, live stats, config bar, focus mode, restart, pause on blur (TYP-2, 15–18, 25)
- Results card, per-word review, speed chart (RES-1–3)
- Library seeded with the 17 CLI books (LIB-1, OPS-1); passages served from Firestore
- Read aloud with voice picker on web (SPK-1–3, 6)
- Guest mode (ACC-5)

**Done when:** a guest can open the site, type a passage in passage or time mode with accents, see a full result, and listen to the passage. The input-to-paint target from `vision.md` is met.

## M2: Accounts and lessons (about 2 weeks)

**Goal:** the full Plume loop on the web.

- Sign up / in with email, Google, Apple; onboarding; guest linking (ACC-1–8, 11)
- Lessons and follow-ups streamed from Cloud Functions (LES-1–3, 5, 6, 9)
- Sessions saved; history list; resume (HIS-1, 2)
- Settings page, themes, fonts, reduced motion (SET-1, 3–5)
- Stats page, numbers only (HIS-3)
- Remote config, error reporting (OPS-3, 5); delete account (ACC-9)

**Done when:** a new person signs up, picks a level, types, gets a streamed lesson, asks two follow-ups, leaves, and resumes the session the next day on another browser.

## M3: Uploads (about 1.5 weeks)

**Goal:** type from your own books.

- Upload EPUB/TXT, processing pipeline, status, language check, edit and delete (LIB-4, 6–8)
- Source picker: all / one book / my books (LIB-3)
- Book pages (LIB-2)

**Done when:** a person uploads an EPUB, sees it process, and types from it. Nobody else can see it, and deleting it removes every trace.

## M4: Mobile app (about 3 weeks)

**Goal:** the same loop on iOS and Android.

- Expo app with tabs: Type, Library, History, Profile
- Mobile typing input with accent bar (TYP-24) and long-press accents
- Lessons, follow-ups, history, resume, uploads via document picker, read aloud with expo-speech
- TestFlight and Play internal testing builds through EAS

**Done when:** the M2 and M3 "done" stories pass on an iPhone and an Android phone, and the apps are in TestFlight and Play internal testing.

## M5: Public launch

- App Store and Play Store review, privacy labels, store listings
- Production Firebase hardening: App Check enforced, budget alerts, quotas tuned
- Landing page

**Done when:** the apps are live in both stores and the web app is on the production domain.

## After launch (P1, then P2)

Priority order for P1, based on expected value to learners:

1. Personal bests, accent heatmap, stats charts, calendar (RES-4, RES-6, HIS-3 charts, HIS-7)
2. Dictée mode (TYP-12) and word highlight while listening (SPK-4)
3. Tap a word for meaning (LES-7); suggested follow-ups (LES-4)
4. My words (HIS-5); daily goal and streak (HIS-4)
5. Words mode, punctuation rule, stop on error, confidence mode, sounds, caret styles (TYP-8, 11, 19, 20, 22)
6. Type in order and chapters (LIB-9, 10); PDF uploads (LIB-5); library search (LIB-12)
7. Command palette and shortcuts (NAV-1, 2); deep links (NAV-3)
8. More themes (SET-2); data export (ACC-10); analytics and usage dashboard (OPS-2, 4)

P2 items wait for evidence: leaderboards, classes, cloud voices, spaced repetition, replay, share image, blind and tape modes, other languages, paid plans.
