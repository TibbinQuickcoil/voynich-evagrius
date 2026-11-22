# Details

Numbers, methods and failures behind the summary in [README.md](../README.md). Every test compares the real text with the same text shuffled, so results are ratios: observed ÷ chance.

## Prior work

- [Bowern et al. (2020)](https://www.voynich.ninja/thread-3344.html) measured full reduplication at 0.84% (Currier A) and 0.94% (B) per word.
- A [voynich.ninja analysis](https://www.voynich.ninja/thread-5878.html) found doubling at about 2× chance across six comparison languages, with permutation nulls.
- [*Strata* (2026)](https://artwaste.land/strata/is-the-voynich-manuscript-a-language/) measured 1.5× chance against 50 medieval books, all below one, and [showed](https://artwaste.land/strata/is-the-voynich-manuscript-a-hoax/) that the Timm–Schinner generator discards half its exact repeats in code.
- Timm and Schinner (2020) proposed self-citation from the current and preceding lines.

New here, as far as a quick search shows: the coordinate-based ink test, the Naibbe cipher run through the repeat test, and the *Codex Seraphinianus* OCR control with its training-word check.

## Data and methods

- **Transcriptions.** Takahashi EVA and Zandbergen–Landini ZL3b (13 May 2025). Paragraph text only; lines with unreadable glyphs dropped.
- **Baselines.** Latin (Vulgate, Pliny, Varro, Vitruvius), English (KJV, *Moby Dick*, Austen), Italian, German, French, cut to comparable length.
- **Null model.** Interior words (not first or last on a line) shuffled within each page; 150–300 shuffles per test, so p = 0.003 is the floor at 300.
- **Near-copy.** Two words differing by one glyph inserted, deleted or substituted. **Horizontal** = next word on the line; **vertical** = word in the matching position on the next line.

## Letter entropy

| Text | 0 merges | 10 merges | 40 merges |
| --- | --- | --- | --- |
| Voynich (Takahashi EVA) | 2.15 | 2.69 | 3.43 |
| Latin, Pliny | 3.42 | 3.67 | 4.07 |
| Latin, Vulgate | 3.34 | 3.60 | 3.90 |
| English, KJV | 3.11 | 3.38 | 3.56 |

Conditional entropy in bits after the same number of automatic pair merges for every text. About 60% of the Voynich's gap closes under merging, so many EVA letters are parts of larger symbols. Naibbe ciphertext also lands at 2.08 bits, so entropy cannot separate a cipher from nonsense.

## Repetition in human transcriptions

| Transcription and pages | Same line, near-copy | Same line, exact | Line below, near-copy |
| --- | --- | --- | --- |
| Takahashi, whole book | 1.25× | 1.30× | 1.16× |
| Zandbergen–Landini, whole book | 1.32× | 1.26× | 1.14× |
| Z–L, Currier A | 1.42× | 1.30× | 1.17× |
| Z–L, Currier B | 1.27× | 1.23× | 1.11× |

All p < 0.01 except Currier A/B exact (0.03, 0.02). Line-initial words start with `p` 19× and `t` 5× more often than interior words; line-final words end in `m` 17× more often. Exact next-word repeats in Italian, German and French: 0.22×, 0.03×, 0.11×.

## Controls

- **Naibbe cipher** ([Greshko 2025](https://doi.org/10.1080/01611194.2025.2566408)) of Pliny and Caesar: exact 0.33–0.37×, near 0.82–0.83×.
- **Codex Seraphinianus** OCR: exact 1.25×, near 1.30×; with all 418 OCR training words removed, exact 3.04×, near 1.76×. 63% of exact repeats involve training words, so its exact/near split is unreliable.
- **Timm–Schinner generator**: exact 0.45–0.92× (three seeds), near 1.02–1.29×.

## Machine transcription and ink test

20 recipe pages (f103r–f116r, excluding f111r/v), 1113 × 1600 px scans, about 34,500 pen-stroke blobs clustered into an invented 80-symbol syllabary. Word counts within ±20% of human counts on 18 of 20 pages. Same-line near-copies 1.12–1.14× (p = 0.003); line-below 0.99–1.03× (not significant) in symbol spellings.

voynichese.com word boxes, fitted to the scans by scale and offset per page on box overlap, gave 4,659 one-to-one pairs (human length vs machine width r = 0.49).

| Pair direction | Pairs | Ink similarity, human says same | Human says unrelated | Margin |
| --- | --- | --- | --- | --- |
| Same line | 2,102 | 0.176 | −0.111 | +0.29 |
| Line below | 2,352 | 0.147 | −0.101 | +0.25 |
| Far apart (≥ 4 lines) | 7,059 | 0.101 | −0.151 | +0.25 |

Vertical minus far: 95% CI −0.09 to +0.10 (page bootstrap). Machine-only similarity to the aligned word below, minus a random word on that line: +0.036 (1 line), +0.017 (2), +0.028 (3), +0.008 (5); SE about 0.007.

## Scribe model ("Brother Evagrius")

| Measure | Voynich | Evagrius | Evagrius + aversion 0.5 | Timm–Schinner |
| --- | --- | --- | --- | --- |
| Distinct words per word | 0.208 | 0.162 | 0.178 | 0.187 |
| Letter entropy (bits) | 2.11 | 1.88 | 1.95 | 2.03 |
| Next word exact repeat | 1.25× | 2.76× | 1.61× | 0.67× |
| Next word near-copy | 1.30× | 2.07× | 1.98× | 1.19× |
| Line below near-copy | 1.15× | 2.29× | 2.09× | 1.21× |
| Page vocabulary clustering | 2.33× | 2.66× | 3.04× | 1.24× |

Evagrius copies a recent word from his line or the line above and changes one or two glyphs; mutations must form glyph triplets seen in the Voynich. Aversion = re-mutate a word equal to one of the last four on the line, half the time (fit loss 166 → 62). This is the same rule the Timm–Schinner code uses.

## Failures

| Attempt | What went wrong | Consequence |
| --- | --- | --- |
| Pairing words by position in line | Same counts, different words (r = 0.09) | Replaced by coordinate pairing |
| First coordinate fit | Locked one line too low | Refit on full box overlap |
| Synthetic machine-error model | Destroyed the same-line effect the machine detects | Superseded by the ink test |
| Herbal pages | Plant stems faked vertical copying | Herbal machine data not used |
| Exact matches in machine spelling | 0.23× to 1.5× across syllabary versions | Only near-copies and ink similarity reported |

## Open questions

- Herbal and other sections, which need a segmenter that separates text from drawings.
- Homophonic and nomenclator ciphers, untested.
- A scribe model that keeps a large vocabulary while copying.

## Sources and data

- Takahashi EVA: [alephmembeth/voynich](https://github.com/alephmembeth/voynich)
- ZL3b, voynichese.com boxes, Timm–Schinner output, Naibbe controls, Italian/German/French corpora: [lrozanova/voynich-units](https://github.com/lrozanova/voynich-units)
- Naibbe cipher: Greshko, M. A. (2025), *Cryptologia*, [doi:10.1080/01611194.2025.2566408](https://doi.org/10.1080/01611194.2025.2566408)
- Scans (public domain, Beinecke MS 408): [sunkencity999/voynich-atlas](https://github.com/sunkencity999/voynich-atlas)
- Seraphinianus OCR: [marcoponzi/codex_seraphinianus_ocr](https://github.com/marcoponzi/codex_seraphinianus_ocr)
- Latin: [cltk/lat_text_latin_library](https://github.com/cltk/lat_text_latin_library); English: NLTK Gutenberg
