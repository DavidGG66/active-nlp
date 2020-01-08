# Nouns

## Typical Noun lexical entries

Here is the sign representing the lexical entry for the noun "dog":

```
{"syn_val": {"cat": "NounLex",
             "quantType": "count",
             "plural": False,
             "regPlu": True},
 "sem_val": [{"rel": "Dog",
              "rolespecs": {"_EVENT": "x1",
                            "DOG": "x2"}}],
 "hooks": {"event": "x1",
           "head": "x2"}}
```
Every noun's lexical entry with have syntactic category `NounLex`. `quantType`
distinguishes count nouns, like "dog" from mass nouns like "paint". A count noun
will also have a value for `plural`, either `True` or `False`. Finally, `regPlu`
tells whether the noun pluralizes in a regular fashion. This is set to True for
singular nouns which take regular plurals, False for singular nouns that take
irregular plurals, or for those irregular plurals themselves.

A typical noun is expected to have an event hook and a head hook. Normally, the
semantic value of the noun contains a single relspec. The value of its `_EVENT`
role is the event hook, and the value of the other role is the head hook.

## NounLex to Noun

A noun's lexical entry has the syntactic category `NounLex`. Grammatical rules
take the raw information in the lexical entry and create a true grammatical
sign. This includes a syntactic `agr` property, and the inclusion of a value
relspec corresponding to the syntactic number. For instance, the rule that turns
a bare-form NounLex into a singular noun produces the following sign from the
about NounLex sign for "dog":

```
{"syn_val": {"cat": "Noun",
             "agr": {"plu": "-",
	             "sg": "+"}},
 "sem_val": [{"rel": "Dog",
              "rolespecs": {"_EVENT": "x1",
                            "DOG": "x2"}},
             {"rel": "AbsVal",
              "rolespecs": {"NODE": "x3",
                            "VAL": 1}}],
 "hooks": {"event": "x1",
           "head": "x2",
           "quant": "x3"}}
```
There are three lexical functions that can turn a lexical specification for a
noun into a lexical entry: `count_noun_entry`, `irr_count_noun_entry` and
`mass_noun_entry`.

## count_noun_entry

This function creates a regular count noun entry, like the above one for "dog".
Its arguments are `rel` and `role`, the semantic relationship and its head role.

## irr_count_noun_entry

This function creates an irregular count noun entry. Its arguments are `rel`,
`role` and `plural`. The `plural` argument is true for irregular plural forms,
and false for singular forms.

## mass_noun_entry

This function creates a mass noun entry. It's arguments are `rel` and `role`.
