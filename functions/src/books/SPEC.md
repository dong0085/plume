# functions/books: ingestBook, deleteBook, sweepStaleUploads

Level: L3 Module · Status: Review
Parent: `functions/SPEC.md` · Features: LIB-4–8 (P1: LIB-5, 10) · Flow: `specs/1-experience/ux-flows.md` F5

## ingestBook (Storage `onObjectFinalized`, path `uploads/{uid}/{bookId}/original.*`)

1. Parse `uid`, `bookId` from the path. Load `users/{uid}/books/{bookId}`; if missing or not `uploading`, delete the object and stop (orphan).
2. Set `status: "processing", statusStep: "reading"`.
3. Checks: size ≤ 25 MB (`too_large`); the user's ready+processing book count ≤ limit (`limit`), content sniffing matches the extension (`unsupported`).
4. **Read text** by format:
   - **EPUB:** unzip (`jszip`); if `META-INF/encryption.xml` lists encrypted content documents → `drm`. Read `content.opf`: metadata (title, creator, language), spine order. For each spine item, parse XHTML (`htmlparser2`): take text from `p`, `div` (leaf), `blockquote`, headings as chapter titles; skip `nav`, footnotes (`epub:type="footnote"`, `aside`), scripts, styles. Paragraph boundaries become blank lines. Chapter list from headings / `nav` (P1).
   - **TXT:** detect encoding (`chardet`: UTF-8, Windows-1252, ISO-8859-1, UTF-16 with BOM), decode, normalize line endings.
   - **PDF (P1):** `pdfjs-dist` text items → lines → paragraphs by vertical gaps; skip headers/footers repeated on most pages; if under 1,000 characters of text, `no_text` (scanned PDF).
5. `statusStep: "cutting"`: `cutPassages` from `packages/core` (per chapter for EPUB). Zero passages in every size → `no_text`.
6. `statusStep: "checking"`: `frenchScore` on a sample of passages → `langScore`. Below 0.35 → still `ready`, with `langScore` stored (the client shows the warning). EPUB `dc:language` other than `fr*` lowers the score by 0.2.
7. Write passages in batches of 400 (IDs `{size}-{order}`, `rand = Math.random()`), at most 20,000.
8. Update the book: `status: "ready"`, title/author from metadata if the person hasn't edited them, `passageCounts`, `chapters` (P1), `sha256` (computed here, authoritative), `updatedAt`.
9. Any thrown error → `status: "failed"`, `failReason: "parse_error"` (or the specific reason), log with the book's format and size only.

Idempotent: re-running on the same file overwrites the same passage IDs.

## deleteBook

Owner only. Delete passages (batched, `recursiveDelete` on the subcollection), the Storage object, then the book doc. If `settings.source.bookId` points to it, reset the source to `all`.

## sweepStaleUploads (daily)

Books stuck in `uploading` for over 24 h or `processing` for over 1 h → delete Storage object and doc (uploading) or mark `failed: parse_error` (processing).

## Fixtures

`test/fixtures/`: small public-domain EPUB (3 chapters), EPUB with `encryption.xml`, broken zip, Latin-1 TXT, UTF-16 TXT, English TXT, image-only PDF (P1), 26 MB file.
