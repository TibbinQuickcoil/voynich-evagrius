# Lab notebook: Voynich and Rohonc, 21–22 November 2026

A plain-language record of how this repository came to be, in the order it happened, dead ends included. Clint Foster asked the questions and steered; Claude (Anthropic's AI model) wrote and ran the code. Results are in [README.md](README.md), [DETAILS.md](DETAILS.md) and [rohonc/README.md](rohonc/README.md); this page is the story behind them.

## Saturday evening: where the name came from

The session started as a slow Saturday. That led to a tangent about *acedia*, the "noonday demon" described by the 4th-century desert monk Evagrius Ponticus: the restless flatness of an afternoon that won't end. A little later the Voynich Manuscript came up, and the idea of a bored scribe filling pages by copying his own words became the working premise. He was named **Brother Evagrius**.

## The five hypotheses

We set out what the Voynich text could be and what each idea predicts:

1. A natural language in an invented script.
2. A "verbose" cipher, where each real letter becomes two or three glyphs.
3. Abbreviated or shorthand Latin or a European vernacular.
4. A hoax made with a mechanical generator.
5. Fluent nonsense made by copying and changing recent words: Brother Evagrius.

Clint chose to run with number 5 as the working premise.

## First measurements

- **Letter predictability.** Voynich letters are far more predictable than Latin or English. Counting common glyph groups as single symbols closes about 60% of that gap, so many "letters" in the standard EVA alphabet are really parts of larger symbols.
- **Repetition.** Real languages avoid putting the same word twice in a row; the Voynich does it more than chance. Near-copies (one letter different) are also above chance and fade over about twenty words.
- **Line effects.** Voynich lines open and close with their own glyph habits. Removing the first and last word of each line made the repetition stronger, not weaker.

## Building Brother Evagrius

A simulated scribe who copies a recent word and changes a glyph or two. His failed drafts taught the most:

- When he copied line-start and line-end decorations along with words, everything collapsed into one long repeated word. So those decorations are added at the edges, not copied.
- Unconstrained copying drifted into nonsense like `qoqoqo`, so the real scribe followed rules about what a word may look like.
- Rules about letter pairs still allowed runs like `chckhckh`, so those rules span at least three glyphs.

He matched the repetition but used too small a vocabulary.

## Clint's challenges, and what came of them

- **"He was just transcribing older works."** Tested and set aside: a copyist reproduces his source's statistics, and copied real language avoids repeats. Clustering pages by vocabulary did, though, independently rediscover Currier's two Voynich "languages" (A and B), supporting the idea of several distinct bodies of text.
- **Known nonsense as a control.** The *Codex Seraphinianus*, whose author says its script means nothing, also repeats words above chance.
- **"Maybe that OCR bot didn't know about Evagrius."** A fair catch: the program that read the Seraphinianus leans toward the words it was trained on, and 63% of its exact repeats involve those words. But removing every training word left the repetition in place.
- **"Give me virgin data. Make up your own syllabary."** We built a transcription straight from the Voynich scans with no human reading: ink cut into pen-stroke blobs, sorted by shape into 80 invented symbols. It confirmed the side-by-side copying on its own.

## The hard checks

- **A second human transcription** (Zandbergen–Landini) agreed with the first on every repetition measure.
- **Three failures, all documented:** pairing machine words with human words by position (wrong words got paired); a simulated machine-error model (it destroyed a signal the real machine detects); herbal pages (plant stems crossing lines faked copying from the line above).
- **Word positions from voynichese.com** finally let us pair about 4,700 human-read words with the ink. The ink backs the human-reported repeats equally side by side, one line apart and pages apart. Transcriber bias was ruled out, and copying from the last few lines showed up in the ink itself.
- **The Naibbe cipher**, the best published case for "it's a code," turns Latin into Voynich-looking text but keeps Latin's avoidance of repeats. The Voynich doesn't.
- **The Timm–Schinner generator**, the published version of Brother Evagrius, matches the vocabulary but throws away half its exact repeats in code. Giving Evagrius the same "not that word again" habit closed much of his gap. No model matched everything.
- **Italian, German and French** joined Latin and English: all five avoid repeats.

## Writing it up

The first write-up was too technical, and Clint said so, pointedly; it was rewritten in plain language, with conclusions first and numbers moved to DETAILS.md. A literature check showed the repetition itself was already known (voynich.ninja thread 5878; the *Strata* articles), so the write-up credits that and claims only what looked new: the ink check and the two comparison books. Clint flagged that the main Voynich forum bans AI-assisted work (confirmed: zero tolerance), so it was published here instead.

## Sunday: the Rohonc Codex

- **Coptic?** Clint thought the Rohonc script looked vaguely Coptic. We cut 79,808 signs out of all 227 page spreads, sorted them into 150 invented codes, and compared their shapes with ten scripts. Coptic landed in the middle; Greek, which most Coptic letters come from, fit worst. Old Hungarian and Hebrew fit best, but only slightly, and both are written right to left like the Rohonc, which may explain it.
- **"Put it into Old Hungarian."** Every sign was swapped for its nearest-looking Old Hungarian letter. The result sounds nothing like Hungarian, no better than random letters. The signs borrow the look of Old Hungarian, not its sounds.
- **"Same premise as the Voynich: an ignorant transcriber."** A scribe copying a real text he couldn't read would keep its grammar, so neighbouring words would look alike less than chance. The Rohonc's neighbouring words look alike more than chance in all nine settings tried, so it leans toward a scribe composing as he went. That's weaker than the Voynich result, because there is no human transcription to check the ink against.

## Open threads

- Herbal and other Voynich sections need a segmenter that can separate text from drawings.
- Homophonic and nomenclator ciphers haven't been tested against the repeat signature.
- A scribe model that copies while keeping a large vocabulary.
- The Rohonc repeat test on Király and Tokai's human transcription, whose site permits analysis but wasn't reachable from the workspace.
- A note to the *Strata* author, whose work the ink check most directly extends.
