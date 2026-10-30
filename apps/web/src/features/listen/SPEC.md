# web/features/listen

Level: L3 Module · Status: Review
Parent: `apps/web/SPEC.md` · Features: SPK-1, 2, 3, 6 (P1: SPK-4, TYP-12)
System spec: `specs/1-system/speech.md` · Ranking: `packages/core/src/voices/SPEC.md`

## Pieces

| Piece | Job |
|---|---|
| `useVoices()` | Loads `speechSynthesis.getVoices()`, waits for `voiceschanged` (up to 3 s), maps to `VoiceLike` (`id = voiceURI`, `local = localService`), ranks with `rankFrenchVoices` |
| `useSpeaker()` | `speak(text, {slow})`, `stop()`, `state: idle | speaking`, `currentChar` (P1) |
| `ListenControls` | Listen / Stop button and Slow button with the voice name in a tooltip |
| `VoicePicker` | Settings and onboarding: ranked list with labels and a Sample button |
| `NoVoiceHelp` | Per-OS instructions to add a French voice (macOS, Windows, ChromeOS, Android, iOS) |

## Behavior

- Chosen voice: per-device `localStorage` key `plume.voice` (voice URI). If missing or unavailable, use the top-ranked voice.
- `speak` splits the text with `splitSentences` and queues one utterance per sentence (avoids Chrome's long-utterance cut-off). `rate` = 1 or 0.7 (Slow); `lang` = the voice's lang.
- Pressing Listen while speaking stops. Pressing Slow while normal speech plays restarts slowly (same as the CLI).
- Speech stops when the test ends, restarts, or the page changes.
- Shortcut Ctrl/Cmd + L (Listen) and Ctrl/Cmd + Shift + L (Slow), registered in `lib/shortcuts.ts`; they work while typing and are never inserted as text.
- Word highlight (P1): `boundary` events give `charIndex`; the passage marks the word being spoken with a soft `--surface-2` background. If no boundary events arrive within 1 s, highlight the current sentence instead.

## Edge cases

- `speechSynthesis` missing → hide listen controls; show `NoVoiceHelp` in Settings.
- No French voices → Listen shows a tooltip "No French voice on this device" with a link to help.
- Safari needs a user gesture → speech only starts from a click or the shortcut (a key press counts).

## Tests

Mock `speechSynthesis` in unit tests (voices arriving late, none, boundary events). Manual pass on Safari, Chrome, Edge, Firefox per milestone.
