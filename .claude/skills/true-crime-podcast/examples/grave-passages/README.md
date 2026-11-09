# Example: grave passages (slower reading for the sad and the frightening)

A worked example from *Darkness and Distance* (Frankenstein as a true-crime podcast), kept so the next podcast
starts with this instead of rediscovering it.

## The input (the user's words, 2026-11-09)

> lets make som adjustments, remember them. 1 when reading from the diareis lets lower the speed sligthly to
> ingcrase the gravity of the text. 2 the pod narrator is a bit to sceptical. make her tell the sotory as this is
> increadeble could it really be true? and then lt here lift forward all that seam to be true .re write and record
> all but publish episode 1 as early as possible

> we need to find parts of the story wich is sad or scary like the opening statmen with whatr is true and lowe the
> reading spead of all of them to make it more grave. make a folder wit exsampls and remeber this input anr resullt
> in a true crim pod skill

## The result

Three layers of pace, set in `voice/<slug>/book.yaml`:

```yaml
narration:
  speed: 1.0          # host and guests
  speeds:             # the documents (letters, diaries, statements) read slower
    Walton: 0.88
    Victor: 0.88
    Creature: 0.88
  grave:              # [grave] paragraphs
    factor: 0.9       # guests and readers: their own speed x 0.9
    speeds:
      narrator: 0.8   # the host, absolute
    voices:
      af_heart: af_heart,af_sarah   # the host voice blended 50/50 with a darker, more mature one
    pitch:
      narrator: -1.5  # semitones down, tempo kept
```

| Who | Normal | `[grave]` |
|---|---|---|
| Host | af_heart, 1.0 | af_heart+af_sarah blend, 0.8, pitch −1.5 semitones |
| Guests | 1.0 | 0.9 |
| Readers (the documents) | 0.88 | 0.79 |

### Second round: speed alone wasn't enough

> the grave opening is still to quick and happy

Slowing a bright voice (af_heart) keeps it bright, and Kokoro has no emotion control. Four takes of the opening
statement were rendered in `audio/opening-variants/`:

- A: slower (0.8) with a pause after every sentence
- B: a darker blend (af_heart + af_sarah)
- C: a hushed blend (af_heart + af_nicole)
- D: A pitched down 1.5 semitones

The user picked **B and D** and said "the paus inweteen centense is to long and unnatural". Two combinations followed:

- E: the B blend and the D pitch, with short 0.15 s breaths
- F: the same, but each paragraph rendered in one go with no added pauses

The user picked **F**. Lessons:

- Mood comes from the voice's colour (blend, pitch), not from speed.
- Never insert silence between sentences. Kokoro's own rhythm sounds natural, and added gaps sound robotic.
- Change only what the listener approved. The readers kept 0.79 with no pitch change, because only the host was
  auditioned.
- The user approved the creature's grave voice as it was ("i also like the cretures grave voice"): bm_lewis at
  0.79, with no blend and no pitch change. A deep voice slowed by 0.9 is already grave; only the bright host needed
  more.

In the script a grave paragraph starts with `[grave]`, before any speaker tag:

```
[grave] Here's what we know. One northern summer, more than two hundred years ago, …
[grave] [[Victor]] About five in the morning I discovered my lovely boy, …
```

The narration-prep step keeps the mark on every piece of a split paragraph. kokoro-narrate slows it down.
`check_quotes.py` and `site/build.py` strip it, so it never shows in a transcript. The mark is a cue for delivery,
not text.

88 paragraphs across eight episodes, about 11 per episode and roughly one paragraph in six. The full list is in
`passages.md`. Listen to `audio/`, where each clip has a `normal` and a `grave` take (the first round, speed only), and to
`audio/opening-variants/` (the second round; F is the one in use).

## How the passages were chosen

Mark a paragraph grave when it does one of these things:

1. **States the stakes plainly.** This includes the opening statement ("Here's what we know… five deaths… only one
   person was ever convicted… last seen drifting north on a raft of ice"), the "what we know" summaries, and the
   last line of an episode that names the next death.
2. **Is a death or its discovery.** A body found, a verdict, an execution, a coffin opened, a deathbed.
3. **Is the victim's own voice, or someone grieving them.** Justine's denial in the cell, Elizabeth's cry, a
   father's letter, Henry's last words to Victor.
4. **Is frightening.** A figure in a lightning flash, a face at the window, a threat ("I shall be with you on your
   wedding-night"), the confession in the suspect's own words, the shape over the coffin.
5. **Is the last image.** The cold open and the closing line of the season.

Don't mark arguments, evidence analysis, guest expertise, recaps or the light moments. Slow speech everywhere
stops meaning anything, so about one paragraph in six is the ceiling. When two grave paragraphs sit next to each
other, ask whether the second one earns it.

## Pairs with the host-tone change

Lines from the same request: the host stops sounding like a sceptic taking apart a tall tale. She asks "this is
incredible; could it really be true?", and then puts forward what holds up: independent witnesses, a court file that
agrees, the same mark on three necks. The grave passages are where the true parts land, so they get the most room.
