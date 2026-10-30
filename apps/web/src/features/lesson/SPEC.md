# web/features/lesson

Level: L3 Module · Status: Review
Parent: `apps/web/SPEC.md` · Features: LES-1, 2, 3, 5, 6, 9 (P1: LES-4, 7, 8; HIS-5)
Server side: `functions/src/lessons/SPEC.md`

## Components

| Component | Job |
|---|---|
| `LessonView` | Shows the lesson: streaming text while generating, saved text when ready |
| `ChatThread` | Follow-up questions and answers after the lesson |
| `FollowUpBox` | Multi-line input; Enter sends, Shift+Enter new line; 1,000-character limit with a counter after 800 |
| `SuggestedQuestions` (P1) | Chips that fill and send a question |
| `LessonFeedback` | 👍 / 👎, then an optional note field on 👎 |
| `QuotaBadge` | "7 lessons left today"; amber at ≤ 2; at 0: "Lessons reset at 00:00" (local time) |
| `GuestLessonTeaser` | For guests: the five section headings blurred + Sign up button |

## Streaming

`useLessonStream(sessionId)`:
1. Read the session doc (live listener).
2. `lesson.status`:
   - `ready` → render `messages[0]`
   - `generating` and started under 90 s ago → show "Writing your lesson…" and wait for the listener
   - `none` or stale `generating` → call `lesson` (streaming callable); append chunks to local text
3. On the final message: update quota in the query cache.
4. On error: keep any text received; show the matching message from `api.md` with **Retry**.

`useFollowUp(sessionId)` does the same for one question: shows the question at once (pending style), streams the answer under it, and on failure removes the pending pair and puts the question back in the box.

Rendering: Markdown with raw HTML off. Headings use `--type-h2`. Quotes from the passage (`>` blocks and *italic French*) use Literata. The stream re-renders at most every 50 ms (batched) to stay smooth on long lessons. New blocks fade in (`--motion-fast`).

## Behavior

- After the lesson finishes, focus moves to `FollowUpBox` (unless the person already moved focus). Tab+Enter still means "next passage" when focus is not in the box.
- `truncated` lessons show "Continue" which sends "Please finish the lesson." as a follow-up (free, not counted).
- `refusal` shows "This lesson couldn't be written for this passage." with Next passage.
- Quota exhausted before the lesson: lesson area shows the reset time; the result and word review stay.
- Follow-ups disabled at 60 messages: "This session is full. Start a new passage to keep going."

## Accessibility

- Lesson region is a polite live region only while streaming starts ("Lesson started"), then announces "Lesson ready" once (not every chunk).
- Chat messages are a list with "You asked" / "Tutor" labels for screen readers.

## Tests

Fake streaming callable in tests: chunks, slow chunks, error mid-stream, quota error, refusal, truncated. Check that a reload mid-stream shows the saved lesson once the server finishes.
