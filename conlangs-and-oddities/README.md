# Constructed languages, randomness and birdsong

*Part of [the Untranslatable Archive](../README.md).*

**Short answer: the meter measures grammar, not "natural versus invented."** Every constructed language tested avoids repeating a word like a real language does. Random words land almost exactly at chance. Birdsong lands far above it, higher than the Voynich.

| Text | Kind | Same word twice in a row, observed ÷ chance |
| --- | --- | --- |
| Esperanto (Zamenhof's own writings) | constructed language | 0.03× |
| Lojban | constructed language | 0.05× |
| Klingon | constructed language | 0.11× |
| Toki Pona | constructed language | 0.47× |
| Lorem ipsum (randomly drawn filler words) | random | 1.02× |
| Bengalese finch song (syllables) | birdsong | 2.10× |

All are significantly different from chance except Lorem ipsum, which isn't (p ≈ 0.27), as it shouldn't be.

## What each one shows

- **Constructed languages behave like languages.** Esperanto, Lojban and Klingon were invented, but they have real grammar, and they sit among natural languages. So the Voynich's above-chance repetition can't be explained by "someone invented a language." An invented language with grammar would still avoid repeats.
- **Toki Pona is the loosest** at 0.47×. It has only about 120 words, so the same word comes up constantly and grammar has less room to keep repeats apart. It's still well below chance.
- **Lorem ipsum calibrates the meter.** Words drawn at random are exactly what the shuffle imitates, so they should land at 1×, and they do (1.02×). Below 1 means grammar; about 1 means randomness; above 1 means something repetitive is producing the text.
- **Birdsong is the most extreme reading in the archive.** Bengalese finches sing a syllable over and over (`BBBB`, `CCCCCCCC`). An animal's song lands on the Voynich side, which shows that "above chance" means *repetitive production*, not meaning. Birdsong is measured by syllable, the only unit it has.

## Not on the meter

- **Elvish (Quenya, Sindarin):** no open running-text corpus could be found, and Tolkien's own texts are short and still under copyright.
- **Crows:** corvids make real sequences of discrete calls, and a 2024 study in *Science* showed carrion crows can plan how many calls to make. The one open dataset is from the paper "Unsupervised Discovery and Analysis of the Vocal Repertoires and Patterns of Select Corvid Species" ([Zenodo 18381906](https://doi.org/10.5281/zenodo.18381906)), about 3 GB of field audio. Turning that into call sequences means cutting noisy recordings into calls and sorting them by sound, so a result would carry wide error bars. Parked until it is worth the effort.

## Sources

- Klingon: [dadap/tlhIngan-Hol-QIch-wab-tamey](https://github.com/dadap/tlhIngan-Hol-QIch-wab-tamey), text sources only, in "xifan hol" spelling (`z` for the apostrophe; `zayz waz` = *'ay' wa'*, "part one").
- Esperanto: Zamenhof's *Originala Verkaro* (1929), from [alexcasper/esperanto](https://github.com/alexcasper/esperanto).
- Toki Pona: [kulupu-lapo/poki](https://github.com/kulupu-lapo/poki).
- Lojban: [La-Lojban/phrases](https://github.com/La-Lojban/phrases).
- Bengalese finch song sequences: [djinpsu/POMM-Python](https://github.com/djinpsu/POMM-Python).
- Lorem ipsum: generated with the Python [`lorem`](https://pypi.org/project/lorem/) package.
- Shuffles are within each sentence (or song bout), 500 times. Every number is in [`results.json`](results.json).
