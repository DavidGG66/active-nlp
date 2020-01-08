# Lexicon

The lexicon is stored in the variable src.lexicon.load.lexicon. it is a
dictionary from morpheme strings to a list of lexical specifications.

Each lexical specification includes a string associated with a function name,
and a list of arguments. Applying that function to those arguments returns a
sign corresponding to the lexical entry of the relevant morpheme.

For instance, the value of `lexicon["with"]` is this list of lexical
specifications:

```
[["prep:adj-trans", "Own", "OWNER", "OWNED"],
 ["prep:adv-trans", "Instrument", "EVENT", "INSTRUMENT"]]
```
The first says you can get one lexical entry for "with" by applying the function
associated with `prep:adj-trans` to the arguments `"Own"`, `"OWNER"` and
`"OWNED"`. The second says you can get one by applying the function associated
with `prep:adv-trans` to `"Instrument"`, `"EVENT"` and `"INSTRUMENT"`.

The resulting lexical entries are the these two signs, respectively:

```
{"syn_val": {"cat": "PrepLex"},
 "sem_val": [{"rel": "Own",
              "rolespecs": {"_EVENT": "x1",
                            "OWNER": "x2",
                            "OWNED": "x3"}}],
 "hooks": {"event": "x1",
           "head": "x2"},
 "subcat": [{"arg": "Object",
             "analyses": [{"cat": "NP",
                           "case": "acc"}],
             "hooks": {"root": "x3"},
             "optional": False}]}

{"syn_val": {"cat": "PrepLex"},
 "sem_val": [{"rel": "Instrument",
              "rolespecs": {"EVENT": "x1",
                            "INSTRUMENT": "x2"}}],
 "hooks": {"modevent": "x1"},
 "subcat": [{"arg": "Object",
             "analyses": [{"cat": "NP",
                           "case": "acc"}],
             "hooks": {"root": "x2"},
	     "optional": False}]}
```

The lexicon stores lexical specifications rather than full-blown lexical entries
in order to save memory. The trade-off is the time it takes to "reconstitute"
the entries from the specifications.

The identifiers of the lexical functions have the structure *pos*:*name", with a
part-of-speech followed by a colon, followed by a specific name. Each lexical
function identifier, the associated function, and how that function transforms
its arguments into a sign, is explained in the documentation file connected with
its particular part of speech.