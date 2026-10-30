# core/engine: the typing state machine

Level: L3 Module · Status: Review
Parent: `packages/core/SPEC.md` · Features: TYP-1, 3, 4, 5, 9–14, 19, 20, 25, 26

## Model

A test is a list of **target words** (from `splitWords(passage)`) and a cursor. Each target word holds what was typed for it.

```ts
type LetterState = "untyped" | "correct" | "incorrect" | "slip" | "extra" | "missed";

interface WordState {
  target: string;          // original word as shown
  typed: string;           // raw typed text for this word
  letters: LetterState[];  // one per target letter + one per extra letter
  done: boolean;           // space pressed after it
  status?: "ok" | "slip" | "wrong" | "missed";   // set when done
}

interface TestState {
  config: TestConfig;
  words: WordState[];       // grows in time mode as passages are appended
  index: number;            // current word
  startedAt?: number;       // first keystroke time
  endedAt?: number;
  pausedMs: number;
  keystrokes: { correct: number; incorrect: number; slips: number; total: number };
  log: TimedEvent[];        // every event with time
  phase: "ready" | "running" | "paused" | "done";
}
```

## Events

```ts
type InputEvent =
  | { t: number; type: "insert"; text: string }       // one or more characters (composition result, accent bar, paste-blocked)
  | { t: number; type: "space" }
  | { t: number; type: "backspace" }
  | { t: number; type: "deleteWord" }                  // Ctrl/Option + Backspace
  | { t: number; type: "pause" } | { t: number; type: "resume" }
  | { t: number; type: "timeUp" }
  | { t: number; type: "append"; passage: string };    // time mode: next passage flows in
```

Platforms turn their input into these events (web: `beforeinput` + composition events; mobile: TextInput diffs). The engine never sees key codes, so keyboard layouts and dead keys work the same everywhere.

## Rules

1. **First insert** starts the test (`startedAt = t`, `phase = running`).
2. **insert**: compares the typed letter(s) with the target at the current position using `core/text` rules. Past the end of the word, letters become `extra` (max 10 extra per word, then ignored).
   - `œ` in the target accepts `o` then `e`: after `o` the letter is "pending"; `e` completes it; anything else makes it incorrect.
3. **space**:
   - On an empty current word: ignored (no skipping by double space).
   - Otherwise: the word is `done`. Untyped target letters become `missed`. Status: `ok` (all correct), `slip` (only slips), `wrong` (any incorrect, extra, or missed).
   - Moves to the next word. On the last word of a passage in passage mode, the test ends when the last word is complete and correct, or on space.
4. **Passage end**: in passage mode the test also ends the moment the last letter of the last word is typed correctly (no trailing space needed).
5. **backspace**: removes the last typed letter of the current word. On an empty current word, goes back into the previous word **only if** that word's status is not `ok` (`slip` counts as not ok in strict mode). Confidence mode (P1) blocks backspace entirely.
6. **deleteWord**: clears the current word; if already empty, behaves like one backspace into the previous word, then clears it.
7. **Stop on error (P1)**: `letter` rejects an incorrect insert (counted as an error keystroke, nothing added); `word` rejects space on a wrong word.
8. **pause / resume**: time between them is added to `pausedMs` and excluded from all timing.
9. **timeUp** (time mode): ends the test; the current partial word counts only its correct letters.
10. **Time mode**: when the cursor reaches the second-to-last passage, the app appends the next passage (`append`), so text never runs out.
11. **Words mode (P1)**: target words are the first N words across passages; ends when word N is done.
12. **Dictée (P1)**: same engine; the UI hides letters. No engine difference.

## Keystroke counting

- Each insert of one letter is one keystroke: correct, incorrect, or slip.
- A space that ends a correct word is a correct keystroke; on a wrong word it is incorrect.
- Backspace and deleteWord are not counted as keystrokes (but are logged).

## Keystroke log

Every event is appended to `log` with its time. Packed for storage:

```
<version>|<startEpochMs>|<events>
events = ";" joined: <deltaMs base36>,<code>[,<payload>]
codes: i=insert (payload = text, escaped), s=space, b=backspace, w=deleteWord, p=pause, r=resume, t=timeUp, a=append (payload = passage index)
```

Example: `1|1793374364000|0,i,I;8c,i,l;5f,s;...`. About 6 bytes per keystroke; a 2-minute test is under 10 KB.

`replay(passage, config, log)` runs the events through `apply` and must reproduce the client's final state exactly.

## Performance

- `apply` touches only the current word (and the previous one on backspace). The `words` array uses structural sharing so React can memo unchanged words.
- No regex or normalization of the whole passage per keystroke: the target word's normalized form is computed once at `createTest` / `append`.
