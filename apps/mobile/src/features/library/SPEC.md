# mobile/features/library

Level: L3 Module · Status: Review
Parent: `apps/mobile/SPEC.md` · Same behavior as `apps/web/src/features/library/SPEC.md` except where noted · Features: LIB-1–4, 6–8

## Differences from web

- **Pick a file:** `expo-document-picker` with types `application/epub+zip`, `text/plain` (P1 `application/pdf`); `copyToCacheDirectory: true`.
- **Share into Plume (P1):** iOS share extension / Android share intent for `.epub` and `.txt` opens the upload screen with the file.
- **Hash:** SHA-256 with `expo-crypto` on the file in chunks (no full-file string in memory).
- **Upload:** Firebase Storage `uploadBytesResumable` from a Blob made with `fetch(fileUri).blob()`; progress shown; continues while the app is open; if the app goes to background, the upload pauses and resumes on return (the book doc stays `uploading`; a stale `uploading` doc older than 24 h is cleaned up by `ingestBook`'s scheduled sweep).
- **Grid:** two columns of `BookCard` on phones, four on tablets; Classics / My books as a segmented control at the top.
- **Delete:** swipe on a book card or the button on the book page; same confirmation text.

## Tests

Maestro: pick a fixture EPUB from the simulator's files → processing → ready → Type from this book.
