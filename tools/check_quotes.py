#!/usr/bin/env python3
"""Rule 4 gate: every reader paragraph ([[Walton]], [[Victor]], [[Creature]]) and every quoted phrase in the
host's narration must be verbatim from the 1831 text (cuts allowed only between quotes, never inside one).

Compares on letters and digits only, so punctuation, quote marks, line breaks and the ae ligature don't matter.
Modern speech that the host quotes (an email, a guest) goes in ALLOW below.
[[Archive]] paragraphs (the season's invented finds, bible rules 21-24) are not from the novel: each must appear
verbatim in case/evidence.md under "Archive texts", so every invented document is on file.

    python3 tools/check_quotes.py            # all episodes
    python3 tools/check_quotes.py ep03       # one
Exit 1 if anything is not found.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source" / "frankenstein-1831-gutenberg84.txt"
EVIDENCE = ROOT / "case" / "evidence.md"
READERS = {"Walton", "Victor", "Creature"}
MIN_WORDS = 3  # shorter quotes ("cousin", "the dæmon") are names and terms, not claims

# Quoted phrases in the host's narration that are modern (not from the book).
ALLOW = {
    "give me a month",
    "do you know these people",
    "who are these people to you",
}


def norm(text: str) -> str:
    text = text.lower().replace("æ", "ae").replace("daemon", "daemon")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def main() -> int:
    src = norm(SOURCE.read_text(encoding="utf-8"))
    ev = EVIDENCE.read_text(encoding="utf-8")
    archive = norm(ev[ev.index("## Archive texts"):]) if "## Archive texts" in ev else ""
    # The text has "dæmon"; scripts may write "daemon". Both normalise to "daemon".
    names = sys.argv[1:]
    files = sorted((ROOT / "episodes").glob("ep*.md"))
    if names:
        files = [f for f in files if f.stem in names]
    bad = 0
    for f in files:
        for n, para in enumerate(f.read_text(encoding="utf-8").split("\n\n"), 1):
            para = re.sub(r"^\[grave\]\s*", "", para.strip())  # [grave] = read slower, not text
            m = re.match(r"\[\[(\w+)\]\]\s*(.*)", para, re.S)
            if m and m.group(1) == "Archive":
                if norm(m.group(2)) not in archive:
                    bad += 1
                    print(f"{f.stem} ¶{n}: ARCHIVE TEXT NOT ON FILE in evidence.md: {m.group(2)[:100]}")
                continue
            if m and m.group(1) in READERS:
                pieces = [m.group(2)]
            elif m:
                continue  # modern guest tape
            else:
                pieces = re.findall(r"[\"“]([^\"”]+)[\"”]", para)
            for q in pieces:
                nq = norm(q)
                if len(nq.split()) < MIN_WORDS or nq in ALLOW:
                    continue
                if nq not in src:
                    bad += 1
                    print(f"{f.stem} ¶{n}: NOT IN SOURCE: {q[:110]}")
    print(f"checked {len(files)} episode(s): {'OK' if not bad else f'{bad} problem(s)'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
