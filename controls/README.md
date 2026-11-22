# Controls: what languages, ciphers and nonsense look like on the test

*Part of [the Untranslatable Archive](../README.md).*

Every undeciphered text here is judged against texts whose nature is known.

| Text | Kind | Same word twice in a row, observed ÷ chance |
| --- | --- | --- |
| Latin (Pliny, Vulgate) | language | 0.02–0.06× |
| German | language | 0.03× |
| Māori | language (Polynesian) | 0.04× |
| French | language | 0.11× |
| English (*Moby Dick*) | language | 0.14× |
| Italian | language | 0.22× |
| Linear B | language (Mycenaean Greek) | 0.25× |
| Homophonic cipher of Latin | cipher | 0.00× |
| Naibbe cipher of Latin | cipher | 0.33–0.37× |
| Timm–Schinner generator | generated nonsense | 0.45–0.92× |
| *Codex Seraphinianus* | human-made nonsense | 1.25× |

## The ciphers

- A **homophonic cipher** gives common letters several interchangeable symbols chosen at random. It makes repeats even rarer (0.00×, near-copies 0.30–0.34×), because the same word comes out spelled differently each time. Tested here on Pliny with 68 and 125 symbols.
- A **nomenclator** swaps common words for fixed code words. It keeps the original word order exactly, so it inherits the language's avoidance of repeats; no test needed.
- The **Naibbe cipher** ([Greshko 2025](https://doi.org/10.1080/01611194.2025.2566408)) is the leading published proposal for how the Voynich could encode Latin. It still sits below chance.

None of these can turn a real language into above-chance repetition. A cipher padded on purpose with repeated filler words could, but none like that has been proposed for these texts.

## Sources

Latin from the Latin Library; English from NLTK Gutenberg; Italian, German and French from [lrozanova/voynich-units](https://github.com/lrozanova/voynich-units); Māori from [douglasbagnall/mi.wikipedia](https://github.com/douglasbagnall/mi.wikipedia); Linear B from [mwenge/linearb.xyz](https://github.com/mwenge/linearb.xyz); Naibbe and Timm–Schinner output from lrozanova/voynich-units; *Codex Seraphinianus* OCR from [marcoponzi/codex_seraphinianus_ocr](https://github.com/marcoponzi/codex_seraphinianus_ocr). Shuffles stay within each line, sentence, page or inscription. Every number is in [`all_results.json`](all_results.json).
