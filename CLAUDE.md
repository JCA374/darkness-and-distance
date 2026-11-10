# Darkness and Distance (Frankenstein as a true-crime podcast)

- Method: `.claude/skills/true-crime-podcast/SKILL.md`. Canon is `source/frankenstein-1831-gutenberg84.txt`; never contradict it.
- Before changing an episode, read `case/bible.md` (Rules of the Case) and `case/evidence.md`. New invented facts must be
  `invented-consistent` and added to evidence.md; unanswered things stay `open`.
- `python3 tools/check_quotes.py` must pass (quotes verbatim). Reviews go in `case/review.md`.
- Audio via the voice-text skill (studio at ~/code/other/fantasy-audiobook-studio). After re-prep, patch
  `voice/darkness-and-distance/audio/ch05.txt`: "M. Frankenstein" → "Monsieur Frankenstein" (quote must stay verbatim in the episode).
- Site: `site/build.py`; pushing to main deploys via Actions.
- Delivery: readers at 0.88 (`narration.speeds`); sad/frightening paragraphs start with `[grave]` (×0.9). Host tone is
  wonder ("could it really be true?") and builds the case for what holds. Example: `.claude/skills/true-crime-podcast/examples/grave-passages/`.
- Script feedback: `writing-feedback` skill. Notes page https://claude.ai/artifact/HKqtJUHtkTghaUQw82Esbb (pinned), built
  by `python3 tools/feedback_page.py`. On "I left notes": follow the skill's process; downstream = check_quotes,
  re-record changed chapters, export, push.
  Each application is a numbered round: commit, tag `notes-round-<n>`, `rounds/r<n>` doc via the skill's `round.py`.
  ★ Keep marks are collected in `feedback/keepers.md`: read it before any rewrite, and never rewrite kept words unless asked.
