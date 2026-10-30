# packages/tokens

Level: L2 Folder · Status: Review
Parent specs: `specs/1-experience/design-system.md` · Values: `design/tokens.json` (exported from the Plume Design System artifact)

## Purpose

The design tokens (color per theme, type, space, radius, shadow, motion) in one source, built into what each platform needs.

## Layout

```
src/
├── tokens.json          source of truth (same shape as design/tokens.json)
├── themes/              one file per extra theme (P1), same token names
├── build.ts             generates the outputs below
└── check-contrast.ts    fails the build if any pair in design-system.md drops below its rule
dist/ (generated)
├── tokens.css           :root (Papier), [data-theme="encre"], [data-theme="papier"], prefers-color-scheme mapping
├── tailwind-preset.ts   Tailwind theme reading the CSS variables
└── index.ts             typed object for React Native: { themes: { encre, papier }, type, space, radius, motion }
```

## Rules

- Token names match `design-system.md` (`bg`, `surface`, `text-untyped`, `slip`, …). Components use names, never values.
- Every theme defines every color token; the build fails otherwise.
- The contrast check runs in CI for every theme, using the rules table in `design-system.md`.
- Fonts are not in this package. Web self-hosts Literata, Inter, and JetBrains Mono from `apps/web/public/fonts`; mobile bundles them with `expo-font`.
- Changing a value: edit `src/tokens.json`, run the build, and update the Design System artifact so the preview stays in step.
