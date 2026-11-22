# Does the Rohonc Codex's script look like Coptic?

Clint Foster · November 2026 · contact: emmertfoster [at] yahoo [dot] com

**Short answer: not especially.** Measured purely by the shapes of the signs, the Rohonc Codex resembles Old Hungarian and Hebrew a little more than other scripts, Coptic sits in the middle, and Greek and Latin fit worst. The margins are thin, so treat this as a lean, not a finding.

## What the Rohonc Codex is

A small 16th-century book of about 450 pages, held by the Library of the Hungarian Academy of Sciences, written in a script found in no other document. It has around 87 rough drawings, many with Christian scenes. In 2018 Király and Tokai argued it is a Christian devotional text in an invented script, read right to left.

## What we did

We ignored all earlier theories and compared shapes only.

1. **Cut the signs out of the pages.** From a restored facsimile of all 227 page spreads, software found 79,808 individual signs as ink blobs and sorted them by shape into 150 invented codes (R001 to R150). No transcription, font or reading by anyone else was used.
2. **Drew ten other scripts the same way.** Coptic, and scripts older than it or near the codex: Greek, Latin, Phoenician, Imperial Aramaic, Hebrew, Old Italic, Gothic, Old Hungarian and Glagolitic, from the free Noto fonts. Every sign and every letter was thinned to a one-pixel skeleton and redrawn at the same thickness, so only shape is compared, not pen weight.
3. **Matched every Rohonc sign to its closest letter in each script.** To be fair to small alphabets, each script was tested with random sets of 22 of its letters.
4. **Compared against a scrambled version of each script.** The same letters turned sideways or flipped keep their complexity but lose their real shapes. A script truly resembles the Rohonc only if its real letters match better than its scrambled ones. That difference is the "lift."

## Results

| Script | Lift, counting every sign on every page | Lift, counting each sign type once |
| --- | --- | --- |
| Old Hungarian | +0.083 | +0.049 |
| Hebrew | +0.085 | +0.043 |
| Phoenician | +0.049 | +0.036 |
| Gothic | +0.055 | +0.033 |
| Old Italic | +0.049 | +0.031 |
| Coptic | +0.046 | +0.030 |
| Imperial Aramaic | +0.050 | +0.022 |
| Glagolitic | +0.005 | +0.015 |
| Latin | +0.017 | +0.006 |
| Greek | −0.006 | −0.010 |

Typical uncertainty is about ±0.01 to ±0.02 per row.

**Why this probably isn't Coptic:** most Coptic letters are Greek letters, and Greek fits worst of all. Coptic only edges ahead of Greek through its few extra letters borrowed from Egyptian demotic, such as Ϧ and Ϭ.

**A caution about the top two:** Old Hungarian and Hebrew are both written right to left, like the Rohonc, so their letters face the same way. The Rohonc's most common signs are `)`-shaped crescents, and that is where those scripts score. The result may reflect writing direction more than family history. Phoenician and Aramaic are also right to left and land mid-table, so that is not the whole explanation.

## The 25 most common Rohonc signs, matched to Coptic

Similarity runs from 0 (nothing alike) to 1 (identical). Single straight strokes match any script's I-like letter, so high scores there mean little.

