#!/usr/bin/env python3
"""Build the GitHub Pages site into _site/ from the repo: episodes/, case/, voice/<slug>/audio/.

    pip install markdown pyyaml   (the Actions workflow does this)
    python3 site/build.py
"""
import html
import re
import shutil
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
AUDIO = ROOT / "voice" / "darkness-and-distance" / "audio"
REPO = "https://github.com/JCA374/darkness-and-distance"
EPISODES = yaml.safe_load((ROOT / "site" / "episodes.yaml").read_text(encoding="utf-8"))

SPEAKERS = {
    "Judith": ("Judith Saville", "guest"),
    "Reber": ("Dr Anselm Reber", "guest"),
    "Okafor": ("Dr Paul Okafor", "guest"),
    "Walton": ("Robert Walton (letters, read)", "reader"),
    "Victor": ("Victor Frankenstein (statement, read)", "reader"),
    "Creature": ("The creature (as recorded, read)", "reader"),
    "Archive": ("Archive document (invented for this podcast, read)", "reader"),
}

CSS = """
:root{--bg:#0b111c;--panel:#131c2b;--ink:#e6ebf1;--muted:#9fb0c4;--ice:#c9d8e6;--accent:#8fb4d9;--line:#24324a;
--guest:#d9c38f;--reader:#a9c7a0}
:root[data-theme="light"]{--bg:#f4f6f9;--panel:#ffffff;--ink:#16202e;--muted:#55657a;--ice:#2c4560;--accent:#2e5f8f;--line:#d5dde7;--guest:#7a5a12;--reader:#3b6a32}
@media (prefers-color-scheme: light){:root:not([data-theme="dark"]){--bg:#f4f6f9;--panel:#ffffff;--ink:#16202e;--muted:#55657a;--ice:#2c4560;--accent:#2e5f8f;--line:#d5dde7;--guest:#7a5a12;--reader:#3b6a32}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:18px/1.65 Georgia,"Iowan Old Style","Palatino Linotype",serif}
a{color:var(--accent)}
header.top{border-bottom:1px solid var(--line);background:var(--panel)}
header.top nav{max-width:860px;margin:0 auto;padding:12px 16px;display:flex;gap:18px;flex-wrap:wrap;align-items:baseline}
header.top .brand{font-weight:bold;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);text-decoration:none;margin-right:auto}
header.top a{text-decoration:none;font-size:16px}
main{max-width:860px;margin:0 auto;padding:24px 16px 64px}
.hero{display:grid;grid-template-columns:minmax(0,260px) 1fr;gap:28px;align-items:center;margin:8px 0 28px}
.hero img{width:100%;border-radius:6px;box-shadow:0 8px 30px rgba(0,0,0,.35)}
@media (max-width:640px){.hero{grid-template-columns:1fr}.hero img{max-width:260px}}
h1{font-size:2.1em;line-height:1.15;margin:.2em 0}
h2{font-size:1.35em;margin:1.6em 0 .4em}
.lede{color:var(--muted);font-size:1.05em}
.note{border-left:3px solid var(--accent);background:var(--panel);padding:12px 16px;margin:20px 0;font-size:16px;color:var(--muted)}
.ep{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px 18px;margin:16px 0}
.ep h3{margin:0 0 4px;font-size:1.15em}
.ep .meta{color:var(--muted);font-size:15px}
.ep p{margin:.5em 0}
audio{width:100%;margin:10px 0 4px}
.btn{display:inline-block;border:1px solid var(--accent);border-radius:6px;padding:8px 14px;text-decoration:none;font-size:16px;margin:4px 8px 4px 0}
.transcript p{margin:0 0 1em}
.transcript .sp{display:block;font:bold 12px/1.4 system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;margin-bottom:2px}
.transcript .guest{border-left:3px solid var(--guest);padding-left:14px}
.transcript .guest .sp{color:var(--guest)}
.transcript .reader{border-left:3px solid var(--reader);padding-left:14px;font-style:italic}
.transcript .reader .sp{color:var(--reader);font-style:normal}
.transcript hr,.doc hr{border:0;border-top:1px solid var(--line);margin:28px auto;width:40%}
.doc table{border-collapse:collapse;width:100%;font-size:14px;display:block;overflow-x:auto}
.doc th,.doc td{border:1px solid var(--line);padding:5px 7px;vertical-align:top;text-align:left}
.doc th{background:var(--panel)}
.doc code{font-size:.9em}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:14px;text-align:center;padding:20px 16px}
.pager{display:flex;justify-content:space-between;gap:12px;margin-top:36px;font-size:16px}
"""


