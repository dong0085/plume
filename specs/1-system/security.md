# Security, privacy, and rights

Level: L1 System · Status: Review

## Authentication

- Firebase Auth with email/password, Google, Apple, and anonymous (guest) accounts.
- Email accounts must verify their email before uploading books. Lessons work before verification so the first-run experience stays smooth; quota still applies.
- Guests use anonymous accounts. Linking keeps the same `uid`, so guest tests become the person's history.
- Sensitive actions (delete account, change email or password) need a sign-in within the last 5 minutes.
- Password rules: at least 8 characters; Firebase password policy turned on; email enumeration protection on.

## Authorization: Firestore rules (outline)

```
library/**                          read: true; write: false
users/{uid}                         read: owner
                                    create: owner, only whitelisted fields, plan absent
                                    update: owner, only displayName, level, onboarded, settings (shape-checked)
users/{uid}/books/{bookId}          read: owner
                                    create: owner, status == "uploading", only title/author/format/sizeBytes/createdAt
                                    update: owner, only title, author
                                    delete: false (use deleteBook)
users/{uid}/books/{b}/passages/**   read: owner; write: false
users/{uid}/sessions/{s}            read: owner
                                    update: owner, only lesson.feedback
                                    create/delete: false (server only)
users/{uid}/words/{w}               read/write: owner, shape-checked (P1)
users/{uid}/private/**              read: owner (stats only); write: false
usage/{uid}/**                      read: owner; write: false
everything else                     deny
```

`owner` means `request.auth.uid == uid`. Rules are tested with the emulator (`testing.md`).

## Authorization: Storage rules (outline)

```
uploads/{uid}/{bookId}/{file}   create: owner, email verified (or a provider that verifies email),
                                        size ≤ 25 MB, contentType in [application/epub+zip, text/plain, application/pdf],
                                        no overwrite
                                read: owner; delete: false (server only)
exports/{uid}/**                read: owner; write: false
tts/**                          read: signed in; write: false (P2)
```

## App Check

Enforced on Functions, Firestore, and Storage from M5. In dev it runs in monitor mode with debug tokens for local and CI.

## Abuse and cost controls

- Lesson and follow-up quotas per user per day (`ai-lessons.md`), counted on the server in a transaction before calling Claude.
- Global daily spend guard: if the day's total Claude cost passes the limit in Remote Config, new lessons pause with a friendly message and an alert goes out.
- Functions `maxInstances` caps per function.
- Upload limits: 25 MB per file, 20 books per account, 5 uploads per hour.
- `nextPassage`: 120 calls per minute per user.

## AI safety and prompt injection

- Passage text, book titles, and questions are **data**. The prompt puts the passage inside `<passage>` tags and the system prompt says to treat it as text to explain, not instructions.
- Uploaded books are the main injection risk (a book could contain "ignore your instructions"). The same tagging covers it, and lessons have no tools or side effects, so the worst outcome is an off-topic lesson.
- The tutor stays on French learning. Off-topic questions get a short, kind redirect.
- Claude's `refusal` stop reason is handled: the session shows "This lesson couldn't be written for this passage." and quota is refunded.
- Lesson Markdown is rendered without raw HTML (no `dangerouslySetInnerHTML`; a Markdown renderer with HTML off), so model output cannot inject script.

## Web hardening

- Firebase Hosting headers: strict Content-Security-Policy (self, Firebase, Google sign-in, Apple sign-in, Sentry, reCAPTCHA), `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` limited.
- No secrets in client code. The Anthropic key exists only in Secret Manager and is read by the lesson functions.
- Dependabot and `pnpm audit` in CI.

## Privacy

- Data kept: account email and name, settings, sessions (passage copy, result, keystroke log, lesson, chat), uploaded books, stats, usage counts.
- Purpose: running the app. No selling or ad tracking.
- Logs and analytics never contain passage text, book text, questions, or lessons.
- Claude API: requests contain the passage, the result summary, the level, and the chat. Anthropic API terms apply; state this in the privacy policy.
- Deletion: delete account removes everything within minutes (`deleteAccount`). Deleting a book removes its file and passages; sessions keep their short passage copy until the session or account is deleted.
- Export (P1): JSON of all personal data.
- Laws: the owner is in Canada (PIPEDA); the policy also covers GDPR basics (access, deletion, export) for EU users. Have the privacy policy and terms reviewed before launch.

## Rights to uploaded books

- Uploaded books are private to the uploader. There is no feature to share, publish, or browse other people's books.
- Upload screen and Terms: people upload only books they have the right to use.
- DRM-protected EPUBs are rejected, not decrypted.
- Library books come only from the public domain (Project Gutenberg). The seed tool strips Gutenberg boilerplate and keeps a credit line on each book page, as Gutenberg's license allows for public-domain texts.
