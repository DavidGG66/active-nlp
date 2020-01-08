# Determiners

## Quantification

Determiners are part of how quantification is determined in a noun phrase. So
before we specify how determiners are stored/produced in the lexicon, we should
take a look at how quantification works in the semantics.

### Noun and Verb Phrase signs

Let's take a look at two signs, one for the string "dog", and one for the string
"barks":

```
The noun "dog"
{"syn_val": {"cat": "Noun",
             "agr": {"plu": "-",
                     "sg": "+"}},
 "sem_val": [{"rel: "Dog",
              "rolespecs": {"_EVENT": "x1",
                            "DOG": "x2"}},
             {"rel": "AbsVal",
              "rolespecs": {"NODE": "x3",
                            "VAL": 1}}],
 "hooks": {"event": "x1",
           "head": "x2",
           "quant": "x3"}}

The verb "barks" (tense information not shown)
{"syn_val": {"cat": "Verb",
             "agr": {"pers": "3",
                     "sg": "+"}},
 "sem_val": [{"rel": "Bark",
              "rolespecs": {"_EVENT": "x4",
                            "BARKER": "x5"}}],
 "hooks": {"event": "x4",
           "subj": "x5"}}
```

You can think of the *head* hook of the "dog" sign (x2) as meaning something
like the set of dogs, and the *subj* hook of the "bark" sign (x5)  as the set of
barkers. Semantically, a quantifier specifies a relationship between these two
hooks.

### The quantifying relationship

The relationship between the sets represented by a subject noun and a predicate
verb phrase are of two main sorts, "absolute" quantification and "relative"
quantification. The first counts the absolute number of things in the
intersection of the two sets, and the second looks at the ratio of things in
that intersection to things just in the noun set.

#### Absolute quantification

Absolute quantification only cares about the intersection between the subject
noun's set (called the *restriction*) and the verb phrase's set (called the
*nuclear scope*). An absolute quantifier describes the number of items in that
intersection

An example of an absolute quantifier in english is "a", as in the phrase "a dog
barks". It says that the intersection of the restriction (the set of dogs) and
the nuclear scope (the set of barkers) is one. Here is the sign for "a dog
barks":

```
{"syn_val": {"cat": "S",
             "args": [{"arg": "Subject",
                       "node": <see above>},
                      {"arg": "Predicate",
                       "node": <see above>}]},
 "sem_val": [{"rel": "Bark",
              "rolespecs": {"_EVENT": "x4",
                            "BARKER": "x5"}},
             {"rel": "Dog",
              "rolespecs": {"_EVENT": "x1",
                            "DOG": "x2"}},
             {"rel": "Quant",
              "rolespecs": {"RESTR": "x2",
                            "SCOPE": "x5",
                            "QUANT": "x3"}},
             {"rel": "AbsVal",
              "rolespecs": {"NODE": "x3",
                            "VAL": 1}}],
 "hooks": {"event": "x4"}}
```
In the `sem_val` above, the determiner "a" introduced the `Quant` relspec, which
specifies the proper restriction and nuclear scope. It also has a `QUANT` role,
which connects to the `AbsVal` relspec provided by the noun, which it in turn
got from being in its singular form. This AbsVal relspec asserts that `x3` has
the "absolute" value 1. All together, this structure asserts that the
intersection between the dogs and the barkers contains 1 element.

#### Relative quantification

Relative quantification cares about the ratio between the number of things in
the intersection between the restriction and the nuclear scope, and the number
of things just in the restriction. This ratio can range from 0 to 1, where the
value is 0 for "no dog barks" and the value is 1 for "every dog barks". Here is
the sign for "every dog barks":

```
{"syn_val": {"cat": "S",
             "args": [{"arg": "Subject",
                       "node": <see above>},
                      {"arg": "Predicate",
                       "node": <see above>}]},
 "sem_val": [{"rel": "Bark",
              "rolespecs": {"_EVENT": "x4",
                            "BARKER": "x5"}},
             {"rel": "Dog",
              "rolespecs": {"_EVENT": "x1",
                            "DOG": "x2"}},
             {"rel": "Quant",
              "rolespecs": {"RESTR": "x2",
                            "SCOPE": "x5",
                            "QUANT": "x3"}},
             {"rel": "RelVal",
              "rolespecs": {"NODE": "x3",
                            "VAL": 1}}],
 "hooks": {"event": "x4"}}
```
This structure is exactly the same as the one for "a dog barks", except the
`QUANT` role is filled by a relative value (`RelVal`) rather than an absolute
value (`AbsVal`).
(CONSIDER: Have an indication in the Quant relspec itself about whether this is
absolute or relative quantification)

## Determiners in the lexicon

Determiners are stored in the lexicon according to the following pattern.
Different ways of filling in the properties marked *val* correspond to different
types of determiners:

