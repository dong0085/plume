# packages/schema

Level: L2 Folder · Status: Review
Parent specs: `specs/1-system/data-model.md`, `specs/1-system/api.md`

## Purpose

One definition of every stored document and every function payload, as **zod** schemas, with TypeScript types inferred from them. Web, mobile, and functions all import from here, so a shape change is one edit that the compiler checks everywhere.

## Layout

```
src/
├── firestore/
│   ├── book.ts          LibraryBook, UserBook, BookStatus, FailReason
│   ├── passage.ts       Passage, PassageSize
│   ├── user.ts          UserProfile, Settings (with defaults), Level
│   ├── session.ts       Session, Result, LessonState, ChatMessage, TestConfig
│   ├── stats.ts         Stats, ModeKey
│   ├── usage.ts         UsageDay
│   └── words.ts         SavedWord (P1)
├── api.ts               input/output schemas for every callable in api.md
├── converters.ts        Firestore data converters (timestamps ↔ Date), SDK-agnostic
├── defaults.ts          defaultSettings, limits (upload size, quotas fallback)
└── index.ts
```

## Rules

- Schemas match `data-model.md` field for field. When they differ, update `data-model.md` in the same PR.
- `Settings` has `.default()` for every field, so old user docs gain new settings safely.
- Function inputs use `.strict()` (unknown keys rejected). Stored docs use `.passthrough()` on read (forward compatible) and `.strict()` on write.
- Converters work with both the web/mobile Firebase SDK and `firebase-admin` by taking a tiny timestamp adapter.
- No runtime dependencies except `zod`.

## Tests

Round-trip each schema with example docs from `data-model.md`; reject the invalid examples listed in `firebase/test/` rules tests.
