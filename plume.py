#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = ["anthropic", "rich"]
# ///
"""plume — type a passage of French literature, then get a mini lesson on it."""

import argparse
import difflib
import json
import os
import random
import re
import readline  # noqa: F401  (gives input() arrow keys and history)
import shutil
import subprocess
import sys
import time
import unicodedata
import urllib.request
from pathlib import Path

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

# Public-domain French originals on Project Gutenberg: (id, title, author)
BOOKS = [
    (14155, "Madame Bovary", "Gustave Flaubert"),
    (4650, "Candide, ou l'optimisme", "Voltaire"),
    (4647, "Zadig, ou la Destinée", "Voltaire"),
    (798, "Le Rouge et le Noir", "Stendhal"),
    (5711, "Germinal", "Émile Zola"),
    (800, "Le Tour du monde en quatre-vingts jours", "Jules Verne"),
    (4791, "Voyage au centre de la Terre", "Jules Verne"),
    (14287, "L'Île mystérieuse", "Jules Verne"),
    (5097, "Vingt mille lieues sous les mers", "Jules Verne"),
    (17989, "Le Comte de Monte-Cristo, tome I", "Alexandre Dumas"),
    (13951, "Les Trois Mousquetaires", "Alexandre Dumas"),
    (2419, "La Dame aux camélias", "Alexandre Dumas fils"),
    (2650, "Du côté de chez Swann", "Marcel Proust"),
    (17489, "Les Misérables, tome I : Fantine", "Victor Hugo"),
    (32854, "Arsène Lupin, gentleman-cambrioleur", "Maurice Leblanc"),
    (62215, "Le Fantôme de l'Opéra", "Gaston Leroux"),
    (13704, "L'Homme à l'oreille cassée", "Edmond About"),
]

SIZES = {"short": (100, 200), "medium": (200, 350), "long": (350, 550)}
CACHE = Path.home() / ".cache" / "plume"
SESSIONS = CACHE / "sessions"
MODEL = "claude-opus-5-5"

console = Console()


# ---------- passages ----------

def load_book(book_id: int) -> str:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{book_id}.txt"
    if not path.exists():
        url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
        with console.status("Fetching the book from Project Gutenberg…"):
            raw = urllib.request.urlopen(url, timeout=30).read()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("latin-1")
        path.write_text(text, encoding="utf-8")
    return path.read_text(encoding="utf-8")


def body_of(text: str) -> str:
    text = text.replace("\r\n", "\n")
    start = re.search(r"\*\*\* ?START OF.*?\*\*\*", text)
    end = re.search(r"\*\*\* ?END OF", text)
    return text[start.end() if start else 0 : end.start() if end else len(text)]


def looks_like_prose(p: str) -> bool:
    letters = sum(c.isalpha() for c in p)
    return (
        letters > 0.7 * len(p)
        and sum(c.isdigit() for c in p) < 4
        and not p.isupper()
        and "[" not in p
        and "Gutenberg" not in p
        and p[0] in "«—–-" + "ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÇÉÈÊÎÔŒÙÛ"
        and p[-1] in ".!?»…"
    )


def passages(text: str, size: str) -> list[str]:
    lo, hi = SIZES[size]
    paras = [
        re.sub(r"\s*--\s*", " — ", " ".join(p.split()).replace("_", "")).strip()
        for p in re.split(r"\n\s*\n", body_of(text))
    ]
    paras = paras[len(paras) // 30 :]  # skip front matter (prefaces, tables, notes)
    out = []
    for p in paras:
        if len(p) < lo or not looks_like_prose(p):
            continue
        if len(p) <= hi:
            out.append(p)
            continue
        # Long paragraph: take its opening sentences up to the size limit
        chunk = ""
        for s in re.split(r"(?<=[.!?…])\s+(?=[«—A-ZÀ-Ü])", p):
            if len(chunk) + len(s) > hi:
                break
            chunk = f"{chunk} {s}".strip()
        if lo <= len(chunk) and looks_like_prose(chunk):
            out.append(chunk)
    return out


def pick_passage(size: str, query: str | None):
    books = BOOKS
    if query:
        q = strip_accents(query.lower())
        books = [b for b in BOOKS if q in strip_accents(f"{b[1]} {b[2]}".lower())]
        if not books:
            sys.exit(f"No book matches “{query}”. Try `plume --list`.")
    for _ in range(5):
        book = random.choice(books)
        found = passages(load_book(book[0]), size)
        if found:
            return book, random.choice(found)
    sys.exit("Couldn't find a good passage. Try another --size or --book.")


# ---------- comparing what you typed ----------

def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))


