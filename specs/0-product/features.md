# Feature list

Level: L0 Product · Status: Review

Every feature has an ID. Lower-level specs refer to these IDs.

**Priority**
- **P0**: in the first public release (MVP)
- **P1**: soon after launch
- **P2**: later, once the core is proven

**Platform**: W = web, M = mobile, S = server (Cloud Functions), C = shared core package

---

## 1. Accounts and profile

| ID | Feature | Pri | Platform |
|---|---|---|---|
| ACC-1 | Sign up and sign in with email + password, with email verification | P0 | W M S |
| ACC-2 | Sign in with Google | P0 | W M |
| ACC-3 | Sign in with Apple (required on iOS when Google sign-in is offered) | P0 | W M |
| ACC-4 | Password reset by email | P0 | W M |
| ACC-5 | Guest mode: type passages without an account; sign up to get lessons and save history | P0 | W M |
| ACC-6 | Guest progress carries over when the guest signs up (anonymous account linking) | P0 | W M S |
| ACC-7 | Onboarding: pick French level (A1–C2), check read-aloud voice, first passage | P0 | W M |
| ACC-8 | Profile: display name, avatar initial, level, joined date | P0 | W M |
| ACC-9 | Delete account and all data (books, sessions, vocab) | P0 | W M S |
| ACC-10 | Export my data as JSON | P1 | W S |
| ACC-11 | Settings sync across devices | P0 | W M |

## 2. Typing test (the Monkeytype-grade core)

| ID | Feature | Pri | Platform |
|---|---|---|---|
| TYP-1 | Live per-letter marks while typing: untyped (dim), correct, incorrect, extra, missed, accent slip | P0 | W M C |
| TYP-2 | Smooth caret that glides between letters; caret styles: line, block, underline, off | P0 / P1 styles | W M |
| TYP-3 | Word-based flow: space moves to the next word; backspace can go back into a wrong word | P0 | C |
| TYP-4 | Ctrl/Option + Backspace deletes the whole word | P0 | W C |
| TYP-5 | Accents and dead keys work: macOS Option keys, Windows US-International, AZERTY, long-press on phones, IME composition events | P0 | W M C |
| TYP-6 | French typography is forgiving: `'`=`’`, `oe`=`œ`, `"`=`« »`, optional spaces before `; : ! ?`, `-`=`—` | P0 | C |
| TYP-7 | Accent rule: **strict** (an accent slip counts as an error) or **lenient** (accent slips pass but are still shown in yellow and counted) | P0 | C W M |
| TYP-8 | Punctuation rule: strict or ignore punctuation | P1 | C W M |
| TYP-9 | Modes: **passage** (type one whole passage) | P0 | C W M |
| TYP-10 | Modes: **time** (15 / 30 / 60 / 120 s across flowing passages from one book) | P0 | C W M |
| TYP-11 | Modes: **words** (10 / 25 / 50 / 100 words) | P1 | C W M |
| TYP-12 | Modes: **dictée** (hear the passage, type it without seeing it; text revealed at the end) | P1 | W M |
| TYP-13 | Modes: **zen** (type freely over a passage, no timer, no score) | P2 | W M |
| TYP-14 | Passage length: short / medium / long | P0 | C W M |
| TYP-15 | Live stats while typing (WPM, accuracy, timer or progress), each can be hidden | P0 | W M |
| TYP-16 | Quick restart: Tab, then Enter (web); restart button (mobile) | P0 | W M |
| TYP-17 | Focus mode: everything except the text fades while typing | P0 | W M |
| TYP-18 | Test config bar above the text: mode, length, accent rule, book source | P0 | W M |
| TYP-19 | Stop on error: off / stop on letter / stop on word | P1 | C |
| TYP-20 | Confidence mode: backspace off | P1 | C |
| TYP-21 | Blind mode: errors hidden until the end | P2 | W M |
| TYP-22 | Keypress sounds (several soft sets) | P1 | W M |
| TYP-23 | Tape mode: one line that scrolls sideways | P2 | W |
| TYP-24 | Accent bar on phones: one-tap é è ê à ç ù î ô œ « » above the keyboard | P0 | M |
| TYP-25 | Pause on blur: test pauses when the window loses focus; resume on refocus | P0 | W M |
| TYP-26 | Keystroke log recorded for each test (timing + key), used for stats and replay | P0 | C |

## 3. Results

| ID | Feature | Pri | Platform |
|---|---|---|---|
| RES-1 | Result card: WPM, accuracy, raw WPM, consistency, time, characters (correct / incorrect / extra / missed / accent slips) | P0 | W M C |
| RES-2 | Per-word review of the passage: each word marked, with what was typed vs the original | P0 | W M |
| RES-3 | Speed chart over time: WPM and raw WPM per second, error dots | P0 / M P1 | W M |
| RES-4 | Personal best badge per mode + length | P1 | W M S |
| RES-5 | Replay: watch the test play back keystroke by keystroke | P2 | W |
| RES-6 | Accent heatmap: which accented letters you miss most (é è ê à ç …) | P1 | W M |
| RES-7 | Share a result image (stats + passage line + book) | P2 | W M |

## 4. Lessons and follow-up (Claude)

