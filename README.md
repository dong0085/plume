# plume

Type a passage of French literature, then get a mini lesson on it.

> **Coming next:** Plume is growing into a web app and an iOS/Android app with accounts, your own uploaded books, and a full typing-test experience. The plan lives in [`specs/`](specs/README.md); start there. This README covers the current Python CLI.

`plume` picks a random passage from a classic French novel (Flaubert, Hugo, Zola, Verne, Dumas, Voltaire, Proust, and more, via Project Gutenberg). You type it out, see which words and accents you got right, and Claude gives you a short lesson: an English translation, key vocabulary, a grammar point from the passage, context on the book, and tips on your typing mistakes. Ask follow-up questions as long as you like.

## Setup

Requires [uv](https://docs.astral.sh/uv/). The script installs its own dependencies on first run.

```sh
chmod +x plume.py
ln -s "$PWD/plume.py" ~/.local/bin/plume
```

Lessons come from Claude, using either:

- the Claude API, when `ANTHROPIC_API_KEY` is set, or
- the [Claude Code](https://claude.com/claude-code) CLI (`claude`), which uses your Claude subscription.

## Usage

```sh
plume                          # random passage, B1 level
plume --level "beginner (A2)"  # tune the lesson to your level
plume --size short             # short / medium / long passages
plume --book verne             # only books whose title or author matches
plume --list                   # list all books
plume --resume                 # reopen your most recent session
plume --history                # choose a past session to reopen
plume --voices                 # list installed French voices
plume --voice amélie           # pick a voice for listening
```

While a passage is showing, type `/s` (or `/skip`) to skip it and get a different one.

After the lesson, type a question to ask Claude about the passage, press Enter for the next passage, or type `q` to quit.

## Listening

At any prompt, type `/l` to hear the passage read aloud, or `/slow` to hear it slowly. Type the same command again to stop. Listening uses the macOS `say` command and picks your best French voice automatically: Premium, then Enhanced, then the rest. Install better voices in System Settings → Accessibility → Spoken Content → System Voice → Manage Voices.

## Notes

Typing is relaxed about French typography: `'` matches `’`, `oe` matches `œ`, and quotes and dashes are optional. Accents count.

Every session (passage, typing result, lesson, and questions) is saved automatically. Resuming one shows the passage and last answer again so you can keep asking questions.

Books and sessions are stored in `~/.cache/plume/`.