def normalize(s: str) -> str:
    """Even out French typography so only letters count: ’→', œ→oe, etc."""
    s = unicodedata.normalize("NFC", s)
    for a, b in {"’": "'", "‘": "'", "ʼ": "'", "œ": "oe", "Œ": "Oe", "æ": "ae", "Æ": "Ae", "–": "-", "—": "-"}.items():
        s = s.replace(a, b)
    return s


def words(s: str) -> list[str]:
    return [w.strip("'-") for w in re.findall(r"[\w'-]+", normalize(s)) if w.strip("'-")]


def compare(target: str, typed: str):
    """Return [(status, expected, typed)] where status is ok / accent / wrong / missing / extra."""
    exp, got = words(target), words(typed)
    key = lambda w: strip_accents(w.lower())
    sm = difflib.SequenceMatcher(None, [key(w) for w in exp], [key(w) for w in got], autojunk=False)
    result = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for e, g in zip(exp[i1:i2], got[j1:j2]):
                if e == g or e.lower() == g.lower():
                    result.append(("ok", e, g))
                else:
                    result.append(("accent", e, g))
        else:
            e_part, g_part = exp[i1:i2], got[j1:j2]
            for k in range(max(len(e_part), len(g_part))):
                e = e_part[k] if k < len(e_part) else None
                g = g_part[k] if k < len(g_part) else None
                result.append(("wrong" if e and g else "missing" if e else "extra", e, g))
    return result


def show_result(result, seconds: float, typed: str):
    line = Text()
    for status, e, g in result:
        if status == "ok":
            line.append(e, "green")
        elif status == "accent":
            line.append(g, "yellow underline")
            line.append(f"→{e}", "yellow dim")
        elif status == "wrong":
            line.append(g, "red strike")
            line.append(f"→{e}", "red dim")
        elif status == "missing":
            line.append(f"[{e}]", "dim")
        else:
            line.append(g, "red strike")
        line.append(" ")
    total = sum(1 for s, e, _ in result if e)
    ok = sum(1 for s, *_ in result if s == "ok")
    accent = sum(1 for s, *_ in result if s == "accent")
    speed = f"   [cyan]{len(typed.split()) / (seconds / 60):.0f} wpm[/]" if seconds >= 2 else ""
    console.print(Panel(line, title="How you did", border_style="cyan"))
    console.print(
        f"  [green]{ok}/{total} words exact[/]   "
        f"[yellow]{accent} accent slip{'s' if accent != 1 else ''}[/]{speed}"
    )
    if accent:
        console.print(
            "  [dim]Mac accents: hold a letter for options, or ⌥e é · ⌥` è · ⌥i ê · ⌥u ë · ⌥c ç[/]"
        )
    console.print()


# ---------- the lesson ----------

SYSTEM = """You are a warm, precise French tutor. The learner just typed out a passage \
from a French novel as practice. Write a short lesson in English (French examples are fine) \
using Markdown with exactly these sections:

## Meaning
A natural English translation, then one or two sentences on what is happening in this \
moment of the story. Keep big plot spoilers out.

## Words worth keeping
5–8 useful words or expressions from the passage, as a list: **French** (gender for nouns) — meaning, \
plus a short note if the word is literary, old-fashioned, or a false friend.

## Grammar spotlight
One or two structures the passage actually uses (for example passé simple, subjunctive, \
inversion, pronoun placement). Show the line from the passage and explain it simply.

## About the book
Two or three sentences on the author and why this book matters.

## Your typing
Only if the learner made mistakes: point out patterns (missing accents, spelling) and how to \
remember them. If they made none, one line of praise.

Match explanations to the learner's level. Keep the whole lesson under 450 words.

After the lesson, the learner may ask follow-up questions about the passage, the book, or \
French in general. Answer those directly and briefly, without the lesson sections."""


def lesson_prompt(book, passage, result, level):
    slips = [f"typed “{g}” for “{e}”" for s, e, g in result if s in ("accent", "wrong")]
    missed = [e for s, e, _ in result if s == "missing"]
    return (
        f"Learner level: {level}\n"
        f"Book: {book[1]} by {book[2]}\n\n"
        f"Passage:\n{passage}\n\n"
        f"Typing mistakes: {'; '.join(slips) or 'none'}\n"
        f"Words left out: {', '.join(missed) or 'none'}"
    )


def stream_api(messages: list[dict]):
    import anthropic

    client = anthropic.Anthropic()
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=8000,
        system=SYSTEM,
        output_config={"effort": "low"},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        messages=messages,
    ) as stream:
        yield from stream.text_stream


