# Rongorongo: does it repeat like a language?

*Part of [the Untranslatable Archive](../README.md).*

**Short answer: no, but not like the Voynich either.** Rongorongo puts the same glyph twice in a row about as often as chance would. Every language tested avoids that, even at the level of syllables. Rongorongo doesn't avoid it, and doesn't seek it out.

## What rongorongo is

Wooden tablets from Easter Island (Rapa Nui) carved with rows of small figures: birds, people, plants and shapes. About two dozen objects survive. Lines run in alternate directions, with every other line upside down. Nobody living could read them by the time outsiders asked in the 1860s.

## The test, adapted

Rongorongo has no word dividers, so the unit here is the glyph, not the word. A glyph might stand for a syllable, a word or something else; nobody knows. So it's compared with languages measured both ways: syllable by syllable and word by word.

One worry: Polynesian languages, Rapa Nui included, double syllables constantly (*rapa-rapa*, *koro-koro*), so a real Rapa Nui text might repeat signs legitimately. To check, Māori, a close Polynesian relative, was measured syllable by syllable.

| Text | Unit | Same unit twice in a row, observed ÷ chance |
| --- | --- | --- |
| Māori | words | 0.04× |
| Linear B (Greek) | words | 0.25× |
| Linear B (Greek) | syllable signs | 0.48× |
| Māori | syllables | 0.58× |
| Linear A | syllable signs | 0.66× |
| Voynich (EVA letters) | glyphs | 0.71× |
| **Rongorongo** | **glyphs** | **0.93–0.95×** |

Every other text avoids repeats below chance at whatever level it's measured. Even Māori, for all its doubling, repeats a syllable back-to-back less than chance. Rongorongo sits at chance (not significantly different from it), whichever coding detail is used.

## What it might mean

Things that could produce this:

- **Lists or chants.** Genealogies, calendars and litanies repeat the same formula with small changes, which isn't ordinary prose grammar. The Mamari tablet's lunar calendar is widely thought to be one such list.
- **Not a full writing system.** Rongorongo may record cues for memorized recitation rather than spell out language, which would not follow a language's rules.
- **Transcription conventions.** How compound glyphs are split into codes could add or remove adjacent repeats.

## Data and limits

- **Corpus:** tablets A–F from [phspaelti/RR-corpus](https://github.com/phspaelti/RR-corpus) (5,460 glyphs, standard Barthel-style numbering). This is about a third of the known corpus.
- **Māori:** 1,322 sentences from [douglasbagnall/mi.wikipedia](https://github.com/douglasbagnall/mi.wikipedia).
- Unreadable glyphs split a line into separate pieces. Shuffles are within each line or sentence, 500 times.
- Done with AI assistance (Claude); code in `code/`.
