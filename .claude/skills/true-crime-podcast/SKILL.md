---
name: true-crime-podcast
description: "Adapt a public-domain novel (or any fictional crime story) into a serialized true-crime podcast that stays true to the source's events and outcome: case file from the source text, invented modern investigators and interviewees, Rules of the Case (sourcing and chain-of-custody rules), a reveal ladder across episodes, multi-voice scripts for Kokoro, and fidelity audits against the source. Use when the user wants a true-crime podcast, a crime serial, a 'Serial-style' retelling, or a documentary-style audio adaptation of a book."
---

# True-crime podcast from a novel

A true-crime serial is journalism shaped as a story. The adaptation works when the *events* are the book's and the
*investigation* is new: a modern host who reads the surviving documents, finds the gaps, tests the theories, and
reaches the book's own ending honestly. Invent the investigators, not the crimes.

Downloaded references (see `../vendored/VENDORED.txt`): `true-crime-writer` (ethics, source hierarchy, attribution)
and `documentary-standards` (no fabricated quotes, no internal-state claims). The book-logic machinery comes from the
fantasy-audiobook-studio skills `world-rules` (numbered rules, stress test, reveal ladder, audit) and
`manuscript-review` (independent reviewer that never edits, issue ledger, hard round caps).

## 0. Can we do this?
The source must be public domain where the user lives and where it will be published (author dead 70+ years and
published before 1931 is safe in the EU/US). Use a public-domain *text* (Project Gutenberg), name the edition, and
put it in `source/`. If it is not public domain, stop.

## 1. Case file (from the source, not from memory)
Read the crime chapters in full and grep the rest. Write `case/evidence.md`: one row per fact,
`| ID | Fact | Source (chapter, line) | Who reports it | Witnessed by | Status |`. Status is one of
`book` (stated in the text), `invented-consistent` (a modern artefact the book's events entail, e.g. a court
register of a sentence the book describes) or `open` (the book never says: the podcast may ask, never answer).
Record every discrepancy between two accounts of the same thing. Those are the podcast's best material.

## 2. Rules of the Case (world-rules Build, for sourcing)
In `case/bible.md`, numbered rules the reader never hears, covering:
- **Canon.** Past events, names, dates and outcomes come from the source. Nothing is added to the past that the book
  forbids or never allows; open questions stay open.
- **Quotes.** Words in quotation marks from a historical person are verbatim from the text (cuts allowed, never
  rewording). Modern tape is invented and labelled as interview.
- **Inner states.** The host never states what a historical person felt or thought; she attributes it
  ("Victor says he…").
- **Chain of custody.** For every document: who wrote it, when, from whose memory, who edited it, how it survived.
- **Corroboration.** Which facts have a witness independent of the main narrator. List them; the finale leans on them.
- Stress test (world-rules): for each death, ask *who could have done it, who has an alibi, why didn't X just…*
  and make sure the book answers it or the podcast says plainly that it can't.

## 3. Cast (invent only what the investigation needs)
- **Host**: an active investigator, not a neutral voice (Koenig in *Serial*): she says what she believed and when it
  changed. One verbal habit, warm, allowed a dry joke for breathing room, never jokes about a victim.
  Stance: wonder, not debunking. When the source material is extraordinary, the host's question is "this is
  incredible; could it really be true?", and every episode lifts forward what holds up (independent witnesses,
  records that agree, details that match). Doubts and gaps are named honestly, but the arc builds the case for truth.
  Don't let her sound like a sceptic dismantling a tall tale.
- **3–4 recurring guests**, each owning one kind of evidence (the documents' owner, a legal historian, a forensic
  expert…). Distinct speech habits so a listener can tell them apart by ear. Real-sounding but fictional names; no
  real living experts or institutions put words in their mouths.
- **Readers** for the documents: one voice per historical writer, introduced on first use.
- Record each in the bible with voice, habit, what they know and when they learn it (knowledge states).

## 4. Season structure
- 6–10 episodes of 2,000–2,600 words (13–17 minutes). Each one moves the case forward and leaves one question open.
- **Cold open** (60–120 words): a scene or line from later, the strongest document fragment.
- Then the five beats per episode: **hook → world before → the event → investigation & aftermath → the unresolved**
  (the cliffhanger). Inside, write in scenes; drama peaks at the act break.
- Order for a novel: open on the most arresting surviving document (often the end), tell the crimes in the order
  the *investigator meets them*, put the suspect's own statement at the midpoint, test the strongest alternative
  theory honestly before the finale, end with what is proven, what isn't, and the source's own outcome.
- Victims are people first: give each a life before the death (true-crime-writer, victim-centred approach). The
  perpetrator gets context, not glamour.
- `case/outline.md`: one section per episode with target words, the beats, the evidence IDs it uses, the rules it
  shows, the closing hook. Then the **reveal ladder**: every fact the finale uses is heard at least one episode earlier.

## 5. Script format (for the ear and for Kokoro)
`episodes/epNN.md`, `# Episode N: Title`, then paragraphs. Host narration is plain paragraphs. Other speakers get a
paragraph of their own that starts with a tag: `[[Reber]] Text…` (exactly the names in `book.yaml`
`narration.characters`). Never mix the host and a guest in one paragraph. The host introduces every voice before it
speaks ("Judith Saville. Her family has kept these letters for two hundred years.") because a listener can't see a
caption. Theme/music cues are not spoken: use a scene break (`---`) for a pause. Writing-for-the-ear rules apply
(short sentences, names re-introduced, numbers as words, no italics carrying meaning).
Reader voices (the documents: letters, diaries, statements) run a little slower than the host, about 0.88 against
1.0 via `narration.speeds` in `book.yaml`, so the old words land with weight.

## 6. Fidelity loop (manuscript-review, adapted)
After drafting, a fresh reviewer subagent that **never edits** reads the episodes against `source/` and
`case/evidence.md` and returns: misquotes (compare word for word), events that contradict the book, invented past
facts not marked `invented-consistent`, internal-state claims, knowledge errors (someone knows something too early),
loopholes. Writer fixes, at most 3 rounds. Then a **fresh-listener test**: an agent that gets only the episodes
explains the case and the book's outcome in its own words. Anything it gets wrong is a finding.

## 7. Audio and site
Use the `voice-text` skill (kind `fiction`) with the narration characters mapped in `book.yaml`; listen-check;
export MP3s; publish a GitHub Pages site with a player per episode, show notes and a full transcript. Say clearly
on the site that it is fiction adapted from the novel and that the modern people are invented.
