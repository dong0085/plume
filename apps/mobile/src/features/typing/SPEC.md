# mobile/features/typing

Level: L3 Module · Status: Review
Parent: `apps/mobile/SPEC.md` · Same behavior as `apps/web/src/features/typing/SPEC.md` except where noted · Features: TYP-1–7, 9, 10, 14–18, 24, 25

## Input capture

Phones give no reliable key events, so typing goes through a hidden `TextInput` and Plume reads the **difference** between its old and new value.

| Prop | Value |
|---|---|
| `autoCorrect` | false |
| `autoCapitalize` | "none" |
| `spellCheck` | false |
| `autoComplete` | "off" |
| `keyboardType` | "default" (iOS: `"ascii-capable"` is off because it blocks accents) |
| `textContentType` / `importantForAutofill` | "none" / "no" |
| `contextMenuHidden` | true (no paste) |
| `caretHidden` | true |
| `blurOnSubmit` | false |

**Sentinel technique:** the input always holds one sentinel character (a zero-width space) with the selection after it. On each `onChangeText`:
- value shorter than the sentinel → `backspace` (Android Gboard sends deletes this way)
- new characters after the sentinel → one `insert` per character; a space → `space`
- then reset the value to the sentinel

`onKeyPress` adds Backspace detection where the platform sends it (iOS hardware keyboards, some Android keyboards) and is de-duplicated against the value diff.

Long-press accents on iOS and Android arrive as a replacement of the last letter: the diff shows "delete 1, insert é". This becomes `backspace` + `insert("é")` and counts as one keystroke (no error is recorded for the base letter if it was replaced within 1.5 s).

Hardware keyboards (iPad, Bluetooth): Tab+Enter restart via `onKeyPress`; Option dead keys arrive as composed text.

## Accent bar (TYP-24)

- A bar above the keyboard: `é è ê à â ç ù û î ï ô ë œ « » ’` (scrolls sideways; most used first, ordered by the person's own accent misses (P1)).
- iOS: `InputAccessoryView`; Android: an absolutely positioned view above the keyboard using keyboard height events.
- Tap → `insert(letter)` + light haptic. The input keeps focus (the bar never steals it).
- Setting to hide it.

## Rendering

- Letters are `Text` spans inside one `Text` per line. Each word is a memoized component keyed by word index; only the current word re-renders per event.
- Caret: a Reanimated view positioned from `onTextLayout` line/character metrics; spring off, timing 80 ms; reduced motion → jump.
- 3 visible lines above the keyboard; scrolls one line at a time.
- Live stats update 4× per second through a Reanimated shared value (no React re-render).

## Lifecycle differences

- App to background (`AppState` change) → `pause`; returning shows "Tap to continue" and reopens the keyboard.
- Incoming call or Siri → same as background.
- Tabs hide while a test runs (`tabBarStyle` display none) and return on the result.

## Tests

- Unit: diff-to-event mapping for every case above, including Gboard batch inserts and the iOS long-press replacement.
- Maestro: type a short passage with the accent bar; background/foreground pause; restart.
- Manual matrix from `specs/1-system/testing.md`: iOS keyboard, Gboard, Samsung Keyboard, SwiftKey, hardware keyboard on iPad.
