# web/features/auth

Level: L3 Module · Status: Review
Parent: `apps/web/SPEC.md` · Features: ACC-1–9, 11 · Security: `specs/1-system/security.md`

## Pieces

| Piece | Job |
|---|---|
| `AuthProvider` | Subscribes to `onAuthStateChanged`; exposes `user`, `isGuest`, `isVerified`, `profile` |
| `ensureGuest()` | On first visit, signs in anonymously (silent) so guests can call `nextPassage` and `finishTest` |
| `SignUpPage` / `SignInPage` | Google, Apple, email + password; links from guest when a guest is signed in |
| `ResetPage` | Sends the reset email; always says "If an account exists, we sent a link" |
| `VerifyBanner` | Shown to unverified email accounts; "Resend email" |
| `WelcomeFlow` | Onboarding steps from `ux-flows.md` F2: level → voice check → accent rule |
| `RequireAccount` | Route guard: guests see a sign-up prompt in place of the page |
| `DeleteAccountDialog` | Typed confirmation, re-auth if needed, calls `deleteAccount` |

## Guest → account

- Sign-up while anonymous uses `linkWithCredential` / `linkWithPopup` so the `uid` stays the same and guest sessions stay.
- If the credential already belongs to another account (`auth/credential-already-in-use`): sign into that account instead and tell the person "Signed in to your existing account. Tests from this visit weren't added." (Guest data is small; merging is out of scope.)
- After linking: create `users/{uid}` if missing (whitelisted fields, `onboarded: false`) and go to `/welcome`.

## Providers

- Google: popup on desktop, redirect on mobile browsers.
- Apple: Sign in with Apple via Firebase OAuth provider (`apple.com`), requesting name and email.
- Email: password ≥ 8 characters; send verification email on sign-up.

## Profile creation

On the first signed-in load with no `users/{uid}` doc, the client writes it with defaults from `packages/schema` (`defaultSettings`), `level: "B1"`, `onboarded: false`. Rules allow only these fields.

## Tests

Emulator-backed E2E: guest types → signs up with email → session still in history; existing-account collision message; reset flow; delete account removes data (check Firestore and Storage emulators).
