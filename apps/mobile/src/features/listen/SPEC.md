# mobile/features/listen

Level: L3 Module · Status: Review
Parent: `apps/mobile/SPEC.md` · Same behavior as `apps/web/src/features/listen/SPEC.md` except where noted · Features: SPK-1, 2, 3
System spec: `specs/1-system/speech.md`

## Differences from web

- Voices from `Speech.getAvailableVoicesAsync()` → `VoiceLike { id: identifier, name, lang: language, quality: quality.toLowerCase() }` → `rankFrenchVoices`.
- `Speech.speak(sentence, { voice, language, rate, onDone, onStopped, onError })`, queued one sentence at a time (same as web).
- Chosen voice saved per device in AsyncStorage `plume.voice`.
- Audio session: plays when the silent switch is on if Settings → Listening → "Play when silent" is on (default on); ducks other audio.
- Word highlight (P1): `onBoundary` where the platform supports it (iOS); sentence highlight otherwise.
- No French voice: `NoVoiceHelp` with the iOS or Android steps from `speech.md`, plus a button that opens the system settings screen where possible.

## Tests

Mock `expo-speech` in unit tests (voices list per platform fixture). Manual pass on iOS with an Enhanced French voice installed and on Android with Google TTS French.
