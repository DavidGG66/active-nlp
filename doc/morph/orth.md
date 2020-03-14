
# Orthographic Transducers

Finite-state transducers are used to model orthographic alternations, such as
the doubling of consonants before a vowel-initial suffix, e.g. "stop" vs
"stopping" or the use of "es" rather than "s" as the plural suffix sometimes,
e.g. "dogs" vs "foxes".

We have an FST for each of these individual rules, and they are combined in
various ways to create the FST `src.morph.orth.full`, which is the overarching
FST that handles all the orthographical rules.

In the namespace `src.morph.orth`, the `full` FST is the union of the FSTs
`free`, `pre_vowel`, `takes_es`, takes_s` and `punc`. It is the result of
calling `src.morph.fst.non_det_or_fst` on those five FSTs.

## free

This FST recognizes any string at all as being a free morpheme. That is, no
matter what a lexeme looks like, if it appears without any affixes, its surface
form will look just like its deep form. The