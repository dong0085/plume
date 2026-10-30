# Vision

Level: L0 Product · Status: Review

## One line

Learn French by typing the great French books, with a patient tutor beside you.

## The problem

People learning French hit three walls:

1. **Textbook French is thin.** Real literature is rich, but a page of Flaubert alone is too hard to use.
2. **Accents and spelling stay fuzzy.** Reading lets you skip over `é` vs `è`. Writing forces you to know.
3. **Help is far from the text.** Looking up each word, tense, and reference breaks the flow.

Typing a passage makes you notice every letter. A lesson right after it explains what you just wrote, while it is fresh.

## Who it is for

| Person | What they want | What Plume gives them |
|---|---|---|
| **Adult learner, A2–B2** (the main user) | Steady progress, real texts, less dull drilling | Short daily rounds: type, learn, ask |
| **Typing enthusiast** | A good typing test with something new to type | A fast, Monkeytype-style test with French literature as the content |
| **Advanced reader, C1+** | Close reading of favourite books | Upload their own books; deep follow-up questions |
| **Teacher** (later) | Material for a class | Shared reading lists and class progress (P2) |

## What people do in Plume

1. **Type** a passage from a classic French novel or from their own book.
2. **See** each word marked right, wrong, or an accent slip, plus speed and accuracy.
3. **Learn** from a short lesson: translation, key words, grammar, book context, typing tips.
4. **Ask** follow-up questions in the same conversation.
5. **Listen** to the passage read aloud, normally or slowly, or type it as a dictée.
6. **Return** to any past session, and watch their stats and streak grow.

## Product principles

1. **The text comes first.** The typing screen is calm and spare. Everything else waits until the test ends.
2. **Feedback is exact and kind.** Every mark on the screen is precise. Every lesson is warm.
3. **Accents matter, French typography does not.** `'` for `’` and `oe` for `œ` always pass. Accents count by default, with a lenient mode for beginners.
4. **Real books, honest sources.** Passages come from real texts, never made up. Each passage shows its book and author.
5. **Your books stay yours.** Uploaded books are private to the person who uploaded them.
6. **Fast on every device.** The typing test feels instant on a laptop and on a phone.
7. **Simple language.** Plain words in the UI and in lessons, matched to the learner's level.

## Goals for the first public release

| Goal | Measure | Target |
|---|---|---|
| People finish the core loop | Share of started tests that reach a lesson | 60% or more |
| People come back | Share of new users active on day 7 | 25% or more |
| Lessons feel useful | Thumbs up on lessons | 80% or more |
| The typing feels great | Input-to-paint delay on a mid-range laptop and phone | under 16 ms (one frame) |
| AI cost stays in budget | Average Claude cost per active user per month | Within the budget set in `decisions.md` |

## Out of scope for the first public release

These ideas are good. They come later and are listed in `features.md` as P2:

- Languages other than French
- Classrooms and teacher dashboards
- Public sharing of uploaded books
- Paid plans and billing
- Offline lessons

## Where it starts

Plume starts as a Python CLI (`apps/cli`) that already does the core loop: random passage → type → word marks → streamed Claude lesson → follow-up questions → saved sessions → read aloud. The web and mobile apps carry that loop to everyone, and add accounts, uploads, and a Monkeytype-grade typing experience.