def as_transcript(messages: list[dict]) -> str:
    """The claude CLI takes one prompt, so earlier turns go in as a transcript."""
    if len(messages) == 1:
        return messages[0]["content"]
    *history, last = messages
    lines = [f"[{'Learner' if m['role'] == 'user' else 'Tutor'}]\n{m['content']}" for m in history]
    return "Conversation so far:\n\n" + "\n\n".join(lines) + f"\n\nThe learner now asks:\n{last['content']}"


def stream_claude_cli(messages: list[dict]):
    prompt = as_transcript(messages)
    cmd = [
        "claude", "-p", "--output-format", "stream-json", "--include-partial-messages", "--verbose",
        "--system-prompt", SYSTEM, "--tools", "", "--strict-mcp-config", "--no-session-persistence",
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    proc.stdin.write(prompt)
    proc.stdin.close()
    for raw in proc.stdout:
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            continue
        ev = msg.get("event", {}) if msg.get("type") == "stream_event" else {}
        if ev.get("type") == "content_block_delta" and ev["delta"].get("type") == "text_delta":
            yield ev["delta"]["text"]
    if proc.wait() != 0:
        raise RuntimeError(proc.stderr.read().strip() or "claude CLI failed")


def teach(messages: list[dict], status: str) -> str:
    if os.environ.get("ANTHROPIC_API_KEY"):
        chunks = stream_api(messages)
    elif shutil.which("claude"):
        chunks = stream_claude_cli(messages)
    else:
        sys.exit("Set ANTHROPIC_API_KEY or install Claude Code (`claude`) to get lessons.")
    text = ""
    with console.status(status):
        first = next(chunks, "")
    text += first
    with Live(Markdown(text), console=console, refresh_per_second=12, vertical_overflow="visible") as live:
        for chunk in chunks:
            text += chunk
            live.update(Markdown(text))
    return text


# ---------- listening ----------

NOVELTY_VOICES = {"Eddy", "Flo", "Grandma", "Grandpa", "Jacques", "Reed", "Rocko", "Sandy", "Shelley"}
voice: str | None = None
player: subprocess.Popen | None = None


def french_voices() -> list[tuple[str, str]]:
    """Installed French voices as (name, locale), best first."""
    if not shutil.which("say"):
        return []
    out = subprocess.run(["say", "-v", "?"], capture_output=True, text=True).stdout
    found = []
    for line in out.splitlines():
        m = re.match(r"(.+?)\s+(fr_[A-Z]{2})\s+#", line)
        if m and m.groups() not in found:
            found.append(m.groups())

    def rank(v):
        name, locale = v
        quality = 3 if "Premium" in name else 2 if "Enhanced" in name else 0 if name.split()[0] in NOVELTY_VOICES else 1
        return (-quality, locale != "fr_FR", name)

    return sorted(found, key=rank)


def choose_voice(wanted: str | None) -> str | None:
    voices = french_voices()
    if not wanted:
        return voices[0][0] if voices else None
    for name, _ in voices:
        if strip_accents(name.lower()).startswith(strip_accents(wanted.lower())):
            return name
    sys.exit(f"No French voice matches “{wanted}”. Try `plume --voices`.")


def stop_speaking():
    global player
    if player and player.poll() is None:
        player.terminate()
    player = None


def speak(text: str, slow: bool = False):
    """Read text aloud in the background. The same command again while it plays stops it."""
    global player
    if player and player.poll() is None:
        same = ("-r" in player.args) == slow
        stop_speaking()
        if same:
            console.print("[dim]Stopped.[/]")
            return
    if not voice:
        console.print("[yellow]No French voice found. Listening needs macOS and a French voice.[/]")
        return
    cmd = ["say", "-v", voice] + (["-r", "110"] if slow else []) + [text]
    player = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    console.print(f"[dim]🔊 {voice}{', slowly' if slow else ''} — {'/slow' if slow else '/l'} again to stop[/]")


def ask(prompt: str, passage: str) -> str:
    """input() that handles /l and /slow, returning the first other line typed."""
    while True:
        line = input(prompt)
        command = line.strip().lower()
        if command in ("/l", "/listen"):
            speak(passage)
        elif command == "/slow":
            speak(passage, slow=True)
        else:
            return line


# ---------- sessions ----------

def save_session(session: dict):
    SESSIONS.mkdir(parents=True, exist_ok=True)
    (SESSIONS / f"{session['id']}.json").write_text(json.dumps(session, ensure_ascii=False, indent=1), encoding="utf-8")


def load_sessions() -> list[dict]:
    files = sorted(SESSIONS.glob("*.json"), reverse=True) if SESSIONS.exists() else []
    return [json.loads(f.read_text(encoding="utf-8")) for f in files]


def latest_session() -> dict:
    sessions = load_sessions()
    if not sessions:
        sys.exit("No saved sessions yet. Run `plume` to start one.")
    return sessions[0]


def pick_session() -> dict | None:
    sessions = load_sessions()[:20]
    if not sessions:
        sys.exit("No saved sessions yet. Run `plume` to start one.")
    for i, s in enumerate(sessions, 1):
        when = time.strftime("%b %d %H:%M", time.localtime(int(s["id"].split("-")[0])))
        questions = len(s["messages"]) // 2 - 1
        console.print(
            f"[cyan]{i:>2}[/]  {when}  [italic]{s['book'][1]}[/]  "
            f"[dim]{s['passage'][:45]}…  ({questions} question{'s' if questions != 1 else ''})[/]"
        )
    choice = input("\nResume which session? [number, Enter to cancel] ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(sessions):
        return sessions[int(choice) - 1]
    return None


# ---------- main loop ----------

def show_passage(book, passage):
    console.print()
    console.print(Panel(
        Text(passage, style="bold"),
        title=f"[italic]{book[1]}[/] — {book[2]}",
        border_style="magenta",
        padding=(1, 2),
    ))


def converse(session: dict) -> bool:
    """Follow-up questions until the learner moves on. Returns True to quit."""
    messages = session["messages"]
    while True:
        console.print()
        question = ask("Ask a question, Enter for the next passage, q to quit › ", session["passage"]).strip()
        stop_speaking()
        if not question:
            return False
        if question.lower() == "q":
            return True
        console.print()
        messages.append({"role": "user", "content": question})
        messages.append({"role": "assistant", "content": teach(messages, "Thinking…")})
        save_session(session)


def round_(args) -> bool:
    while True:
        book, passage = pick_passage(args.size, args.book)
        show_passage(book, passage)
        console.print("[dim]Type the passage, then press Enter.  /l to listen · /slow to listen slowly · /s to skip[/]")
        while True:
            start = time.monotonic()
            typed = input("› ")
            command = typed.strip().lower()
            if command not in ("/l", "/listen", "/slow"):
                break
            speak(passage, slow=command == "/slow")
        seconds = time.monotonic() - start
        stop_speaking()
        if command not in ("/s", "/skip"):
            break
        console.print("[dim]Skipped. Here's another one.[/]")
    console.print()
    result = compare(passage, typed)
    show_result(result, seconds, typed)
    session = {
        "id": f"{int(time.time())}-{book[0]}",
        "book": list(book),
        "passage": passage,
        "typed": typed,
        "seconds": seconds,
        "result": result,
        "messages": [{"role": "user", "content": lesson_prompt(book, passage, result, args.level)}],
    }
    session["messages"].append({"role": "assistant", "content": teach(session["messages"], "Preparing your lesson…")})
    save_session(session)
    return converse(session)


def resume(session: dict) -> bool:
    show_passage(session["book"], session["passage"])
    show_result(session["result"], session["seconds"], session["typed"])
    console.print(Markdown(session["messages"][-1]["content"]))
    return converse(session)


def main():
    ap = argparse.ArgumentParser(description="Type a passage of French literature, then get a mini lesson on it.")
    ap.add_argument("--level", default="intermediate (B1)", help="your French level, e.g. 'beginner (A2)'")
    ap.add_argument("--size", choices=SIZES, default="medium", help="passage length")
    ap.add_argument("--book", help="only use books whose title or author contains this text")
    ap.add_argument("--list", action="store_true", help="list the books and exit")
    ap.add_argument("--resume", action="store_true", help="reopen your most recent session")
    ap.add_argument("--history", action="store_true", help="choose a past session to reopen")
    ap.add_argument("--voice", help="French voice for /l, e.g. 'amélie' (default: best installed)")
    ap.add_argument("--voices", action="store_true", help="list installed French voices and exit")
    args = ap.parse_args()

    if args.list:
        for _, title, author in BOOKS:
            console.print(f"[italic]{title}[/] — {author}")
        return
    if args.voices:
        for i, (name, locale) in enumerate(french_voices()):
            console.print(f"{name}  [dim]{locale}{'  (default)' if i == 0 else ''}[/]")
        return

    global voice
    voice = choose_voice(args.voice)

    try:
        quit_ = False
        if args.history or args.resume:
            session = pick_session() if args.history else latest_session()
            quit_ = session is None or resume(session)
        while not quit_:
            quit_ = round_(args)
    except (KeyboardInterrupt, EOFError):
        pass
    stop_speaking()
    console.print("\n[magenta]À bientôt ![/]")


if __name__ == "__main__":
    main()
