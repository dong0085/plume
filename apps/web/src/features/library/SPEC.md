# web/features/library

Level: L3 Module · Status: Review
Parent: `apps/web/SPEC.md` · Features: LIB-1, 2, 3, 4, 6, 7, 8 (P1: LIB-5, 9, 10, 12)
Server side: `functions/src/books/SPEC.md`

## Components

| Component | Job |
|---|---|
| `LibraryPage` | Tabs Classics / My books; grid of `BookCard`; search (P1) |
| `BookCard` | `BookCover` + title + author + year or status chip |
| `BookCover` | Generated cover: tinted card (`coverTint`), title in Literata, author in Inter small caps; deterministic per book |
| `BookPage` | Details, passage count, your stats on this book, actions |
| `UploadDialog` | Drop zone, file input, rules, rights note, progress steps |
| `EditBookDialog` | Title and author fields |
| `DeleteBookDialog` | Confirmation: "Delete *{title}*? Your sessions keep their passages." |

## Upload flow (client side)

1. Validate locally: extension `.epub`/`.txt` (P1 `.pdf`), size ≤ 25 MB, account email verified, under the book limit. Show the exact problem otherwise.
2. Compute SHA-256 in a Web Worker (keeps typing smooth). Check `users/{uid}/books` for the same `sha256`; if found, link to it.
3. Create `users/{uid}/books/{bookId}` with `status: "uploading"`, title from the file name (EPUB metadata replaces it later).
4. Upload to `uploads/{uid}/{bookId}/original.{ext}` with a resumable upload; show percent.
5. Listen to the book doc: `processing` steps → `ready` (show passage count, "Type from this book") or `failed` (show `failReason` message from `ux-flows.md` F5, with Delete).
6. `not_french` warning: the book is `ready` with `langScore` low; show "This book doesn't look French. Use it anyway?" with Keep / Delete.

Closing the dialog during upload keeps it going in the background with a small progress pill in the top bar.

## Source selection

"Type from this book" sets `settings.source = {type: "book", bookId}` and goes to `/`. The config bar's source menu lists: All classics · My books (all) · each book (recent first).

## Tests

E2E with emulators: upload a small EPUB fixture → ready → type from it; failed DRM fixture shows the right message; delete removes the card and the Type source falls back to All classics.
