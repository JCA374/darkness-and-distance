#!/usr/bin/env python3
"""Build feedback/review.html (the script-notes page) with the writing-feedback skill.

    python3 tools/feedback_page.py

Then republish it to https://claude.ai/artifact/HKqtJUHtkTghaUQw82Esbb. See ~/.claude/skills/writing-feedback/SKILL.md.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = Path.home() / ".claude/skills/writing-feedback/scripts/build_page.py"
eps = sorted((ROOT / "episodes").glob("ep*.md"))
labels = [f"--label={f.stem}=" + ("Trailer" if f.stem == "ep00" else f"Ep {int(f.stem[2:])}") for f in eps]
sys.exit(subprocess.call([sys.executable, str(BUILD), *map(str, eps), "--out", str(ROOT / "feedback/review.html"),
                          "--title", "Darkness and Distance Script Notes", "--heading", "Script notes",
                          "--label=_narrator=Tessa", *labels,
                          "--kind=guest=Judith,Reber,Okafor", "--kind=reader=Walton,Victor,Creature,Archive"]))
