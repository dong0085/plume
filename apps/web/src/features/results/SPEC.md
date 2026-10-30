# web/features/results

Level: L3 Module · Status: Review
Parent: `apps/web/SPEC.md` · Features: RES-1, 2, 3 (P1: RES-4, 6; P2: RES-5, 7)

## Components

| Component | Job |
|---|---|
| `ResultCard` | Headline WPM and accuracy (`--type-display`, mono), secondary stats (raw, consistency, time), character breakdown with colored counts |
| `SpeedChart` | uPlot chart: WPM line (`--brand`), raw line (`--text-subtle`, thinner), error dots (`--error`) on a second axis. X axis in seconds. Hover shows values for that second |
| `WordReview` | The passage with each word colored by status; hover/focus/tap on a marked word opens a tooltip: "You typed **perkluse** · original **percluse**" |
| `ResultActions` | Listen, Type it again, Next passage (Tab+Enter) |
| `PersonalBestBadge` (P1) | "New best for time 60 · strict" in `--success` |

## Behavior

- Appears in place of the passage with the `--motion-slow` rise.
- Uses the client result at once; swaps in the server result silently when `finishTest` returns.
- `tooShort` results show numbers with a note "Too short to count" and no chart.
- In time mode, WordReview shows only the words reached, plus a faint "…" for the rest.
- Lazy-loads uPlot (chart appears with a 120 ms fade; skeleton before).

## Accessibility

- ResultCard is a region with a heading "Your result"; numbers have text labels.
- The chart has a text summary under it ("Speed rose from 40 to 58 words per minute; 3 errors, mostly in the second half.") built from the samples.
- WordReview tooltips open on focus as well as hover; words are buttons only when marked.

## Tests

Visual snapshots of the result card for: perfect run, many slips (lenient), many errors (strict), time mode partial, too short; both themes.
