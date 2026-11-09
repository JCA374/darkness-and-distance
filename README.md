# Darkness and Distance

**A true-crime podcast in eight episodes, adapted from Mary Shelley's *Frankenstein*.**

Listen: **https://jca374.github.io/darkness-and-distance/** (episodes, transcripts, the case file, and the whole season as an `.m4b` audiobook).

A retired teacher in Kent finds her ancestor's letters from the Arctic. Inside them: five deaths, one execution,
one acquittal and a suspect last seen drifting north on the ice. The host treats it as a cold case. She says where every
document came from, who wrote it down, and who touched it afterwards.

This is fiction. Every past event, date and quotation comes from the novel (public domain, 1831 text, `source/`), and the
book's outcome is unchanged. The host, guests and a few artefacts the book implies are invented.

## Layout

| Path | What |
|---|---|
| `source/` | the novel, Project Gutenberg #84 (1831 text) |
| `case/bible.md` | premise, **Rules of the Case**, cast, voices, knowledge states, decisions |
| `case/evidence.md` | every fact with its line in the novel; `book` / `invented-consistent` / `open` |
| `case/outline.md` | episode plan and reveal ladder |
| `case/review.md` | issue ledger from the independent reviews |
| `episodes/epNN.md` | the scripts (source of truth); `[[Name]]` paragraphs are other voices |
| `voice/darkness-and-distance/` | narration work dir: glossary, voice map, scripts, MP3s, `.m4b` |
| `tools/check_quotes.py` | gate: every quoted line must be verbatim from the novel |
| `site/` | GitHub Pages builder (`build.py`), show notes, the "how it was made" page |
| `.claude/skills/true-crime-podcast/` | the method, as a reusable Claude Code skill |

## Rebuild

```bash
python3 tools/check_quotes.py                          # must print OK
V=~/.claude/skills/voice-text/scripts/voice.sh         # fantasy-audiobook-studio pipeline
$V new episodes/ep0*.md --kind fiction --slug darkness-and-distance --force
$V prep voice/darkness-and-distance && $V narrate voice/darkness-and-distance
$V listen voice/darkness-and-distance && $V export voice/darkness-and-distance
python3 site/build.py                                  # or push: Actions builds and deploys
```