```
{"syn_val": {"cat": "DetLex",
             "quant": *val*,
	     "agr": {"sg": *val*,
                     "pl": *val*}},
 "sem_val": [{"rel": "Quant",
              "rolespecs": {"RESTR": "x1",
                            "SCOPE": "x2",
                            "QUANT": "x3",
                            "DEF": *val*,
                            "WIDTH": *val*}}],
 "hooks": {"head": "x1",
           "root": "x2",
	   "quant": "x3"}}
```
### Agreement

Determiners must agree in number with their head nouns. The syn_val for a
determiner includes an `agr` property which is itself a structure specifying a
value for `sg` and a value for `pl`. It is this `agr` property which must unify
with the `agr` property of the noun in order for the determiner to be allowed to
combine with the noun. See the description of Noun number for the details of
what this `agr` value means, but the purpose is so that we predict the following
sorts of facts:

```
A dog
* A dogs
* A sand
* All dog
All dogs
All sand
That dog
* That dogs
That sand
The dog
The dogs
The sand
```

### Open vs. fixed determiners

Normally, a determiner carries its own quantity. For instance, "a" is an
absolute quantifier with the (absolute) quantity 1, and "each" is a relative
quantifier with the (relative) quantity 1. We don't need to look at the
grammatical number of the noun. These are examples of *fixed* determiners.

On the other hand, a determiner like "the" is not specified for number. The
quantity must come from the number specification on the noun. Determiners like
that are *open* determiners.

Some determiners which must agree in grammatical number with their nouns can be
handled either way. However, we cannot just make every determiner an open
determiner. The determiner "every" must agree with a singular noun, where the
determiner "all" must agree with a plural noun. Yet they indicate the same
quantity, a relative quantity of 1. Therefore, the cannot get their quantity
from the number of the noun.

In the lexicon, a fixed determiner will have the `quant` property of its syn_val
set to "fixed", and an open determiner will have its set to "open".

### Definiteness

In a quantified noun phrase, the semantic value of the head noun provides the
restriction set. So in the sentence "A dog barks" means that the intersection
between the restriction, the set of dogs; and the nuclear scope, the set of
barkers; contains one element. But of course it is probably never really true
that the set of *all* dogs, intersected with the set of barkers yields just one
element. We just mean the set of dogs *of interest in the current context*.

So the restriction set is restricted not just by the semantics of the noun, but
also by the conversational context. Some determiners, namely the *definite*
determiners restrict the restriction set even further. For instance, in the
sentence "the dog barks", the determiner "the" restricts the restriction set to
a single element, the one that is most salient in the current context, whatever
the definition of "salient" might be at the given time. To represent this, the
`Quant` relationship has a role `DEF` which specifies how the restriction set
should be further restricted. Here is the sign for the definite determiner
"the":

```
{"syn_val": {"cat": "DetLex",
             "quant": "open",
	     "agr": {"sg": "any",
                     "pl": "any"}},
 "sem_val": [{"rel": "Quant",
              "rolespecs": {"RESTR": "x1",
                            "SCOPE": "x2",
                            "QUANT": "x3",
                            "DEF": "definite",
                            "WIDTH": "narrow"}}],
 "hooks": {"head": "x1",
           "root": "x2",
	   "quant": "x3"}}
```
The `Quant` relspec is specified as `"DEF": "definite"`, indicating that the
restriction set (dogs) should be restricted such that its cardinality matches
the (absolute) value of its `QUANT` role somehow.

Other values of the `DEF` role are more specific about how that restriction
should be done. For instance, the `DEF` role for the determiner "this" is
'proximal', meaning to restrict the restriction set based on immediate
proximity.

### Width

This refers to whether a quantifying determiner typically takes wide scope or
narrow scope. The possible values are "narrow" and "wide".

## Loading determiners

Each determiner in the lexicon is stored as a lexical specification with one of
three lexical functions: `abs_det_entry`, `rel_det_entry` and `open_det_entry`.

### abs_det_entry

This creates a (fixed) absolute quantifier. Its arguments are `sg`, `plu`, `df`,
`width` and `val`. `sg` and `plu` specify the agreement features, `df` is the
definiteness, i.e. the value of the `DEF` role of the `Quant` relspec. `val` is
the value, i.e. the number that fills the `VAL` role of the `AbsVal` relspec.

```
"a" ("+", "-", "indef", "narrow", 1)
```
### rel_det_entry

This creates a relative quantifier. Its arguments are `sg`, `plu`, `width` and
`val`. They have the same meanings as for `abs_det_entry` above, except `val`
refers to the `VAL` role of the `RelVal` relspec. All relative-quantifier
determiners are fixed and are indefinite.

```
"all"   ("any", "+", "narrow", 1)
"each"  ("+", "-", "wide", 1)
"every" ("+", "-", "narrow", 1)
```

### open_det_entry

This creates an open (absolute) quantifier. Its arguments are `sg`, `plu`, `df`
and `width`. No `val` argument is needed, since an open determiner gets its
quantity from the number of the head noun.

```
"some"  ("any", "any", "indef", "narrow")
"that"  ("+", "any", "distal", "narrow")
"the"   ("any", "any", "definite", "narrow")
"those" ("-", "+", "distal", "narrow")
```
