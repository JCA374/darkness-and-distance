## Is this allowed?

Mary Shelley's *Frankenstein; or, The Modern Prometheus* was published in 1818 and revised in 1831. Shelley died in
1851, so the novel is in the public domain everywhere. The text used here is the 1831 edition from Project Gutenberg
(eBook #84), kept in the repository's `source/` folder.

## The idea

The novel is already a case file. It's written as letters from an Arctic captain, Robert Walton, to his sister.
Inside them is Victor Frankenstein's dying statement, and inside that, the statement of the being he made. Read as
true crime, the book has five deaths, an execution, an acquittal on an alibi, and a suspect who was never
charged and was last seen on the ice. The podcast keeps every past event and the book's ending. It invents only the
investigation: a host, three guests, a sea chest in Kent, Victor's corrections in a second ink, and the archive
documents Tessa finds, one per episode (a burial register, a trial file, a university register, the Paris police
papers, a notary's act, a Savoy death entry, Lloyd's List). Every find only confirms what the novel says, none closes
a question the novel leaves open, and each one is on file in the evidence locker.

## Method

1. **Research.** I looked for existing true-crime writing skills. Two were worth keeping as references, and both are
   vendored unmodified with their licences:
   - `true-crime-writer` (ethics, source hierarchy, attribution)
   - `documentary-standards` (no invented quotes, no claims about inner states)

   Craft notes came from published interviews about *Serial*: an active narrator who says when her mind changes,
   uncertainty kept in view, act breaks with a cliffhanger at the end of each episode, and breathing room. These
   became the project's own skill, `true-crime-podcast`.
2. **Case file from the text.** About 80 facts, each with its line number in the novel and a status: `book`,
   `invented-consistent` or `open`. The book's own discrepancies are kept and used, never fixed: the pocket against the
   fold of her dress, the scream against "as they slept", and Perth against the Irish beach.
3. **Rules of the Case.** This uses the method of the fantasy-audiobook studio's `world-rules` skill: numbered rules
   that every episode obeys, a stress test ("why didn't X just…?"), and a reveal ladder. Every fact the finale uses
   is heard at least one episode earlier.
4. **Draft, then gate.** `tools/check_quotes.py` checks that every reader passage and every quoted phrase is verbatim
   from the novel. It must pass before audio.
5. **Independent review.** The studio's `manuscript-review` loop was used. A fresh fidelity auditor checked the
   episodes against the novel, and a fresh listener read only the episodes. Neither could edit anything. Their
   findings and what was done about each are in the ledger below.
6. **Audio.** The studio's `voice-text` pipeline produced the audio:
   - a speech-flow scan and a pronunciation glossary
   - Kokoro text-to-speech, run locally, with seven voices
   - a Whisper listen-check
   - loudness-normalised MP3s and a single `.m4b` audiobook with chapter markers

## Voices

| Who | Voice |
|---|---|
| Tessa Lind, host (invented) | af_heart |
| Judith Saville (invented) | bf_emma |
| Dr Anselm Reber, legal historian (invented) | bm_george |
| Dr Paul Okafor, forensic pathologist (invented) | am_michael |
| Robert Walton's letters (reader) | bm_fable |
| Victor Frankenstein's statement (reader) | bm_daniel |
| The creature's words (reader) | bm_lewis |
| Archive documents (reader, invented) | bf_isabella |

The readers speak at 0.88 of normal speed, slightly slower than the host, so the documents carry their weight.