| Invented code | Occurrences | Nearest Coptic letter | Similarity | Nearest letter in any script | Similarity |
| --- | --- | --- | --- | --- | --- |
| R001 | 1,622 | Ϧ (U+03E6) | 0.49 | 𐲙 (Old Hungarian) | 0.69 |
| R002 | 1,598 | Ⲝ (U+2C9C) | 0.53 | 𐲋 (Old Hungarian) | 0.78 |
| R003 | 1,598 | Ⲓ (U+2C92) | 0.88 | 𐌹 (Gothic) | 0.89 |
| R004 | 1,465 | Ⲓ (U+2C92) | 0.59 | 𐲔 (Old Hungarian) | 0.64 |
| R005 | 1,444 | Ⲓ (U+2C92) | 0.65 | 𐌹 (Gothic) | 0.67 |
| R006 | 1,360 | Ⲓ (U+2C92) | 1.00 | 𐌉 (Old Italic) | 1.00 |
| R007 | 1,281 | Ⲝ (U+2C9C) | 0.49 | 𐲋 (Old Hungarian) | 0.76 |
| R008 | 1,215 | Ⲓ (U+2C92) | 0.73 | 𐌹 (Gothic) | 0.74 |
| R009 | 1,173 | Ⲓ (U+2C92) | 0.77 | 𐌹 (Gothic) | 0.77 |
| R010 | 1,071 | Ϭ (U+03EC) | 0.43 | 𐡎 (Aramaic (Imperial)) | 0.62 |
| R011 | 1,033 | Ⲓ (U+2C92) | 0.55 | 𐲔 (Old Hungarian) | 0.70 |
| R012 | 1,031 | Ⲝ (U+2C9C) | 0.48 | 𐲋 (Old Hungarian) | 0.68 |
| R013 | 965 | Ϧ (U+03E6) | 0.48 | 𐤁 (Phoenician) | 0.60 |
| R014 | 954 | Ⲝ (U+2C9C) | 0.53 | 𐲋 (Old Hungarian) | 0.80 |
| R015 | 952 | Ϧ (U+03E6) | 0.54 | 𐲛 (Old Hungarian) | 0.61 |
| R016 | 834 | Ⲓ (U+2C92) | 0.95 | 𐌹 (Gothic) | 0.96 |
| R017 | 825 | Ⲩ (U+2CA8) | 0.36 | 𐡃 (Aramaic (Imperial)) | 0.50 |
| R018 | 818 | Ϧ (U+03E6) | 0.62 | Ⱇ (Glagolitic) | 0.66 |
| R019 | 788 | Ⲓ (U+2C92) | 0.52 | 𐌂 (Old Italic) | 0.63 |
| R020 | 787 | Ⲝ (U+2C9C) | 0.47 | 𐌂 (Old Italic) | 0.72 |
| R021 | 763 | Ϭ (U+03EC) | 0.40 | 𐤓 (Phoenician) | 0.59 |
| R022 | 728 | Ⲏ (U+2C8E) | 0.50 | Ⱙ (Glagolitic) | 0.50 |
| R023 | 727 | Ϧ (U+03E6) | 0.32 | 𐤁 (Phoenician) | 0.50 |
| R024 | 726 | Ⲏ (U+2C8E) | 0.31 | 𐤕 (Phoenician) | 0.53 |
| R025 | 709 | Ⲓ (U+2C92) | 0.52 | 𐤋 (Phoenician) | 0.65 |

## Follow-up: the whole codex in Old Hungarian letters

Old Hungarian fit the shapes best, so every sign was swapped for its nearest-looking Old Hungarian letter and the codex was written out in reading order, right to left, page by page: [`rohonc_old_hungarian.txt`](rohonc_old_hungarian.txt), 4,344 lines and about 69,000 signs. Each line also gives the sounds those letters stand for. An independent 2014 transcription counted about 4,250 lines, so the line-finding holds up.

**This is a look-alike substitution, not a reading.** The test is whether the sounds come out shaped like Hungarian. They don't:

| Text, scored against Hungarian letter patterns | Bits per sound (lower = more Hungarian-like) |
| --- | --- |
| Real Hungarian words | 3.91 |
| Rohonc, shape-matched to Old Hungarian | 8.56 |
| Same letters shuffled randomly among the signs (300 tries) | 8.41 on average |
| Completely random letters (300 tries) | 8.53 on average |

The shape-matched version is less Hungarian-like than 76% of random shuffles. Signs that look like Old Hungarian letters do not carry those letters' sounds. Hungarian reference patterns come from the 30,000 commonest Hungarian words in the [wordfreq](https://github.com/rspeer/wordfreq) package.

## Limits

- Modern font letters are being compared with 16th-century handwriting.
- The sign sorting splits some signs into several codes by size or tilt, and merges touching pairs like `iii` into one blob.
- Shape resemblance says nothing about sound or meaning. It cannot decipher anything.
- Done with AI assistance (Claude, by Anthropic), which wrote and ran the code. Check before trusting.

## What is not in this folder

The page images and any sign images cut from them are not included, because the terms of the source scans were not checked. Nothing from Király and Tokai's site is included.

## Sources

- Page images: restored facsimile from [DiegoVallejoDev/codex-rohonczi-restoration](https://github.com/DiegoVallejoDev/codex-rohonczi-restoration), built from the Hungarian Academy of Sciences scans at [real-ms.mtak.hu/80](https://real-ms.mtak.hu/80/).
- Comparison letters: [Noto fonts](https://github.com/notofonts/notofonts.github.io).
- Background: Király, L. Z. and Tokai, G. (2018), "Cracking the code of the Rohonc Codex," *Cryptologia* 42(4), 285–315.
- Code: `code/` (paths point to the original working folders).
