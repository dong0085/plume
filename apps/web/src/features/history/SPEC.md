# web/features/history

Level: L3 Module · Status: Review
Parent: `apps/web/SPEC.md` · Features: HIS-1, 2, 3 (P1: HIS-3 charts, 4, 7; RES-6)

## History page

- Query `users/{uid}/sessions` ordered by `createdAt` desc, 30 per page, infinite scroll.
- Grouped by local day ("Today", "Yesterday", then dates).
- Row: time · book title · first 60 characters of the passage (Literata italic) · WPM · accuracy · 💬 question count. Whole row is a link to `/s/:id`.
- Filters (query params): book, mode, "has questions". Search passage text (P1, client-side over loaded pages first).
- Empty state: "Your sessions will appear here." with **Type your first passage**.

## Session page (`/s/:sessionId`)

Composes `results` + `lesson` features for a saved session:
- `ResultCard`, `SpeedChart`, `WordReview` from the saved result
- `LessonView` + `ChatThread` + `FollowUpBox` (resume = keep asking)
- Actions: Type this passage again (same passage, new test), Next passage from this book, Listen
- Not found or not the owner → friendly not-found page

## Stats page

From `users/{uid}/private/stats`:
- P0: four numbers: tests, time typed, average WPM (`wpmSum / tests`), best WPM (max across `best`); accuracy average; slips per test.
- P1: WPM and accuracy trend (last 100 sessions, uPlot), accent heatmap (`accents` map: miss rate per letter as a grid colored from `--surface-2` to `--slip`), calendar heatmap (`days`), personal bests table by mode key, streak.

## Tests

Pagination and grouping across time zones (UTC vs America/Toronto); resume a session and send a follow-up; stats numbers from a fixture stats doc.
