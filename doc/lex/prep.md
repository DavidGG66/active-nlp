
# Prepositions

There are three classes of prepositions, distinguished by how they are
incorporated semantically into the wider interpretation of the utterance:
Arguments, Noun adjuncts and Verb adjuncts

## Arguments

An argument preposition adds no semantics of its own - it only exists to
mark its object as a particular argument. For example:

I rely **on** her

Here, *on* serves only to mark *her* as something like the object of *rely*.
You could analyze particles, as in "I looked it **up**" as an intransitive form
of this preposition class.

### Intransitive
"up" as in "I looked it up"

```
syn: {"cat": "PrepLex",
      "pform": "up"}
sem: []
hooks: {},
subcat: []
```
The only information associated with an intransitive argument preposition is
the fact of its pform, namely, that it is the preposition 'up'.

### Transitive
"on" as in "I rely on her"

```
syn: {"cat": "PrepLex",
      "pform": "on"}
sem: []
hooks: {"root": "x1"}
subcat: [{"arg": "Object",
          "analyses": [{"cat": "NP",
	                "case": "acc"}],
          "hooks": {"root": "x1"}]
```
A transitive argument preposition has a subcategorized NP object. Its root
hook becomes the root hook of the PP headed by the preposition, which is what
the subcat of a verb like rely is looking for:

```
syn: {"cat": "Verb"}
sem: [{"rel": "Rely",
       "rolespecs": {"_EVENT": "x2",
                     "RELIER": "x3",
		     "RELIEDON": "x4"}}]
hooks: {"event": "x2",
        "subj": "x3"}
subcat: [{"arg": "PObject",
          "analyses": [{"cat": "PP",
	                "vform": "on"}],
	  "hooks": {"root": "x4"}}]
```

## Noun Adjuncts

A noun-adjunct preposition modifies a noun. For example:

- The light is **on**
- The book **in** the box

### Intransitive
"on" as in "the light is on"
```
syn: {"cat": "PrepLex"}
sem: [{"rel": "InOperation",
       "rolespecs": {"_EVENT": "x1",
                     "OPERATED": "x2"}}]
hooks: {"event": "x1",
        "head": "x2"}
subcat: []
```
An intransitive noun-adjunct preposition acts like an adjective - when applied
to a noun, its head hook is unified with the head hook of the noun.

### Transitive
"in" as in "the book in the box"
```
syn: {"cat": "PrepLex"}
sem: [{"rel": "Contains",
       "rolespecs": {"_EVENT": "x1",
                     "CONTAINED": "x2",
		     "CONTAINER": "x3"}}]
hooks: {"event": "x1",
        "head": "x2"}
subcat: [{"arg": "Object",
          "analyses": [{"cat": "NP",
	                "case": "acc"}],
	  "hooks": {"root": "x3"}}]
```
Transitive prepositions work just the same, except they subcategorize for an
NP object as well, in the same way transitive verbs do.

## Verb Adjuncts

A verb-adjunct preposition modifies a verb, by using that verb's event hook
in a relspec introduced by the preposition. For example:

I cooked **with** the pan

The semantics of the complete sentence is this:
```
[{"rel": "Cook",
  "rolespecs": {"_EVENT": "x1",
                "COOK": "x2 [I]"}},
 {"rel": "Instrument",
  "rolespecs": {"EVENT": "x1",
                "INSTRUMENT": "x3 [the pan]"}}]
```
The verb *cook* introduces the `Cook` relspec and the Preposition *with*
introduces the `Instrument` relspec. The `EVENT` index of `Instrument` is
identified with the `_EVENT` index of `Cook`.

### Intransitive
"yesterday" as in "I Cooked yesterday"
```
syn: {"cat": "PrepLex"}
sem: [{"rel": "EventYesterday",
       "rolespecs": {"EVENT": "x1"}}]
hooks: {"modevent": "x1"}
subcat: []
```
This edge exposes a modevent hook, meaning the event which is modified by this
relspec. The rule that combines a verb-adjunct PP to a verb requires this hook
in order to work. This prevents other types of PP from being interpreted as
this type

### Transitive
"with" as in "I cooked with the pan"
```
syn: {"cat": "PrepLex"}
sem: [{"rel": "Instrument",
       "rolespecs": {"EVENT": "x1",
                     "INSTRUMENT": "x2"}}]
hooks: {"modevent": "x1:}
subcat: [{"arg": "Object",
          "analyses": [{"cat": "NP",
                        "case": "acc"}],
          "hooks": {"root": "x2"}}]
```
Transitive prepositions are similar to intransitive ones, with the difference
that transitive prepositions subcategorize for an object.
