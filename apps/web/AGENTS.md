# apps/web: agent notes

Read `apps/web/SPEC.md`, then the `SPEC.md` of the feature you work on in `src/features/`.

- The typing surface updates the DOM directly from the engine state held in a ref. React renders the passage once per test. Keep per-keystroke work inside `features/typing`.
- Typing input arrives through the hidden textarea as `beforeinput` and `compositionend` events. Keyboard layouts and dead keys work through those two paths.
- Server data flows through TanStack Query; live docs (session, book status) feed the cache through Firestore listeners.
- Settings go through the settings store, which syncs to Firestore for signed-in people and to `localStorage` for guests.
- Styling uses Tailwind classes backed by token variables from `packages/tokens`.
- Lesson Markdown renders with raw HTML turned off.
- Every route has an error boundary with a friendly message and a Sentry report.
- Check the bundle budget (180 KB gzipped JS for `/`) when adding dependencies; load heavy parts lazily.
- Run `pnpm --filter web e2e` for flows and `pnpm --filter web e2e:perf` after touching the typing surface.
