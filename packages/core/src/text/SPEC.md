# core/text: French text rules

Level: L3 Module · Status: Review
Parent: `packages/core/SPEC.md` · Features: TYP-6, TYP-7, TYP-8, LIB-4, LIB-8

## Normalization (what counts as "the same letter")

Applied to both the passage and the typed input before comparing letters. Display always shows the original passage.

| Passage has | Also accepted | Rule |
|---|---|---|
| `’` `‘` `ʼ` | `'` | always |
| `«` `»` `“` `”` | `"` or nothing | always (quotes are optional; see "optional characters") |
| `—` `–` | `-` | always |
| `œ` `Œ` | `oe` `Oe` | always (one passage letter matches two typed letters) |
| `æ` `Æ` | `ae` `Ae` | always |
| `…` | `...` | always |
| non-breaking space, narrow nbsp | space | always |
| space before `; : ! ? »` and after `«` | nothing | always (French spacing is optional) |
| `é` | `e` | only with accent rule **lenient**; recorded as a slip |
| `,` `.` `;` etc. | anything | only with punctuation rule **ignore** (P1) |
| uppercase | lowercase | never (case counts), except the first letter after `—` dialogue dashes which old editions vary on |

### Optional characters

Some passage characters may be skipped without error: `« » “ ”` and the spaces around them, and French typographic spaces. The engine treats them as optional tokens: typing them matches; skipping them moves on silently.

### Accent rule

- **strict**: `e` for `é` is an incorrect letter.
- **lenient**: `e` for `é` is accepted for scoring, marked as a **slip** in yellow, and counted in `chars.slips`.

The accent-equivalence table is generated from Unicode NFD (base letter + combining mark), plus `œ`/`æ` ligatures and `ç`.

## Words

`splitWords(s)` splits on whitespace. Hyphenated words (`peut-être`) and elisions (`l'homme`, `aujourd'hui`) are one word. Leading dialogue dashes (`—`) are their own token and optional to type.

## Sentences

`splitSentences(s)` splits after `. ! ? …` (and the same followed by `»`) when the next non-space character is an uppercase letter, `«`, or `—`. Abbreviations that must not split: `M.`, `Mme`, `Mlle`, `MM.`, `Dr.`, `St.`, `etc.` followed by lowercase, single capital initials (`J. Verne`).

## Cleaning a paragraph

1. Collapse whitespace; remove `_` (Gutenberg italics); replace `--` with ` — `.
2. Convert straight quotes inside French text to the original's style only for display (no change in stored text).
3. Trim.

## Prose filter

A cleaned paragraph is a passage candidate when:
- letters ≥ 70% of characters; fewer than 4 digits
- not all uppercase; no `[` (notes) and no "Gutenberg"
- starts with an uppercase letter (including accented), `«`, or a dash
- ends with `. ! ? » …`

## Cutting a book into passages

`cutPassages(text, {sizes})`:
1. Strip the Gutenberg header/footer when present (`*** START OF` / `*** END OF`).
2. Split into paragraphs on blank lines; drop the first 3% (front matter).
3. For each size bucket (short 100–200, medium 200–350, long 350–550 characters):
   - paragraphs within the bucket become passages
   - longer paragraphs give their opening sentences up to the bucket's max, if the result is at least the bucket's min and passes the filter
4. Each passage gets `order` (paragraph index) and `size`.

For EPUB, the caller passes text per chapter so `chapter` can be set (P1).

## French check

`frenchScore(sample)` on a 20,000-character sample: share of the 100 most common French words among all words, scaled to 0–1, plus a bonus for French accented letters. Books score above 0.6; English books below 0.2. Threshold for the "doesn't look French" warning: 0.35. Tune with fixtures.

## Tests

Golden tables for every normalization row, every abbreviation, and the CLI's 17 books (passage counts per size must stay within ±5% of the CLI's counts).
