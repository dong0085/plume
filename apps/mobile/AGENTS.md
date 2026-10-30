# apps/mobile: agent notes

Read `apps/mobile/SPEC.md`. Features with mobile-specific behavior have their own L3 `SPEC.md` (typing, listen, library); the rest follow the web L3 specs plus the differences table in the L2 spec.

- Typing input comes from the hidden `TextInput` using the sentinel technique in `src/features/typing/SPEC.md`. Each value change becomes engine events.
- Only the current word re-renders per keystroke; words are memoized components. The caret and live stats run on Reanimated shared values.
- Firebase uses the JS SDK with React Native auth persistence, the same contracts as web (`src/lib/api.ts`).
- Styles come from the typed token object in `packages/tokens`.
- Test on a real mid-range Android phone after typing changes.
- Run Maestro flows with `pnpm --filter mobile e2e`.
- Native changes need a new EAS build; JavaScript-only fixes can ship through EAS Update.
