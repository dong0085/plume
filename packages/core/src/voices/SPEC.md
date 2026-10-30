# core/voices: choosing a French voice

Level: L3 Module · Status: Review
Parent: `packages/core/SPEC.md` · Features: SPK-3 · See `specs/1-system/speech.md`

## Input

```ts
interface VoiceLike {
  id: string;          // web: voiceURI; mobile: identifier
  name: string;
  lang: string;        // "fr-FR", "fr_CA", "fr"
  local?: boolean;     // web: localService
  quality?: "default" | "enhanced" | "premium";   // mobile reports this; web infers it from the name
}
```

## Ranking

1. Keep voices whose `lang` starts with `fr` (case-insensitive, `-` or `_`).
2. Quality score:
   - 4: `quality === "premium"` or name contains "Premium"
   - 3: `quality === "enhanced"` or name contains "Enhanced", "Natural", "Neural", "Wavenet", "Studio"
   - 2: an online voice from a known provider (name starts with "Google" or "Microsoft")
   - 1: other voices
   - 0: novelty voices: name's first word in {Eddy, Flo, Grandma, Grandpa, Jacques, Reed, Rocko, Sandy, Shelley, Albert, Bahh, Bells, Boing, Bubbles, Cellos, Wobble, Zarvox, Trinoids, Whisper, Superstar, Organ, Jester, Good, Bad}
3. Sort by quality score (high first), then `fr-FR` before other French regions, then local before online, then name.
4. Remove exact duplicates (same name + lang).

## Output

The sorted list plus a label for the picker: `"Audrey · Premium · France"`, `"Amélie · Canada"`, `"Google français · online"`.

## Tests

Fixtures: the macOS voice list from the CLI test machine (Audrey Premium first), a Chrome macOS list, an Edge Windows list, an Android list, and an empty list.