def page(title, body, depth=0):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="A fictional true-crime podcast adapted from Mary Shelley's Frankenstein.">
<link rel="icon" href="{up}cover.jpg"><style>{CSS}</style></head>
<body><header class="top"><nav><a class="brand" href="{up}index.html">Darkness and Distance</a>
<a href="{up}index.html#episodes">Episodes</a><a href="{up}case.html">The case file</a><a href="{up}making.html">How it was made</a></nav></header>
<main>{body}</main>
<footer>A work of fiction adapted from <i>Frankenstein; or, The Modern Prometheus</i> by Mary Shelley (public domain).
The modern people in it are invented. · <a href="{REPO}">Source on GitHub</a></footer></body></html>"""


def transcript(md_text):
    out = []
    for para in md_text.strip().split("\n\n"):
        para = re.sub(r"^\[grave\]\s*", "", para.strip())  # narration cue (read slower), not text
        if para.startswith("# "):
            continue
        if para == "---":
            out.append("<hr>")
            continue
        m = re.match(r"\[\[(\w+)\]\]\s*(.*)", para, re.S)
        if m and m.group(1) in SPEAKERS:
            name, kind = SPEAKERS[m.group(1)]
            out.append(f'<p class="{kind}"><span class="sp">{html.escape(name)}</span>{html.escape(m.group(2))}</p>')
        else:
            out.append(f"<p>{html.escape(para)}</p>")
    return "\n".join(out)


def duration(n):
    import subprocess
    mp3 = AUDIO / f"ch{n:02d}.mp3"
    if not mp3.exists():
        return ""
    try:
        s = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)],
                                 capture_output=True, text=True).stdout.strip())
        return f"{int(s // 60)} min"
    except ValueError:
        return ""


def doc_page(title, files, intro):
    parts = [f"<h1>{title}</h1>", f'<p class="lede">{intro}</p>']
    for f in files:
        text = (ROOT / f).read_text(encoding="utf-8")
        parts.append(f'<section class="doc">{markdown.markdown(text, extensions=["tables"])}</section><hr>')
    return "\n".join(parts)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "ep").mkdir(parents=True)
    (OUT / "audio").mkdir()
    shutil.copy(ROOT / "site" / "static" / "cover.jpg", OUT / "cover.jpg")
    (OUT / ".nojekyll").write_text("")
    m4b = sorted(AUDIO.glob("*.m4b"))
    for f in list(AUDIO.glob("ch*.mp3")) + m4b:
        shutil.copy(f, OUT / "audio" / f.name)

    cards = []
    first, last = min(e["n"] for e in EPISODES), max(e["n"] for e in EPISODES)
    for e in EPISODES:
        n = e["n"]
        label = "Trailer" if n == 0 else f"Episode {n}"
        mp3 = f"audio/ch{n:02d}.mp3"
        player = f'<audio controls preload="none" src="{mp3}"></audio>' if (AUDIO / f"ch{n:02d}.mp3").exists() else '<p class="meta">Audio coming soon.</p>'
        cards.append(f"""<div class="ep"><h3><a href="ep/ep{n:02d}.html">{label}: {html.escape(e['title'])}</a></h3>
