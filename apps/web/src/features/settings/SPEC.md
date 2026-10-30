# web/features/settings

Level: L3 Module · Status: Review
Parent: `apps/web/SPEC.md` · Features: SET-1, 3, 4, 5, ACC-8, 9, 11 (P1: SET-2, ACC-10)

## Settings store

- One store (Zustand) holding `Settings` from `packages/schema`, with defaults.
- Signed in: loads from `users/{uid}.settings`, writes back with a 500 ms debounce (`updateDoc` with only changed paths).
- Guest: `localStorage` key `plume.settings` (wrapped in try/catch). On sign-up, guest settings are written to the new profile.
- Per-device settings (voice) stay in `localStorage` only.
- Changes apply live everywhere (theme, font, caret) without reload.

## Page layout

Sections from `ux-flows.md` F7: Typing · Appearance · Listening · Lessons · Account. Wide screens: section list on the left, content on the right, scroll-spy. Narrow: one column with section headings.

Each row: label, one-line help, control. "Saved" toast (`--motion-base`) after each change, merged if changes come quickly.

## Live preview

Appearance section shows a sample passage line with letters in every state (correct, incorrect, slip, untyped, caret) using the current theme, font, and size.

## Theme application

- `appearance.theme = "system"`: follow `prefers-color-scheme` (Papier for light, Encre for dark) and update on change.
- Otherwise set `data-theme` on `<html>`.
- An inline script in `index.html` reads `localStorage` (or system) and sets `data-theme` before first paint.

## Tests

Guest settings persist across reloads; sign-up carries them over; theme switches without flash; debounce writes once for rapid changes.
