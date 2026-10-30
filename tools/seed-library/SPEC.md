# tools/seed-library

Level: L2 Folder · Status: Review
Parent specs: `specs/0-product/features.md` (LIB-1, OPS-1), `specs/1-system/data-model.md`

## Purpose

An admin script that loads public-domain French books into `library/`. Run by the owner; never deployed.

## Usage

```
pnpm seed-library --project dev|prod|emulator [--only 14155,4650] [--dry-run]
```

## Input: `books.json`

The list of library books. It starts with the 17 books from the CLI (`apps/cli/plume.py` `BOOKS`), each verified as a French original:

```json
[{ "gutenbergId": 14155, "title": "Madame Bovary", "author": "Gustave Flaubert", "year": 1857,
   "blurb": "A doctor's wife in provincial Normandy dreams of a grander life.", "coverTint": "bordeaux" }]
```

## Steps per book

1. Download `https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt` (cache locally in `.cache/`); decode UTF-8, else Latin-1.
2. Check the header says `Language: French`; stop with an error otherwise.
3. `cutPassages` from `packages/core` (same code as uploads).
4. Write `library/{slug}` and its passages (batched), with `source: {type: "gutenberg", id}` and a credit line.
5. Print counts per size and compare with the last run (±5% warning).

`--dry-run` prints counts and five random passages per book without writing.

## Rules

- Uses a service account via Application Default Credentials; never commits keys.
- Respects Gutenberg's robot policy: one request at a time, cached downloads, a user agent with contact info.
- Idempotent: re-running updates in place (deterministic passage IDs).