<div class="meta">{duration(n)}</div>{player}<p>{html.escape(e['summary'])}</p></div>""")
        md = (ROOT / "episodes" / f"ep{n:02d}.md").read_text(encoding="utf-8")
        prev = f'<a href="ep{n-1:02d}.html">← {"Trailer" if n == 1 else f"Episode {n-1}"}</a>' if n > first else "<span></span>"
        nxt = f'<a href="ep{n+1:02d}.html">Episode {n+1} →</a>' if n < last else "<span></span>"
        notes = "".join(f"<li>{html.escape(x)}</li>" for x in e.get("notes", []))
        body = f"""<p class="meta"><a href="../index.html#episodes">All episodes</a></p>
<h1>{label}: {html.escape(e['title'])}</h1>
{('<audio controls preload="none" src="../' + mp3 + '"></audio>') if (AUDIO / f"ch{n:02d}.mp3").exists() else ''}
<p class="lede">{html.escape(e['summary'])}</p>
<h2>Show notes</h2><ul>{notes}</ul>
<h2>Transcript</h2><div class="transcript">{transcript(md)}</div>
<div class="pager">{prev}{nxt}</div>"""
        (OUT / "ep" / f"ep{n:02d}.html").write_text(page(f"{label}: {e['title']} · Darkness and Distance", body, 1), encoding="utf-8")

    book = ""
    if m4b:
        mb = m4b[0].stat().st_size / 1e6
        book = f'<a class="btn" href="audio/{html.escape(m4b[0].name)}" download>Download the whole season as an audiobook (.m4b, {mb:.0f} MB)</a>'
    index = f"""<section class="hero"><img src="cover.jpg" alt="Cover: a dog sledge on the Arctic ice under a night sky">
<div><h1>Darkness and Distance</h1>
<p class="lede">For a year, Tessa Lind checked a sea captain's letters from the Arctic against every record she could find. The more she learned, the stranger it got, and the more of it checked out.
Five deaths, a young woman executed for a murder she didn't commit, and a suspect last seen drifting north on the ice.
Eight episodes and a trailer. Could it really be true?</p>
{book}<a class="btn" href="case.html">Open the case file</a></div></section>
<div class="note"><b>This is fiction.</b> It retells Mary Shelley's novel <i>Frankenstein</i> (1818; 1831 text) as a cold-case investigation.
Every event, date and quotation from the past comes from the novel, and nothing in it changes the book's outcome.
The host, Tessa Lind, and her guests Judith Saville, Dr Anselm Reber and Dr Paul Okafor are invented, as are the second ink in the
letters and every archive document Tessa finds (the Saville family papers, the Geneva trial file and registers, the university register,
the Paris police papers, the Savoy register and the Lloyd's List entry). They only ever confirm what the novel says. Voices are synthetic (Kokoro text-to-speech).</div>
<h2 id="episodes">Episodes</h2>
{''.join(cards)}"""
    (OUT / "index.html").write_text(page("Darkness and Distance · a true-crime podcast", index), encoding="utf-8")

    case = doc_page("The case file", ["case/bible.md", "case/evidence.md", "case/outline.md"],
                    "The working files behind the podcast: the Rules of the Case that every episode obeys, the evidence locker "
                    "(every fact with its line in the novel), and the episode plan with its reveal ladder. Contains spoilers.")
    (OUT / "case.html").write_text(page("The case file · Darkness and Distance", case), encoding="utf-8")

    making = doc_page("How it was made", ["site/making.md", "case/review.md"],
                      "From a public-domain novel to eight checked episodes and an audiobook.")
    (OUT / "making.html").write_text(page("How it was made · Darkness and Distance", making), encoding="utf-8")
    print(f"built {OUT.relative_to(ROOT)}: {len(EPISODES)} pages, audio files: {len(list((OUT / 'audio').iterdir()))}")


if __name__ == "__main__":
    main()
