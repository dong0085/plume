# UI design

Level: L1 Experience · Status: Review
Visual tokens and components: `design-system.md` and the [Plume Design System](https://claude.ai/artifact/4tw9Z76BdBMRzu2ZyCg3co).

## Look and feel

**Ink on paper.** Plume looks like a quiet writing desk: warm paper or deep ink backgrounds, a reading serif for the passage, and one ink-blue accent for the caret and main actions. Nothing moves unless it helps you type or understand.

- Calm while typing; rich after the test.
- The passage is set like a book page, in a reading serif (Literata), not a code font.
- Color has meaning only: cream/ink = correct, dim = not yet typed, red = wrong, amber = accent slip, blue = caret and action.
- Numbers use a mono font so they do not jump as they change.

---

## Screen: Type (web, wide)

### Idle (before the first key)

```
plume ✒        Type   Library   History   Stats                     ⚙   Sign in
────────────────────────────────────────────────────────────────────────────────

        passage · time   │  short · medium · long  │  accents: strict  │  📖 All classics ▾

        ▌Il allait continuer, mais sa langue devint percluse quand il vit
         ces deux filles embrasser tendrement les deux singes, fondre en
         larmes sur leurs corps et remplir l'air des cris les plus

         Candide, ou l'optimisme · Voltaire                     🔊 Listen   🐢 Slow

────────────────────────────────────────────────────────────────────────────────
  tab + enter  restart   ·   esc  commands   ·   ⌘ L  listen
```

- The caret sits before the first letter and blinks.
- 3 lines of text are visible. Longer passages scroll up one line at a time as you reach the third line.
- Text column: max 72 characters wide, centred.

### Typing (focus mode on)

```
        42 wpm   97%                                   (top bar, footer, config fade to 0%)

        Il allait continuer, mais sa langue devint per▌cluse quand il vit
        ces deux filles embrasser tendrement les deux singes, fondre en
        larmes sur leurs corps et remplir l'air des cris les plus
```

- Typed letters turn from dim to full text color. Wrong letters turn red. Extra letters appear after the word in dark red.
- A word finished with an accent slip turns amber with a thin underline.
- A word skipped with space shows its missed letters underlined in red.
- Live stats: WPM and accuracy in passage mode; seconds left in time mode. Mono font, `--text-subtle` color.
- Moving the mouse brings the chrome back (200 ms fade).

### Result + lesson (same page, after the test)

```
        ┌──────────────────────────────────────────────────────────────────┐
        │  58 wpm        96%            raw 62 · consistency 81% · 0:41    │
        │  speed           accuracy        ▁▂▄▆▇▆▅▆▇▇▆▅▆▇  (chart)          │
        │  52 correct · 1 incorrect · 0 extra · 1 missed · 2 accent slips  │
        └──────────────────────────────────────────────────────────────────┘

        Il allait continuer, mais sa langue devint [percluse] quand il vit
        ces deux filles embrasser tendrement les deux singes, ...
        (hover a marked word: typed "percluse"→ shows "perkluse" vs "percluse")

        Candide, ou l'optimisme · Voltaire        🔊 Listen   ↻ Again   → Next (tab+enter)

        ─ Lesson ──────────────────────────────────────── 7 lessons left today
        ## Meaning
        "He was about to go on, but his tongue went stiff..."
        ## Words worth keeping
        • percluse (adj.) — stiff, paralysed ...          [＋ save]  (P1)
        ## Grammar spotlight
        ...
                                                             👍  👎

        ─ Ask a follow-up ───────────────────────────────────────────────
        [ Explain the passé simple ]  [ More examples ]  [ Say it simpler ]   (P1)
        ┌──────────────────────────────────────────────────────────────┐
        │ Ask about this passage…                                  ⏎ │
        └──────────────────────────────────────────────────────────────┘
```

- The result card animates up from where the text was (250 ms).
- The lesson streams in as rendered Markdown, with a soft fade on each new block.
- The follow-up box is focused automatically after the lesson finishes. Tab+Enter still starts the next test.

---

## Screen: Type (mobile app and narrow web)

```
┌─────────────────────────────┐
│ ⚙  passage · 30s · strict ▾ │  config collapses to one tappable summary
│                             │
│ 42 wpm  97%                 │
│                             │
│ Il allait continuer, mais   │
│ sa langue devint per▌cluse  │
│ quand il vit ces deux       │
│                             │
│ Candide · Voltaire    🔊 🐢 │
├─────────────────────────────┤
│ é è ê à ç ù î ô œ « » ’    │  accent bar (above keyboard)
├─────────────────────────────┤
│        system keyboard      │
└─────────────────────────────┘
```

- Text size 20–22 px; 3 lines visible above the keyboard.
- Accent bar: one tap inserts the letter. Long-press a key on the system keyboard also works.
- Autocorrect, autocapitalize, spell check, and predictive text are off for the hidden input.
- Tabs hide while typing; they return on the result screen.

## Screen: Session (mobile)

- Result headline (WPM, accuracy) → per-word review → lesson → chat.
- The follow-up input sticks above the keyboard.
- Speed chart and full stats sit in a collapsible "More stats" row.

## Screen: Library

```
Library                                        [ Classics | My books ]     🔍 (P1)

┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
│  cover    │ │  cover    │ │  cover    │ │ ＋        │   My books tab shows
│           │ │           │ │           │ │ Upload    │   an Upload card first
│ Madame    │ │ Germinal  │ │ Candide   │ │ a book    │
│ Bovary    │ │ Zola      │ │ Voltaire  │ │           │
│ Flaubert  │ │ 1885      │ │ 1759      │ │           │
└───────────┘ └───────────┘ └───────────┘ └───────────┘
```

- Covers: generated typographic covers (title in Literata on a theme-tinted card). No image assets needed; uploaded books use the same style.
- Uploaded book cards show a status chip: Processing · Ready · Failed.

## Screen: Book

Cover, title, author, year, short blurb (library books), passage count, your stats on this book. Actions: **Type from this book** (sets the source), **Continue in order** (P1), Edit / Delete (my books).

## Screen: Upload

Drop zone, rights note, file rules, then a progress list:

```
✓ Uploaded
● Reading the book…
○ Finding passages
○ Checking language
```

## Screen: History

Rows grouped by day:

```
Today
 14:02  Germinal · "Et elle collait son oreille au charbon…"     61 wpm  98%  💬 2
 13:40  Candide · "Il allait continuer, mais sa langue…"          58 wpm  96%  💬 0
Yesterday
 ...
```

## Screen: Stats

Top: four big numbers (tests, time typed, average WPM, best WPM). Below: WPM and accuracy trend (P1 chart), accent heatmap (P1): a keyboard-like grid of accented letters colored by miss rate, calendar heatmap (P1).

## Screen: Settings

Left section list on web, single scrolling page on mobile. Each setting: label, one-line help, control. Live preview for theme and font (a sample passage line rendered with the current choice).

---

## Interaction details

| Input | Action (web) |
|---|---|
| Any letter key | Starts the test and the timer |
| Space | Ends the current word, moves to the next |
| Backspace | Deletes one letter; can go back into the previous word only if it has an error |
| Ctrl/Option + Backspace | Deletes the current word |
| Tab | Focuses the restart button; Tab then Enter restarts |
| Esc | Opens the command palette (P1); before P1, Esc restarts |
| Ctrl/Cmd + L | Listen / stop (when the passage is not being typed into: the shortcut works anywhere, and the key is not inserted) |
| Ctrl/Cmd + Shift + L | Slow listen |
| Window blur | Pauses the test; "Click or press any key to continue" overlay |

## Motion

| Element | Motion | Duration |
|---|---|---|
| Caret | Glides to the next letter position | 80 ms ease-out (`--motion-caret`) |
| Caret blink | Starts after 500 ms idle | 1 s cycle |
| Focus mode fade | Chrome opacity to 0 | 200 ms |
| Line scroll | Text moves up one line | 150 ms |
| Result card | Rises and fades in | 250 ms |
| Lesson blocks | Fade in as they arrive | 120 ms |

With reduced motion: caret jumps, blink stays, all slides become instant fades.

## Accessibility

- Contrast: all text at least 4.5:1, except untyped passage text, which is at least 3:1 (it is large text and must look "not yet typed").
- Color is never the only signal: wrong letters also get a red underline; accent slips get a dotted underline; missed letters a solid underline.
- Screen readers: the passage is announced once before typing; the result card and lesson are announced as they appear (polite live region). A **screen-reader mode** (P1) announces each word's result after space.
- Full keyboard use on web; visible focus ring (`--focus-ring`) on all controls.
- Tap targets at least 44 × 44 pt on mobile.
- Text size setting scales the passage up to 40 px; the layout reflows.
- The UI language is English; French text is marked `lang="fr"` so screen readers and voices pronounce it in French.

## Copy style

Plain, short, friendly. Second person. English UI with a touch of French in greetings ("Bonjour", "À bientôt"). Error messages say what happened and what to do. Examples are in `ux-flows.md`.
