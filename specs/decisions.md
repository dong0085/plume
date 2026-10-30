# Decisions

Status: Review

Part 1 lists decisions made in this plan, with the reason. Part 2 lists decisions that belong to the owner, each with a recommendation. Coding starts once Part 2 is answered (or the recommendations are accepted).

## Part 1: Decisions made (ADR log)

| # | Decision | Why | Revisit if |
|---|---|---|---|
| D1 | One pnpm + Turborepo monorepo | Shared engine, schema, and tokens across web, mobile, server | Teams split |
| D2 | Web is a React + Vite SPA on Firebase Hosting | Client-heavy typing tool behind sign-in; simplest and fastest | SEO for many public pages becomes important |
| D3 | Mobile is Expo (React Native) | Shares TypeScript packages; EAS builds and store submission | Typing input latency on Android misses the target |
| D4 | Firebase JS SDK on mobile too | One Firebase API everywhere; works with Expo | A native-only Firebase feature is needed |
| D5 | Firestore + Storage + Functions in `northamerica-northeast1` | Lowest latency for the first users; data stays in Canada | Most users end up elsewhere |
| D6 | Server recomputes every result from the keystroke log | Trusted stats, bests, and future leaderboards | — |
| D7 | Lessons via streaming callable functions (SSE HTTPS fallback) | Built-in auth + App Check; text streams word by word | Streaming callables fall short on React Native |
| D8 | Claude `claude-opus-5-5`, effort `low`, server-side refusal fallback | Best lesson quality at a sensible cost | Ratings or cost say otherwise |
| D9 | Accents count by default; French typography is always forgiving | Learning value of accents; nobody should fail on `’` vs `'` | Feedback from learners |
| D10 | Uploaded books are private; no sharing | Copyright safety | Never, without legal review |
| D11 | Read aloud uses device voices (Web Speech API, expo-speech) | Free, instant, offline, same as the CLI | Too many devices lack French voices → SPK-5 |
| D12 | Passage text is copied into each session | Sessions survive book deletion and library changes | — |
| D13 | Visual identity is Plume's own ("ink on paper"), borrowing typing-test conventions, not any site's look | Distinct product; respects other designers' work | — |
| D14 | The Python CLI moves to `apps/cli` and stays standalone | It works today; no reason to tie it to accounts | Owner wants CLI sign-in and synced history |

## Part 2: Owner decisions needed

| # | Question | Recommendation | Why it matters |
|---|---|---|---|
| Q1 | **Lesson quotas and budget.** How many free lessons and follow-ups per day, and what monthly Claude spend cap? | 5 lessons + 20 follow-ups per day; $150/month cap to start (≈ 150–300 active users) | Claude is the main running cost (~$0.025 per lesson on Opus 5.5) |
| Q2 | **Cheaper model for small tasks.** OK to use `claude-haiku-5-5` for tap-a-word meanings (LES-7, P1) while lessons stay on Opus 5.5? | Yes for word meanings only | ~40× cheaper per call for a short, simple task |
| Q3 | **Paid plan.** Free only at launch, or a paid tier with higher quotas? | Free at launch; decide after 2 months of usage data | Changes M5 scope (billing, App Store in-app purchase rules) |
| Q4 | **Name and domain.** Keep "Plume"? Which domain? | Keep Plume; check `plume.app`, `plume.study`, `typeplume.com`, `plume-fr.app` | Needed for auth domains, App Store listing, email sender |
| Q5 | **Developer accounts.** Apple Developer Program ($99/yr) and Google Play Console ($25 once) for M4 | Yes, register before M4; Apple can take days to verify | Blocks mobile release |
| Q6 | **Upload limits.** 20 books per account, 25 MB each? | Yes | Storage and processing cost; abuse |
| Q7 | **Library growth.** Which books after the first 17? | Add 30 more across eras: Molière, Maupassant (short stories, great for short passages), Daudet, Hugo (more), Zola (more), Sand, Mérimée, Perrault, La Fontaine, Balzac | Variety and level range; short stories suit beginners |
| Q8 | **UI language.** English only at launch? | English at launch; French UI as an option in P1 (good for advanced learners) | i18n setup cost |
| Q9 | **Analytics.** Use Google Analytics for Firebase (P1)? | Yes, with no personal content, and a cookie/consent banner for EU visitors | Product learning vs privacy |
| Q10 | **Sign-in providers.** Email, Google, Apple, guests. Add Microsoft or GitHub? | No extras at launch | Each provider adds setup and support |
| Q11 | **Timeline.** Is the M0–M5 plan (about 10 weeks of focused work) the right pace? | Yes; web reaches people at M2 (~5 weeks) | Sets expectations |
| Q12 | **Repo.** Build in this repo (`dong0085/plume`, private), moving `plume.py` to `apps/cli/`? | Yes | One home for CLI, web, mobile, specs |
