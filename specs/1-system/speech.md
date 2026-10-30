# Speech: read aloud

Level: L1 System · Status: Review
Features: SPK-1–6, TYP-12 (dictée).

## Short answer: can the web app use the system voice?

**Yes.** Browsers expose the device's text-to-speech voices through the **Web Speech API** (`window.speechSynthesis`). No server, no cost, no API key. It's the web version of what the CLI does with `say`.

What a person gets depends on their browser and device:

| Browser | Voices it offers | French quality |
|---|---|---|
| **Safari** (macOS, iOS, iPadOS) | The system voices, including downloaded Enhanced/Premium ones in most versions | Best match to the CLI experience |
| **Chrome** (macOS, Windows) | Local system voices **plus** Google's online voices ("Google français") | Good; Google voices need internet |
| **Edge** (Windows, macOS) | Local voices **plus** Microsoft's online "Natural" voices (for example *Denise*, *Henri*, *Sylvie* for Canada) | Very good |
| **Firefox** | Local system voices | Same as the OS |
| **Chrome on Android** | The phone's text-to-speech engine (usually Google), with French if installed | Good |

Two limits to know:
1. A website can't pick a voice file directly. It can only choose from the list the browser offers, and some browsers hide some downloaded premium voices.
2. Quality varies across devices. The P2 cloud-voices feature (SPK-5) fixes this for everyone, at a cost.

Testing: the [Plume Design System](https://claude.ai/artifact/4tw9Z76BdBMRzu2ZyCg3co) page includes a **live voice check** that lists the French voices your browser offers and plays a sample.

## Web design (`apps/web/src/features/listen`)

```ts
const u = new SpeechSynthesisUtterance(text);
u.lang = "fr-FR";          // fallback when no voice is chosen
u.voice = chosenVoice;     // from speechSynthesis.getVoices()
u.rate = slow ? 0.7 : 1;
speechSynthesis.speak(u);
// stop: speechSynthesis.cancel()
```

**Choosing the voice (same idea as the CLI):**
1. Keep voices whose `lang` starts with `fr`.
2. Rank: name contains "Premium" → "Enhanced" / "Natural" / "Neural" / "Online" → other local voices → novelty voices last (Grandma, Grandpa, Rocko, Eddy, Flo, Reed, Sandy, Shelley, Jacques). Ties: `fr-FR` before `fr-CA` (the books are from France), then local before online.
3. The person's choice is saved per device (voice URIs differ across devices).

**Gotchas handled:**
- `getVoices()` can be empty at first in Chrome → wait for the `voiceschanged` event.
- Chrome can cut off long utterances → speak one sentence per utterance, queued.
- iOS Safari needs a user tap or key press to start speech → the Listen button and shortcut are user actions.
- Word highlight (SPK-4): use `boundary` events with `charIndex` when the voice sends them; online voices often don't, so highlight falls back to sentence level.
- Text sent to the voice: the original passage (with `—`, `«»`), never the typed text.

## Mobile design (`apps/mobile/src/features/listen`)

`expo-speech`:

```ts
Speech.speak(text, { language: "fr-FR", voice: voice.identifier, rate: slow ? 0.7 : 1 });
Speech.stop();
const voices = await Speech.getAvailableVoicesAsync(); // { identifier, name, quality, language }
```

- iOS returns the system voices with `quality: "Enhanced"` for downloaded higher-quality voices → ranked first.
- Android returns the engine's voices; quality comes from the engine.
- No French voice → Listen shows how to add one: iOS **Settings → Accessibility → Spoken Content → Voices → French**; Android **Settings → Text-to-speech → Install voice data → French**.
- Audio ducks other audio and respects the silent switch setting chosen in Settings ("Play even when silent", default on).

## Dictée mode (P1)

- Splits the passage into sentences with `packages/core` sentence rules.
- Plays one sentence, waits for typing, then plays the next when the person reaches the end of the sentence (or on "Replay").
- Needs a French voice; the mode is disabled with help text when none exists.

## Cloud voices (P2, SPK-5)

- Server generates MP3 per passage with a neural French voice (Google Cloud Text-to-Speech in the same project, or another provider chosen then), cached at `tts/{sha256(text+voice)}.mp3`.
- Used when the device has no French voice, or when the person picks "Studio voice" in Settings.
- Cost guard: per-user daily limit; cached audio reused across users for library passages.
