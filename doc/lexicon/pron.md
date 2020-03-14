
# Pronouns

Pronouns have very little semantics, and no subcategorized arguments. They are
differentiated from one another by their syntactic specifications.

"me" as in "Give it to me"
```
syn: {"cat": "PronLex",
      ...}
sem: [{"rel": "PronRel",
       "rolespecs": {"PRON": "x1"}}],
hooks: {"root": "x1"}
```

The system recognizes these classes of pronouns: Personal (which may be
animate or inanimate); Indexical (which may be scalar or quantificational); and
Wh.

## Personal pronouns

Syntactically, personal pronouns are marked as `{"personal": "+"}` and are
specified for the following features: `pers`, `agr`, `case` and `animate`.
Animate pronouns (marked `{"animate": "+"}`) are also specified for `gender`.

Here is a more complete version of the specification for the personal pronoun
"me":
```
syn: {"cat": "PronLex",
      "personal": "+",
      "pers": "1",
      "agr": {"sg": "+"},
      "case": "acc",
      "animate": "+",
      "gender": "any"}
sem: [{"rel": "PronRel",
       "rolespecs": {"PRON": "x1"}}],
hooks: {"root": "x1"}
```

### pers

This feature indicates the pronoun's person, 1st, 2nd or 3rd.

### agr

This holds the pronoun's number agreement information - a feature structure
with a single key: `sg`. Its value is "+" for singular-agreeing pronouns and
"-" for plural-agreeing pronouns.

### case

This is the pronoun's case, such as nominative or accusative. Case values are
arranged in this hierarchy:

```
"nom_acc" [
    "nom" - Nominative
    "acc" - Accusative]
"any_gen" [
    "gendet" - 'Determiner' genitive
    "gennp" - 'NP' genitive]
"refl" - Reflexive
```

So a pronoun whose case is `nom_acc` (such as 'you') works as either nominative
or accusative, and one marked as `any_gen` (such as 'his') works as either a
determiner-genitive or np-genitive.

Even with such a hierarchy, the pronoun "her" must have two entries, one for
accusative case, and one for determiner-genitive.

### gender

This is the pronoun's gender, which may be `masc`, `fem` or `any`. These values
are arranged in a hierarchy, so `any` works as `masc` or `fem`.

## Indexical pronouns

Syntactically, indexical pronouns are marked as {"indexical": "+"} and are
specified for the feature `dim` and either `loc` or `quant`.

### dim

This is the dimension along which the indexical operates. Possible values are
`geo` (geographical), for pronouns like "here" and "everywhere"; `temp`
(temporal), for pronouns like "then" and "never"; `pers` (personal), for
pronouns like "someone" and "everybody"

### loc

Scalar indexical pronouns mark a specific distance along the dimension. Values
are either `prox` (proximal), for pronouns like "here" and "now"; or `dist`
(distal), for pronouns like "there" and "then"

For example, the edge created from the entry for "here":
```
syn: {"cat": "PronLex",
      "indexical": "+",
      "dim": "geo",
      "loc": "prox"}
```

### quant

Quantificational pronouns specify some quantity of the dimension. Values can be
`exist` (existential), for pronouns like "somewhere" or "somebody"; `univ`
(universal), for pronouns like "always" and "everyone", `negpol` (negative
polarity existential), for pronouns like "anywhere" and "anybody"; and `none`
(anti-universal), for pronouns like "never" and "nobody".

For example, the edge for "somebody":
```
syn: {"cat": "PronLex",
      "indexical": "+",
      "dim": "pers",
      "quant": "exist"}
```

## WH pronouns

WH pronouns are specified for these syntactic features: `wh_type`, `agr`,
`case` and `animate`. Here is the edge for "what" as a example:
```
syn: {"cat": "PronLex",
      "wh_type": "ques",
      "agr": {"plu": "-",
              "sg": "+"},
      "case": "nom_acc",
      "animate": "-"}
```

### wh_type

Values for this feature are `ques` (question), `comp` (complementizer), or
`any`, which works as either.

### agr

A number agreement structure with features `plu` and `sg`.

### case

The same possibilities as for personal pronouns

### animate

values are `+`, `-` or `any`
