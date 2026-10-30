# Information architecture

Level: L1 Experience · Status: Review

## The objects people work with

```
Person ──┬── Settings (level, theme, font, voice, typing rules)
         ├── Stats (totals, bests, streak)
         ├── My books ── Passages
         ├── Sessions ── Test result + Lesson + Follow-ups
         └── My words (P1)

Library (shared) ── Books ── Passages
```

- A **passage** belongs to one book. A book is either in the **library** (public domain, everyone) or in **my books** (one owner).
- A **session** points to one passage and keeps a copy of its text, so it still works if the book is deleted.
- A **test** without an account lives only in the browser until the guest signs up.

## Web sitemap

```
/                      Type (home). Typing test. Landing hero above it for first-time visitors.
├── /s/:sessionId      Session: result + lesson + follow-up chat (also the "resume" view)
├── /library           Library: tabs [Classics] [My books]
│   ├── /library/:bookId           Book page
│   └── /library/upload            Upload (modal over /library on wide screens)
├── /history           History: list of sessions, filters
├── /stats             Stats: totals, trends, accent heatmap (P1), calendar (P1)
├── /words             My words (P1)
├── /settings          Settings: sections [Typing] [Appearance] [Listening] [Lessons] [Account]
├── /auth/sign-in
├── /auth/sign-up
├── /auth/reset
├── /welcome           Onboarding (after first sign-up)
├── /about, /privacy, /terms
└── 404
```

**Why the test lives at `/`:** the typing test is the product. Opening the site puts the cursor in the text, ready to type, the same way the best typing sites work.

### Web global layout

```
┌──────────────────────────────────────────────────────────────┐
│ plume ✒      Type  Library  History  Stats        ⚙  (E)     │  top bar (fades in focus mode)
├──────────────────────────────────────────────────────────────┤
│                                                              │
│                     page content                             │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ tab + enter  restart · esc  commands · ⌘L  listen    v1.0   │  hint footer (fades in focus mode)
└──────────────────────────────────────────────────────────────┘
```

- `(E)` = account menu: profile, settings, sign out. Guests see **Sign in**.
- On narrow screens, the nav collapses to a menu button. The typing screen stays full width.

## Mobile structure (Expo Router)

```
(tabs)
├── Type        typing test → result → lesson (stacked)
├── Library     Classics / My books → Book → Upload
├── History     sessions → Session (resume)
└── Profile     stats, settings, account
(auth)          sign-in, sign-up, reset   (modal stack)
welcome         onboarding                (modal stack)
```

Words (P1) becomes a fifth tab when it ships.

## URL and deep-link map

| Path | Web | Mobile route | Notes |
|---|---|---|---|
| `/` | Type | `(tabs)/type` | Query: `?book=:bookId&mode=time&t=60` presets the test |
| `/s/:sessionId` | Session | `(tabs)/history/[sessionId]` | Owner only |
| `/library/:bookId` | Book | `(tabs)/library/[bookId]` | Library books public; my books owner only |
| `/library/upload` | Upload | `(tabs)/library/upload` | Signed-in only |
| `/history` | History | `(tabs)/history` | Signed-in only |
| `/stats` | Stats | `(tabs)/profile/stats` | Signed-in only |
| `/settings` | Settings | `(tabs)/profile/settings` | Guests get local-only settings |

Deep links on mobile use the web domain (universal links / app links), P1.

## Access by role

| Page | Guest | Signed in | Email not verified |
|---|---|---|---|
| Type, Library (classics), Book (classic) | yes | yes | yes |
| Lesson + follow-ups | shown as a sign-up prompt with a preview of the lesson sections | yes | yes, with a banner to verify |
| Upload, My books | sign-up prompt | yes | blocked until verified (prevents abuse) |
| History, Stats, Words, Session | sign-up prompt | yes | yes |
| Settings | local only (theme, font, typing rules, voice) | synced | synced |

## Navigation rules

1. The typing test is never more than one click or tap away (logo, "Type" tab, Tab+Enter).
2. After a test, the result and lesson appear **in place** on web (the URL changes to `/s/:sessionId` once saved), so Back returns to a fresh test.
3. Starting a new test from a session page goes to `/` with the same settings.
4. Settings changed from the config bar persist and show in Settings.
5. Every list (history, library, words) keeps scroll position and filters when you come back to it.

## Content hierarchy on the typing screen

In order of visual weight:

1. The passage text and caret
2. Live stats (small, above the text, left)
3. Book title and author (small, below the text)
4. Config bar (above stats, fades while typing)
5. Listen button (beside the book line)
6. Top bar and footer (fade while typing)

## Content hierarchy on the session screen

1. Result headline: WPM and accuracy, large
2. Per-word review of the passage
3. Lesson (streams in)
4. Follow-up box (sticky at the bottom on mobile)
5. Secondary stats and speed chart (collapsible on mobile)
6. Actions: Next passage, Same passage again, Listen, Save words (P1)