| ID | Feature | Pri | Platform |
|---|---|---|---|
| LES-1 | Lesson streams in after a test: Meaning, Words worth keeping, Grammar spotlight, About the book, Your typing | P0 | W M S |
| LES-2 | Lessons match the learner's level | P0 | S |
| LES-3 | Follow-up questions in the same conversation, streamed | P0 | W M S |
| LES-4 | Suggested follow-up chips ("Explain the passé simple", "More examples", "Say it simpler") | P1 | W M S |
| LES-5 | Thumbs up / down on each lesson, with an optional note | P0 | W M S |
| LES-6 | Daily lesson quota per user, shown in the UI before it runs out | P0 | W M S |
| LES-7 | Tap any word in the passage for a quick meaning (cached per word + passage) | P1 | W M S |
| LES-8 | Lesson language: English explanations by default; "more French" setting for B2+ | P1 | S |
| LES-9 | Retry a lesson that failed or was cut off | P0 | W M S |

## 5. Listening

| ID | Feature | Pri | Platform |
|---|---|---|---|
| SPK-1 | Read the passage aloud with the device's French voice | P0 | W M |
| SPK-2 | Slow read-aloud | P0 | W M |
| SPK-3 | Voice picker that lists only French voices, best first (Premium → Enhanced → standard) | P0 | W M |
| SPK-4 | Word highlight follows the voice while it reads (where the platform reports word boundaries) | P1 | W M |
| SPK-5 | Cloud voices: high-quality French audio generated on the server and cached, for devices with weak or no French voices | P2 | S W M |
| SPK-6 | Keyboard shortcut to listen (web): Ctrl/Cmd + L when not typing | P0 | W |

## 6. Library and books

| ID | Feature | Pri | Platform |
|---|---|---|---|
| LIB-1 | Public library of public-domain French classics (the CLI's 17 books to start, then more) | P0 | W M S |
| LIB-2 | Book page: cover, title, author, year, short blurb, passage count, "Type from this book" | P0 | W M |
| LIB-3 | Choose a source for tests: random from all, one book, or my books only | P0 | W M |
| LIB-4 | Upload a book: EPUB or TXT, up to 25 MB | P0 | W M S |
| LIB-5 | Upload PDF (text-based PDFs) | P1 | W S |
| LIB-6 | Processing status: uploading → processing → ready, or failed with a clear reason | P0 | W M S |
| LIB-7 | Edit title/author of an uploaded book; delete it with all its passages | P0 | W M S |
| LIB-8 | Language check on upload: warn when a book does not look French | P0 | S |
| LIB-9 | Type in order: continue a book from where you left off, passage by passage | P1 | W M S |
| LIB-10 | Chapters: pick a chapter to type from (EPUB table of contents) | P1 | W M S |
| LIB-11 | Passage difficulty estimate (A1–C2) shown before typing | P2 | S |
| LIB-12 | Library search and filter (author, era, difficulty) | P1 | W M |

## 7. History, progress, and words

| ID | Feature | Pri | Platform |
|---|---|---|---|
| HIS-1 | History list: every session with date, book, passage start, WPM, accuracy, number of questions | P0 | W M |
| HIS-2 | Resume any session: passage, result, lesson, and chat restored; keep asking | P0 | W M |
| HIS-3 | Stats page: tests done, time typed, average and best WPM, accuracy trend, accent-slip trend | P0 / charts P1 | W M |
| HIS-4 | Daily goal (minutes or tests) and streak | P1 | W M S |
| HIS-5 | Save a word or expression from a lesson to "My words" | P1 | W M |
| HIS-6 | Review my words with spaced repetition (type the French word from its meaning) | P2 | W M |
| HIS-7 | Calendar heatmap of activity | P1 | W |

## 8. Appearance and settings

| ID | Feature | Pri | Platform |
|---|---|---|---|
| SET-1 | Themes: Encre (dark) and Papier (light) at launch; follow system by default | P0 | W M |
| SET-2 | More themes (8+) and a custom theme editor | P1 / P2 | W M |
| SET-3 | Typing font: serif (default), sans, or mono; text size | P0 | W M |
| SET-4 | Reduced motion respected (caret jumps, no glide) | P0 | W M |
| SET-5 | All typing, listening, lesson, and account settings in one Settings page | P0 | W M |

## 9. Navigation and power use

| ID | Feature | Pri | Platform |
|---|---|---|---|
| NAV-1 | Command palette (Esc or Cmd/Ctrl + K): change mode, theme, voice, book, jump to pages | P1 | W |
| NAV-2 | Keyboard shortcut list (`?`) | P1 | W |
| NAV-3 | Deep links: `/b/:bookId`, `/s/:sessionId` open on web and in the app | P1 | W M |

## 10. Community (later)

| ID | Feature | Pri | Platform |
|---|---|---|---|
| COM-1 | Leaderboards: daily and all-time per mode, with server-side checks on the keystroke log | P2 | W M S |
| COM-2 | Classes: a teacher shares a reading list and sees class progress | P2 | W S |
| COM-3 | Public profile page | P2 | W |

## 11. Operations

| ID | Feature | Pri | Platform |
|---|---|---|---|
| OPS-1 | Admin script to add public-domain books to the library | P0 | tools |
| OPS-2 | Usage dashboard: lessons per day, Claude cost, upload failures | P1 | S |
| OPS-3 | Error reporting on web, mobile, and functions | P0 | W M S |
| OPS-4 | Product analytics events (see `1-system/architecture.md#analytics`) | P1 | W M |
| OPS-5 | Feature flags and remote config (lesson quota, model, maintenance banner) | P0 | S W M |

---

## What makes Plume different from a general typing site

Plume borrows the conventions people love in typing tests: instant per-letter feedback, a smooth caret, quick restart, focus mode, clean results with a speed chart, and themes. It has its own look and identity. What only Plume has:

- **Real French literature** as the text, with the book and author always shown
- **Accent slips** as a first-class result, with a lenient accent mode and an accent heatmap
- **A lesson and a tutor chat** after every test
- **Listening and dictée**
- **Your own books**, private to you
- **Resume any session** and keep asking
