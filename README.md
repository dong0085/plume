# plume

Type a passage of French literature, then get a mini lesson on it.

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
```

After the lesson, type a question to ask Claude about the passage, press Enter for the next passage, or type `q` to quit.

Typing is relaxed about French typography: `'` matches `’`, `oe` matches `œ`, and quotes and dashes are optional. Accents count.

Books are cached in `~/.cache/plume/`.
