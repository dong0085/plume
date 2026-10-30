# Design system

Level: L1 Experience · Status: Review
Source of truth for values: `packages/tokens`. Live preview: [Plume Design System](https://claude.ai/artifact/4tw9Z76BdBMRzu2ZyCg3co) · Exported values: `design/tokens.json`.

## Principles

1. **Tokens, never raw values.** Components use semantic tokens (`--text-correct`), never hex codes.
2. **Meaning before decoration.** Each color carries one meaning across the app.
3. **One accent.** Ink blue marks the caret and the primary action. Everything else is neutral.
4. **Same tokens on web and mobile.** `packages/tokens` emits CSS variables for web and a typed object for React Native.

## Color

### Semantic tokens

| Token | Use | Encre (dark) | Papier (light) |
|---|---|---|---|
| `--bg` | Page background | `#1A1814` | `#F6F1E7` |
| `--surface` | Cards, inputs, menus | `#23201B` | `#FFFDF8` |
| `--surface-2` | Hover, raised, code | `#2C2822` | `#EFE8DA` |
| `--border` | Hairlines, dividers | `#3A352D` | `#E0D6C3` |
| `--text` | Body text, typed-correct letters | `#EDE6D6` | `#26221C` |
| `--text-subtle` | Labels, live stats, secondary text | `#A39A89` | `#6B6355` |
| `--text-untyped` | Passage letters not yet typed | `#736B5E` | `#8F8676` |
| `--brand` | Caret, primary buttons, links, focus | `#8DB0FF` | `#2851B8` |
| `--on-brand` | Text on brand fill | `#1A1814` | `#FFFDF8` |
| `--error` | Wrong letters, destructive actions | `#F2777A` | `#C23A40` |
| `--error-extra` | Extra letters typed past a word | `#C2585B` | `#A8474B` |
| `--slip` | Accent slips | `#E8B64C` | `#8A5E00` |
| `--success` | Personal best, success toasts | `#8CC890` | `#2F7A42` |
| `--focus-ring` | Keyboard focus outline | `--brand` at 60% | `--brand` at 60% |
| `--cover-bordeaux`, `--cover-ardoise`, `--cover-sauge`, `--cover-ocre` | Generated book-cover tints (`coverTint` in the data model) | see `design/tokens.json` | see `design/tokens.json` |

### Contrast (checked)

| Pair | Encre | Papier | Rule |
|---|---|---|---|
| `--text` on `--bg` | 14.3 | 14.1 | ≥ 4.5 ✓ |
| `--text-subtle` on `--bg` | 6.4 | 5.3 | ≥ 4.5 ✓ |
| `--text-untyped` on `--bg` | 3.4 | 3.2 | ≥ 3 (large text) ✓ |
| `--brand` on `--bg` | 8.3 | 6.3 | ≥ 4.5 ✓ |
| `--error` on `--bg` | 6.5 | 4.7 | ≥ 4.5 ✓ |
| `--slip` on `--bg` | 9.5 | 5.1 | ≥ 4.5 ✓ |
| `--success` on `--bg` | 9.1 | 4.7 | ≥ 4.5 ✓ |
| `--error-extra` on `--bg` | 4.1 | 5.1 | ≥ 3 (large passage text only) ✓ |

The build runs this check on every theme, including future ones (`packages/tokens/SPEC.md`).

### Themes

- **P0:** Encre (dark), Papier (light). Default follows the system setting.
- **P1:** 8+ more. Planned names and moods: *Bordeaux* (wine dark), *Lavande* (soft violet light), *Ardoise* (slate), *Sépia*, *Menthe*, *Nuit blanche* (high contrast dark), *Craie* (high contrast light), *Côte* (sea blue).
- **P2:** custom theme editor (pick the 6 key colors; the contrast check runs live).

## Typography

| Role | Font | Fallback | Use |
|---|---|---|---|
| Passage | **Literata** (variable, 400–600) | Georgia, serif | The text you type; lesson quotes |
| UI | **Inter** (variable) | system-ui, sans-serif | Everything else |
| Numbers | **JetBrains Mono** | ui-monospace | Live stats, result numbers, timers, keyboard hints |

Typing font setting (SET-3): Serif (Literata, default) · Sans (Inter) · Mono (JetBrains Mono).

All three fonts are open-source (OFL), cover every French letter including `œ « »`, and are self-hosted (web) and bundled (mobile).

### Scale

| Token | Size / line height | Use |
|---|---|---|
| `--type-passage` | clamp(22px, 2.2vw + 8px, 32px) / 1.65 | Passage on web; 20–22px on mobile |
| `--type-display` | 56 / 1.0, mono | Result WPM and accuracy |
| `--type-h1` | 28 / 1.25, Inter 600 | Page titles |
| `--type-h2` | 20 / 1.3, Inter 600 | Lesson section headings |
| `--type-body` | 16 / 1.6 | Lesson text, body |
| `--type-small` | 13 / 1.45 | Labels, hints |
| `--type-stat` | 13 / 1.45, mono | Live stats while typing |
| `--type-micro` | 11 / 1.3, 0.04em tracking, uppercase | Chips, badges |

## Space, size, shape

- **Spacing:** 4 px base. Tokens `--space-1` … `--space-12` = 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96.
- **Radius:** `--radius-sm` 6 · `--radius-md` 10 · `--radius-lg` 16 · `--radius-full` 999.
- **Content widths:** passage column 72ch max; reading column (lesson) 68ch; page max 1120 px.
- **Elevation:** flat by default. One shadow token, `--shadow-pop`, for menus, dialogs, and toasts only.
- **Hairlines:** 1 px `--border`.

## Motion

| Token | Value | Use |
|---|---|---|
| `--motion-caret` | 80 ms cubic-bezier(.2,.8,.2,1) | Caret glide |
| `--motion-fast` | 120 ms ease-out | Hovers, lesson blocks |
| `--motion-base` | 200 ms ease-out | Focus fade, toasts |
| `--motion-slow` | 250 ms cubic-bezier(.2,.8,.2,1) | Result card rise |

`prefers-reduced-motion: reduce` sets all durations to 0 except caret blink.

## Components

Each component has: purpose, variants, states, and tokens. Detailed props live in the L3 specs of the app that builds it. Web and mobile build their own versions from the same tokens.

| Component | Variants / notes |
|---|---|
| **Button** | primary (brand fill), secondary (surface + border), ghost, danger. Sizes sm / md / lg. States: hover, active, focus, disabled, loading |
| **IconButton** | ghost square, 36 px (44 pt on mobile). Tooltip required |
| **Kbd** | Key hint chip (`tab`, `⌘ L`), mono, surface-2 |
| **SegmentedControl** | Config bar groups (mode, length, accents). Selected = brand text, no fill |
| **Toggle** | Settings on/off |
| **Select / Menu** | Book source, voice, theme |
| **TextField** | Auth forms, follow-up box (multi-line variant with send button) |
| **Card** | Result card, book card, settings group |
| **Chip** | Suggested follow-ups, status (Processing, Ready, Failed), filters |
| **Badge** | Quota left, personal best, "new" |
| **Toast** | Saved, errors with Retry |
| **Dialog** | Confirmations, upload on wide screens |
| **Tooltip** | Icon buttons, word review details |
| **Tabs** | Library (Classics / My books), Settings sections on mobile |
| **Skeleton** | Loading shapes |
| **EmptyState** | One line + one action |
| **ProgressSteps** | Upload processing steps |
| **Passage** | The typing surface: letters, words, caret, line scroll (see `apps/web/src/features/typing/SPEC.md`) |
| **Letter** | States: untyped, correct, incorrect, extra, missed, slip |
| **Caret** | Styles: line (default), block, underline, off; smooth or jump |
| **LiveStats** | WPM, accuracy, time; mono, subtle |
| **ResultCard** | Headline numbers, secondary stats, character breakdown |
| **SpeedChart** | WPM + raw lines, error dots; brand and subtle colors |
| **WordReview** | Passage with marked words; hover/tap shows typed vs original |
| **LessonView** | Streamed Markdown; headings `--type-h2`; quotes in Literata italics |
| **ChatThread** | Follow-up questions (right, surface-2) and answers (left, plain) |
| **ListenControls** | Listen / Stop, Slow; shows the voice name in a tooltip |
| **VoicePicker** | French voices only, quality label, sample button |
| **AccentBar** | Mobile only: é è ê à ç ù î ô û ë ï œ « » ’, scrolls sideways |
| **BookCover** | Generated typographic cover: title + author on a tinted card |
| **BookCard / SessionRow** | List items for library and history |
| **QuotaBadge** | "7 lessons left today"; amber at 2 or fewer |
| **AccentHeatmap** (P1) | Grid of accented letters colored by miss rate |

## Iconography

Lucide icons (open source, consistent 1.5 px stroke), 16 / 20 / 24 px. The logo is a small quill mark (✒ stands in until a designed mark exists).

## Voice in the interface

See `ui-design.md#copy-style`.
