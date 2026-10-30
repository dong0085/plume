# UX flows

Level: L1 Experience · Status: Review

Each flow lists the steps, what the system does, and the edge cases to handle. Feature IDs in brackets.

---

## F1. First visit as a guest [ACC-5, TYP-*, RES-*]

1. Person opens plume.app. A short hero sits above the test: "Type the great French books. Learn as you go." The caret blinks in the passage.
2. They start typing. The hero and nav fade (focus mode).
3. The test ends (passage done or timer ends). The result card slides up in place of the text.
4. Below the result: the lesson section shows its five headings, blurred, with **"Sign up free to read your lesson"**.
5. Choices: **Sign up**, **Next passage** (Tab+Enter), **Listen**.

**Edge cases**
- Keyboard layout lacks accents → a small hint under the text the first time an accent slip happens: "Tip: hold a letter or use ⌥ + e for é" (text adapts to OS).
- Mobile web → shows the accent bar above the keyboard and a banner offering the app.
- Guest finishes 3 tests → gentle prompt to sign up to save progress (dismissible, at most once per day).

## F2. Sign up and onboarding [ACC-1–3, 6, 7]

1. Sign-up page: Google, Apple, or email + password. Guest tests are kept and linked to the new account.
2. Email sign-ups get a verification email. They can keep using Plume; a banner reminds them to verify.
3. **Welcome step 1, your level:** six cards A1–C2 with plain descriptions ("A2: I can read simple texts slowly"). Also "Not sure? Start at B1."
4. **Step 2, listening:** "Hear a sample" plays a sentence with the best French voice found. Picker if there are several. If none: explain how to add a French voice on this device, or skip.
5. **Step 3, accents:** choose strict (recommended for B1+) or lenient (recommended for A1–A2). Shows the result of a mini example.
6. Land on the typing test with a short passage chosen for the level.

**Edge cases**
- Sign-up with an email that already exists via Google → offer sign-in with Google.
- If the guest had a result on screen when signing up, return to it and start the lesson.

## F3. Core loop: type, learn, ask [TYP-*, RES-*, LES-1–6, 9]

1. Typing screen with the config bar: `passage | time 15 30 60 120` · `short medium long` · `accents: strict/lenient` · `source: all classics ▾`.
2. Person types. Live WPM and accuracy (or the timer) above the text.
3. End of test:
   - Result card: WPM, accuracy, raw, consistency, time, character breakdown, chart (web).
   - Per-word review: each word marked; hover or tap shows "typed / original".
   - The session saves (URL becomes `/s/:id`).
4. Lesson streams in under the review. A small badge shows lessons left today ("7 left today").
5. Follow-up box: "Ask about this passage…" with suggested chips (P1). Answers stream into the chat.
6. Thumbs up/down under the lesson.
7. **Next passage** (Tab+Enter) or **Type it again**.

**Edge cases**
- Lesson fails or stops early → "The lesson stopped early. Retry" (does not count against quota) [LES-9].
- Quota reached → result still shows; lesson area says when the quota resets. Follow-ups on older sessions still allowed up to a separate follow-up quota (see `1-system/ai-lessons.md`).
- Offline at test end → result shows; session saves when back online (Firestore offline cache); lesson waits with "Waiting for connection".
- Person leaves mid-stream → the server finishes the lesson and saves it; resuming later shows it complete.
- Test abandoned (restart before finishing) → not saved, not counted.
- Time mode with very short input (under 5 words) → result shown, no lesson offered (nothing to teach), not saved to history.

## F4. Listen and dictée [SPK-1–4, TYP-12]

**Listen**
1. Listen button beside the book line (or Ctrl/Cmd + L, or `/l` habit from the CLI shown in the shortcut list).
2. Audio plays with the chosen voice. Button becomes Stop. A second button: Slow.
3. Typing while listening works. Audio stops when the test ends or restarts.

**Dictée (P1)**
1. Choose `dictée` in the mode bar. The passage text is hidden behind a soft blur; word slots show only the length of each word.
2. The passage plays sentence by sentence. Replay sentence: Ctrl/Cmd + R or button.
3. On finish, the text is revealed with marks. Scoring counts accent slips and spelling separately.

**Edge cases**
- No French voice on the device → listen button shows a tooltip with how to add one (per OS); dictée mode disabled with the same help.
- Voice list loads late (Chrome) → picker waits for the `voiceschanged` event.

## F5. Upload a book [LIB-4, 6–8]

1. Library → My books → **Upload a book**. Drop zone + file picker. Accepts `.epub` and `.txt` (P1: `.pdf`). Up to 25 MB.
2. Rights note under the drop zone: "Upload only books you have the right to use. Your books are private to you."
3. Upload progress bar → "Processing…" with steps: reading file → finding passages → checking language.
4. Ready: book card shows title, author (from EPUB metadata, editable), passage count. **Type from this book**.
5. Failure states with plain reasons:
   - "This EPUB is protected (DRM) and can't be read."
   - "We couldn't find enough French text in this file."
   - "This file is too large (max 25 MB)."
   - "This file type isn't supported yet."

**Edge cases**
- Book looks non-French → "This book doesn't look French. Use it anyway?" (Yes keeps it, flagged.)
- Duplicate upload (same file hash) → "You already uploaded this book" with a link.
- Upload limit per account (see `decisions.md`) → message with the limit and the option to delete a book.
- Person leaves during processing → it continues on the server; status updates when they return.

## F6. History and resume [HIS-1, 2]

1. History: list grouped by day. Each row: time, book, first words of the passage, WPM, accuracy, question count.
2. Filters: book, mode, has lesson. Search the passage text (P1).
3. Open a row → session page: result, review, lesson, chat. Follow-up box ready.
4. Actions: **Type this passage again**, **Next passage from this book**, **Listen**.

## F7. Settings [SET-*, ACC-9, 11]

Sections:
- **Typing:** default mode and length, accent rule, punctuation rule (P1), stop on error (P1), confidence mode (P1), live stats on/off, caret style, smooth caret, focus mode, sounds (P1).
- **Appearance:** theme (system / Encre / Papier / more), typing font, text size, reduced motion (system default).
- **Listening:** voice (French voices only, best first), speed, sample button.
- **Lessons:** level, "more French in lessons" (P1).
- **Account:** name, email, password, linked sign-ins, export data (P1), delete account (typed confirmation).

All changes save instantly, with a small "Saved" toast.

## F8. Delete account [ACC-9]

1. Settings → Account → Delete account.
2. Explain what will be deleted: books, sessions, words, stats. Type `DELETE` to confirm. Re-authenticate if the last sign-in was more than 5 minutes ago.
3. Server deletes Storage files, Firestore data, then the Auth user. Person is signed out to `/` with a goodbye message.

---

## Empty, loading, and error states (all screens)

| State | Pattern |
|---|---|
| Empty | One friendly line + one action. History empty: "Your sessions will appear here." **Type your first passage** |
| Loading | Skeleton shapes matching the content. Typing screen preloads the next passage so restart is instant |
| Error | Plain words, what to do next, and a Retry. Never show raw error codes; log them |
| Offline | Thin banner: "Offline. Your typing still works; lessons wait for the connection." |
