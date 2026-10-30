# core/scoring: results and live stats

Level: L3 Module · Status: Review
Parent: `packages/core/SPEC.md` · Features: RES-1, RES-2, RES-3, TYP-15

## Definitions

Let `minutes` = (endedAt − startedAt − pausedMs) / 60,000.

| Number | Formula | Notes |
|---|---|---|
| **WPM** | (characters of `ok` and `slip` words + one space per such word after the first) ÷ 5 ÷ minutes | Standard 5-characters-per-word measure. In strict mode, `slip` words don't count |
| **Raw WPM** | (all typed characters, including incorrect and extra, + spaces) ÷ 5 ÷ minutes | Speed regardless of errors |
| **Accuracy** | correct keystrokes ÷ (correct + incorrect keystrokes); slips count as correct in lenient mode, incorrect in strict | 0–100% |
| **Consistency** | 100 × (1 − coefficient of variation of the per-second raw WPM samples), clamped 0–100, using samples after the first second | Higher is steadier |
| **Characters** | correct / incorrect / extra / missed / slips | Over finished words + the partial last word |

## Per-second samples (for the chart)

For each whole second of active time (pauses removed):
- `wpm[i]`: WPM over the time so far (cumulative), so the line settles as the test goes on
- `raw[i]`: raw WPM within that one second (instant)
- `errors[i]`: incorrect keystrokes in that second

The last partial second is scaled to a full second.

## Per-word results

`words: {status, expected, typed}[]`. `typed` is filled only for non-ok words (keeps the session doc small).

## Live stats

`liveStats(state, now)` gives WPM and accuracy so far, using `now` for elapsed time. The UI calls it at most 4 times per second (not per keystroke), so the numbers are readable.

## Edge cases

- Test shorter than 2 seconds: WPM is computed but flagged `tooShort: true`; UI shows it but it never sets a personal best.
- Zero keystrokes: accuracy 0, WPM 0.
- Time mode with a partial word at timeUp: counts its correct letters toward WPM characters, without the trailing space.

## Personal best key

`modeKey = mode + "-" + (time | words | length) + "-" + accentRule`, for example `time-60-strict`, `passage-medium-lenient`. Bests compare WPM; ties go to higher accuracy.
