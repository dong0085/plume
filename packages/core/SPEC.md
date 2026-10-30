# packages/core

Level: L2 Folder · Status: Review
Parent specs: `specs/1-system/architecture.md`, `specs/0-product/features.md` (TYP-*, RES-1)

## Purpose

The brain of Plume's typing, shared by web, mobile, and Cloud Functions. Pure TypeScript with no I/O, no React, no Firebase, no DOM. Given a passage, settings, and keystrokes, it says exactly what state the test is in and what the result is. The server runs the same code to verify results.

## Modules

| Module | Job | L3 spec |
|---|---|---|
| `src/text/` | French text rules: normalization, word splitting, accent stripping, sentence splitting, passage cleaning and cutting | `src/text/SPEC.md` |
| `src/engine/` | The typing state machine: input events in, letter/word state out; keystroke log packing | `src/engine/SPEC.md` |
| `src/scoring/` | WPM, raw, accuracy, consistency, character counts, per-second samples, per-word results | `src/scoring/SPEC.md` |
| `src/voices/` | Rank a list of voices (name, lang, quality, local) for French, used by web and mobile | `src/voices/SPEC.md` |
| `src/index.ts` | Public exports only | — |

## Public surface

```ts
// text
normalize(s: string, rules: TextRules): string
splitWords(s: string): string[]
stripAccents(s: string): string
splitSentences(s: string): string[]
cleanParagraph(raw: string): string
cutPassages(bookText: string, opts?: CutOptions): CutPassage[]
frenchScore(sample: string): number                  // 0–1

// engine
createTest(passage: string, config: TestConfig): TestState
apply(state: TestState, event: InputEvent): TestState  // pure
packLog(events: TimedEvent[]): string
unpackLog(packed: string): TimedEvent[]
replay(passage: string, config: TestConfig, log: string): TestState

// scoring
score(state: TestState): Result
liveStats(state: TestState, now: number): { wpm: number; acc: number; elapsedMs: number }

// voices
rankFrenchVoices<V extends VoiceLike>(voices: V[]): V[]
```

Types come from `packages/schema` where they are stored (Result, TestConfig); engine-only types live here.

## Rules

- Every function is pure and deterministic. Time comes in through events (`t` in ms), never from `Date.now()` inside core.
- Fast: `apply` runs in under 0.1 ms for a 600-character passage on a mid-range phone. No allocations of the whole passage per keystroke (structural sharing of word states).
- Behaves the same in browsers, React Native (Hermes), and Node 22.
- 100% branch coverage on `text`, `engine`, `scoring`; property tests from `specs/1-system/testing.md`.

## Carrying over from the CLI

The CLI (`apps/cli/plume.py`) is the reference for:
- passage cleaning (`--` → `—`, underscores removed, Gutenberg header/footer stripped)
- prose filter (`looks_like_prose`), size buckets (short 100–200, medium 200–350, long 350–550 characters), sentence-aware trimming of long paragraphs
- normalization table (`’`→`'`, `œ`→`oe`, `—`/`–`→`-`)
- word comparison (accent-insensitive alignment, then ok / slip / wrong / missing / extra)

Golden tests port the CLI's behavior on the same inputs, then extend it to per-letter live state.
