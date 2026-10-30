# apps/mobile

Level: L2 Folder · Status: Review
Parent specs: `specs/1-experience/*`, `specs/1-system/tech-stack.md`

## Purpose

Plume for iOS and Android: the same loop as the web (type → result → lesson → follow-ups), plus library, uploads, history, stats, settings, and auth, built with Expo.

## Stack

Expo SDK (latest stable at M4) · Expo Router · React Native (New Architecture, Hermes) · TypeScript strict · TanStack Query · Zustand · Firebase JS SDK with React Native auth persistence · expo-speech · expo-document-picker · expo-file-system · expo-apple-authentication · Google Sign-In (`@react-native-google-signin/google-signin`) · expo-font · expo-haptics · react-native-reanimated (caret) · victory-native (charts) · react-native-markdown-display (HTML off) · Sentry (`@sentry/react-native`) · EAS Build/Submit/Update.

## Layout

```
app/                              Expo Router routes (map in information-architecture.md)
├── _layout.tsx                   providers: Firebase, Query, theme, fonts, Sentry
├── (tabs)/_layout.tsx            Type · Library · History · Profile
├── (tabs)/type/index.tsx         typing test → result/lesson stacked in the same screen
├── (tabs)/library/…              index, [bookId], upload
├── (tabs)/history/…              index, [sessionId]
├── (tabs)/profile/…              index (stats), settings
├── (auth)/…                      sign-in, sign-up, reset (modal)
└── welcome.tsx                   onboarding (modal)
src/
├── features/                     same feature split as web; L3 SPEC.md where mobile differs
│   ├── typing/                   ← L3: mobile input is very different from web
│   ├── listen/                   ← L3: expo-speech
│   ├── library/                  ← L3: document picker + upload
│   ├── lesson/  results/  history/  settings/  auth/   (follow the web L3 specs; differences noted below)
├── ui/                           RN components built on packages/tokens
└── lib/                          firebase.ts, api.ts, queries.ts (same contracts as web)
.maestro/                         end-to-end flows
app.config.ts, eas.json
```

## Differences from web (for features without their own mobile L3)

| Feature | Mobile difference |
|---|---|
| results | Chart in a collapsible "More stats" row; word review tap opens a bottom sheet with typed vs original |
| lesson | Follow-up box sticks above the keyboard (`KeyboardAvoidingView` / keyboard controller); haptic tick when a lesson finishes |
| history | Pull to refresh; swipe a row to delete the session (P1) |
| settings | One scrolling page; theme preview uses the native components |
| auth | Native Apple and Google sign-in sheets → `signInWithCredential`; anonymous guest same as web |

## Platform rules

- **Typing feel first:** the typing screen keeps the keyboard up, never jumps, and hits the latency goal on a mid-range Android phone (Pixel 6a class).
- **Orientation:** portrait on phones; both on tablets.
- **Dynamic Type / font scale:** respected up to 1.4× on all text except the passage, which has its own size setting.
- **Deep links:** `plume://` scheme plus universal/app links on the web domain (P1).
- **Updates:** EAS Update for JS-only fixes on the production channel; native changes go through store builds.
- **Store requirements:** Sign in with Apple offered alongside Google (Apple guideline 4.8); in-app account deletion (both stores); privacy labels match `security.md`.

## Done for this app

M4 "done" story in `roadmap.md` passes on an iPhone and an Android phone; Maestro flows pass in CI on simulators; TestFlight and Play internal builds exist.
