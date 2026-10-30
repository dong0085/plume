# web/features/typing

Level: L3 Module · Status: Review
Parent: `apps/web/SPEC.md` · Features: TYP-1–7, 9, 10, 14–18, 25 (P1: TYP-8, 11, 19, 20, 22)
Uses: `packages/core` engine and scoring

## Components

| Component | Job |
|---|---|
| `TypingTest` | Owns one test: creates the engine state, wires input, ends the test, calls `finishTest` |
| `Passage` | Renders words and letters with their states, the caret, and line scrolling |
| `HiddenInput` | A visually hidden `<textarea>` that receives all typing (keeps IME, dead keys, and mobile keyboards working) |
| `ConfigBar` | Mode, time/length, accent rule, source; fades in focus mode |
| `LiveStats` | WPM/accuracy or seconds left; updates 4× per second |
| `FocusChrome` | Fades the top bar, footer, and config bar while typing; restores on mouse move |
| `RestartButton` | Tab target; Enter restarts |

## Input handling

All typing goes to `HiddenInput`, focused whenever the Type page is active (click anywhere on the passage refocuses it).

| DOM event | Engine event |
|---|---|
| `beforeinput` `insertText` (outside composition) | `insert(data)`; space → `space` |
| `compositionend` | `insert(event.data)` (dead keys, long-press menus, IMEs) |
| `beforeinput` `insertCompositionText` | ignored (wait for `compositionend`) |
| `keydown` Backspace | `backspace` (Ctrl/Option held → `deleteWord`) |
| `keydown` Tab | focus `RestartButton`, prevent default |
| `keydown` Escape | restart (P0) / command palette (P1) |
| `beforeinput` `insertFromPaste`, drop | blocked |
| `window` blur / `visibilitychange` hidden | `pause`; overlay "Click or press any key to continue" |

After each event the textarea is cleared, so the browser never builds up a long value. Timestamps use `event.timeStamp` mapped to `performance.timeOrigin` (same clock as the engine).

Autocorrect, autocapitalize, spellcheck, and autocomplete are off on the textarea; `lang="fr"`.

## Rendering and performance

Target: input-to-paint under 16 ms at p95 (see `testing.md`).

- The engine state lives in a ref, not React state. Each event updates only the DOM nodes of the current word (and the previous one on backspace) through a small imperative renderer: each `<span class="letter">` gets a `data-s` attribute (`u c i s x m`), styled by CSS.
- React renders the passage once per test (and on `append` in time mode).
- The caret is one absolutely positioned element moved with `transform: translate()` to the measured box of the next letter (`getBoundingClientRect` relative to the passage, cached per line on layout). Smooth caret: CSS transition `--motion-caret`; reduced motion: none.
- Line scrolling: when the caret reaches line 3, the passage shifts up by one line height (`transform`, 150 ms). Lines are measured after fonts load (`document.fonts.ready`) and on resize.
- Live stats use `requestAnimationFrame` throttled to 250 ms.

## Letter styling

| State | Style |
|---|---|
| untyped | `--text-untyped` |
| correct | `--text` |
| incorrect | `--error`, plus a 2 px underline in `--error` |
| slip | `--slip`, dotted underline |
| extra | `--error-extra`, appended after the word |
| missed | `--text-untyped` with a solid `--error` underline |

Done words with status `slip` get the dotted underline across the whole word.

## Test lifecycle

1. On mount: `nextPassage(count: 2)`; render the first; keep the second as the prefetched next.
2. First keystroke: start; focus mode on.
3. End (passage complete, timer, or words count): compute `score()` for the instant result card, then call `finishTest` with the packed log. Show the result immediately from the client score; replace with the server result when it returns (they should match; a mismatch logs to Sentry).
4. Restart (Tab+Enter or Esc): new test with the prefetched passage, prefetch another.
5. Same passage again: restart with the same passage.

Abandoned tests (restart before the end) are discarded.

## Config bar

Reads and writes `settings.typing` and `settings.source`. Changes apply to the next test (and restart the current one if it has not started). In time mode the source must be one book or "all"; the timer counts down from the chosen seconds.

## Accessibility

- The passage has `lang="fr"` and an `aria-label` with the full text; letters are `aria-hidden`.
- A polite live region announces "Test finished. 58 words per minute, 96% accuracy."
- Screen-reader mode (P1) announces each word's result.

## Tests

- Unit: input mapping table (every row above), including composition sequences for ⌥e e, AZERTY dead circumflex, and Windows US-International.
- E2E: type a full passage with accents in strict and lenient mode; time mode ends on time; pause on blur; Tab+Enter restart; paste blocked.
- Perf: 600-character passage at 4× CPU throttle, p95 input-to-paint < 16 ms.
