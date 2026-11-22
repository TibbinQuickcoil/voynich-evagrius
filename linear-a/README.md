# Linear A: does it repeat like a language?

*Part of [the Untranslatable Archive](../README.md).*

**Short answer: yes.** Linear A avoids repeating a word or sign back to back, just like Linear B, its deciphered cousin, which records an early form of Greek. On this test it looks like a real language.

## What Linear A is

The script of Minoan Crete, used about 1800–1450 BC, mostly on clay tablets recording goods: names, commodities and numbers. Linear B was adapted from it to write Greek and was deciphered in 1952. Many Linear A signs can be sounded out using Linear B values, but the words don't match any known language, so it stays unread.

## Why Linear B makes the perfect control

Both scripts were used for the same thing, palace bookkeeping, in nearly the same way. So any difference between them can't come from genre or format. Linear B is known to be a real language, Greek.

| Text | Unit | Same unit twice in a row, observed ÷ chance |
| --- | --- | --- |
| Linear B (Greek, deciphered) | words | 0.25× |
| **Linear A (undeciphered)** | **words** | **0.38×** |
| Linear B (Greek, deciphered) | syllable signs | 0.48× |
| **Linear A (undeciphered)** | **syllable signs** | **0.66×** |

Linear A's word figure is significantly below chance (p ≈ 0.05; the corpus is small, 589 words) and its sign figure is clearly below (p ≈ 0.002). It behaves like Linear B and unlike the Voynich (1.26–1.30×).

One oddity: neighboring Linear A words are one sign different more often than chance (1.44×, p ≈ 0.05). In bookkeeping lists, related names and forms of one word often sit together, so this isn't surprising, but it's worth a closer look.

## Data and limits

- **Corpus:** inscriptions from [mwenge/lineara.xyz](https://github.com/mwenge/lineara.xyz) and [mwenge/linearb.xyz](https://github.com/mwenge/linearb.xyz). Only words of two or more syllable signs were used, so commodity symbols and numbers were left out.
- Word order is the order of entries in each inscription. Shuffles are within each inscription, 500 times.
- The test only says Linear A behaves like a language. It says nothing about which language.
- Done with AI assistance (Claude); code in `code/`.
