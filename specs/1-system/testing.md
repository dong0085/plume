# Testing and quality

Level: L1 System · Status: Review

## Test layers

| Layer | Tool | What it covers | Where |
|---|---|---|---|
| Unit | Vitest | Engine, scoring, text rules, passage cutting, voice ranking, schema | `packages/*`, app `lib/` folders |
| Property | Vitest + fast-check | Engine invariants on random input (see below) | `packages/core` |
| Golden | Vitest | Known passages + typed input → exact result JSON, ported from the CLI's behavior | `packages/core/test/golden/` |
| Rules | `@firebase/rules-unit-testing` + emulators | Every allow and deny in `security.md` | `firebase/test/` |
| Functions | Vitest + emulators + fake Claude stream | Each callable and trigger, quotas, refunds, stop reasons | `functions/test/` |
| Book ingest | Vitest with fixture files | EPUB (normal, DRM, broken, huge), TXT (UTF-8, Latin-1), non-French | `functions/test/fixtures/` |
| Web end-to-end | Playwright (Chromium, WebKit, Firefox) | Flows F1–F8 from `ux-flows.md` | `apps/web/e2e/` |
| Mobile end-to-end | Maestro | Sign in, type, lesson, follow-up, upload, resume | `apps/mobile/.maestro/` |
| Visual | Playwright screenshots | Typing screen states, result card, both themes | `apps/web/e2e/visual/` |
| Accessibility | axe (Playwright) + manual VoiceOver/TalkBack pass per milestone | Contrast, labels, focus, live regions | web + mobile |
| Performance | Playwright + Event Timing API | Input-to-paint under 16 ms at p95 on a throttled CPU (4×) for a long passage | `apps/web/e2e/perf/` |
| Lesson quality | Eval script (40 passages, rubric) | Prompt or model changes | `functions/evals/` |

## Engine invariants (property tests)

- Typing the passage exactly gives 100% accuracy, zero errors, and every word `ok`.
- Every keystroke sequence produces a valid state; the caret is always within the passage plus extra letters.
- Backspace after a letter returns to the exact previous state.
- Accuracy is between 0 and 1; WPM is never negative; raw ≥ WPM.
- `lenient` accent rule never scores lower than `strict` on the same input.
- Normalization is idempotent: `normalize(normalize(x)) === normalize(x)`.
- Replaying a log on the server gives the same result as the live client state.

## Typing input matrix (manual + e2e)

| Input method | Browsers / devices |
|---|---|
| macOS US keyboard, Option dead keys (⌥e e → é) | Safari, Chrome, Firefox |
| macOS ABC Extended, long-press accent menu | Safari, Chrome |
| macOS French AZERTY | Chrome |
| Windows US-International dead keys | Chrome, Edge, Firefox |
| Windows French AZERTY | Edge |
| Canadian French (CSA) | Chrome |
| iOS keyboard long-press + accent bar | Plume app, Safari |
| Gboard (Android) long-press + accent bar | Plume app, Chrome |

Playwright covers composition with `compositionstart/update/end` events and `keyboard.insertText`.

## CI pipeline (GitHub Actions)

On every PR:
1. Install (pnpm, cached) → typecheck → lint → unit + property + golden tests (Turborepo caches unchanged packages)
2. Emulator job: rules tests + functions tests
3. Build web → deploy to a Firebase Hosting preview channel → Playwright smoke tests against it
4. Token contrast check (`packages/tokens`)
5. Comment the preview URL on the PR

On merge to `main`: deploy to `plume-dev` (web, functions, rules, indexes). EAS "preview" build for mobile when `apps/mobile` or shared packages change.

On a release tag: deploy to `plume-prod` after a manual approval; EAS production build + submit.

## Definition of done (every feature)

A feature is done when:
1. Its L3 spec status is **Built** and matches the code.
2. Tests at the right layers pass in CI, including rules tests for new data paths.
3. It works in both themes, with reduced motion, by keyboard (web), and with VoiceOver/TalkBack labels (mobile).
4. Empty, loading, error, and offline states exist.
5. Analytics events (if listed) fire without personal content.
6. The owner has seen it on a preview URL or build.
