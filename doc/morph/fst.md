
# Finite State Transducers

A finite state transducer implements a binary relation between strings, which
can be used to translate a string into a set of strings.

An FST is considered a finite state automaton (FSA) if all its pairs are of the
form (X, X). That is, if a string is in the relation at all, it is related to
only itself. An FSA doesn't serve so much as a way to translate strings, but
rather just to tell whether a given string (word) is in a particular set
(lexicon).

This documentation assumes familiarity with the structure of an FST, with
states (initial, final and otherwise), arcs and labels, and how it is that it
defines a relation between strings.

## FST members

An FST consists of a collection of states; an initial state; a set of final
states; and a next state.

### State map

An FST object includes a `states` member, which is a map from integers to
`State` objects. The integer is the state's number, which is how other objects
refer to the state.

A newly created FST will contain one state, state 0. The `states` map will have
the single key 0, which points to a default `State` object.

### Initial state

An FST object includes an `initial` member, which is the number of the initial
state. This starts out as 0 for a new FST.

### Final states

An FST indicates which of its states are final. But rather than having just a
set including all the final states, here we have a member, `finals`, which is a
map from state numbers to sets of tags. The tags indicate lexical classes that
the corresponding word belongs in.

For instance, in the FST src.morph.orth.det_full, the final state that
recognizes the pair 'dog':'dog' is associated with the tags 'free' and 'takesS'.
The final state that recognizes the pair 'dog':'doge' is associated with the tag
'preVowel'. That is, surface "dog" can mean underlying "dog" for a standalone
word, or as a root that takes the 's' suffix. Surface "dog" could also mea
underlying "doge" that comes before a suffix that starts with a vowel.

### Next state

As new states are added to an FST, it is handy to keep track of the number that
is to be assigned to the next new state. This number is stored in the member
`next`. Whenever a new state is added, this number is used and then incremented.

## States

State objects are identified by integers, but only in the sense that they are
the values pointed to by integer keys in the `states` map in an FST object. The
integers are not stored with the states themselves.

States have only one data member, `arc_map`, which contains the arcs leading
from the state to some target state. This is a map from the target state to
an Arc object.

## Arcs

An arc stores the target state (in the member `target`), and the label. A label
can have two types of components, `units` and `pairs`.

### Units

The `units` member is a set of strings. If a string appears in this set, then
this arc can be taken with that string as an input, giving that same string as
an output.

### Pairs

The `pairs` member is a set of ordered pairs (2-tuples), where the first item is
the input string and the second item is the output string. Either of these may
be the special string `epsilon`, with the expected meaning.

## FST Methods

The main thing you can do with an FST is to analyze a string in order to get
the set of strings (and associated tags) it translates to. Ultimately, you will
also be able to use an FST to generate strings, which is just translating them
in the other direction.

The parsing code includes a function that uses two FSTs in parallel. That
function makes use of methods that analyze a single character at a time.

### Analyze a string

The `analyze` method takes an utterance (as a string) and returns a map from
translation strings to sets of tags. For instance,
`src.morph.orth.full.analyze("dog")` gives us this:

```
{'dog': {'free', 'takesS'},
 'doge': {'preVowel'}}
```
This indicates that, according to the FST src.morph.orth.full, the FST that
implements orthographic alternation rules, surface "dog" could come from an
underlying lexeme "dog" as either a free morpheme or as a root that takes an 'S'
suffix; or it could come from an underlying lexeme "doge" as a root that comes
before a suffix that starts with a vowel.

And `src.lexicon.load.lex_fsa.analyze("dog")` gives us this:
```
{'dog': {'noun'}}
```
This indicates that, according to src.lexicon.load.lex_fsa, the FSA that stores
the lexicon, "dog" is in the lexicon as a noun.

### Analyze a single character

The `analyze_character` method of FST takes a state number and a character and
returns a list of pairs, where each pair is the result of following an arc from
the input state. Each pair consists of a target state and the list of characters
associated with the input character. Normally this will be a single character,
but could be zero or more than one, depending on epsilon arcs. For instance,
`src.morph.orth.full.analyze_character(0, 'd')` gives
```
[(1, ['d']),
 (3, ['d']),
 (7, ['d']),
 (12, ['d']),
 (2, ['d', 'e'])]
```

### Analyze characters with an FSA

The `analyze_fsa_characters` assumes its FST is an FSA. It takes a state of that
FSA and a list of characters. It follows all possible paths from that state
using those characters, and returns the list of resulting states. It doesn't
keep track of output characters, because in an FSA that will always be the same
as the input characters. For instance,
`src.lexicon.load.lex_fsa.anayze_fsa_characters(0, "dog")` gives
```
[15]
```

## FST Creation Functions

This file contains several functions that return FSTs: `word_fst`, `read_fst`,
`and_fst`, `or_fst`, `non_det_or_fst` and `extend_fsa`.

### word_fst

The function `word_fst` takes a single word and a tag, and returns an FST that
recognizes just that word with a tag list containing just that tag. For
instance, `word_fst("dog", "noun")` returns
```
states: {0: {arc_map: {1: {target: 1,
                           units: ["d"]}}},
         1: {arc_map: {2: {target: 2,
	                   units: ["o"]}}},
	 2: {arc_map: {3: {target: 3,
	                   units: ["g"]}}},
	 3: {arc_map: {}}},
initial: 0,
finals: {3: {"noun"}},
next: 4
```
Note: The above FST can be abbreviated with the notation below. Such
abbreviation will be used from now on:
```
states: {0: {1: ["d"]},
         1: {2: ["o"]},
	 2: {3: ["g"]},
	 3: {}},
initial: 0,
finals: {3: {"noun"}}
```
This FST is an FSA that recognizes the word "dog", associated with the tag set
`{"noun"}`.

### read_fst

The function `read_fst` takes a dictionary structure and returns the
corresponding FST. The sort of dictionary structure it expects is like this one:
```
{"finals": {
     0: {"preVowel"},
     2: {"preVowel"}},
 "next": 3,
 "states": {
     0: {0: "abcdfghijklmnopqrstuvwxyz",
         1: "e",
         2: ("e", "epsilon")},
     1: {0: "abcdfghijklmnopqrstuvwxyz",
         1: "e",
         2: ("e", "epsilon")},
     2: {}}}
```
The semantics of this structure are as expected. This FST deletes a stem-final
"e" for when the stem appears before a vowel-initial suffix.

### and_fst

The function `and_fst` takes two FSTs and returns a new FST. In terms of an FST
as a relation between strings, this new FST contains just those pairs that
appear in both the input FSTs. Running the new FST is equivalent to running each
of the input FSTs in parallel.

### or_fst

The function `or_fst` takes two FSTs and returns a new FST. As a relation
between strings, the new FST contains any pair that appears in either of the
input FSTs.

### non_det_or_fst

The function `non_det_or_fst` has the same functionality as `or_fst`. The
resulting FST recognizes the same strings, but with potentially more
non-determinism, which can make for a smaller FST, built more simply, but can
take longer to analyze strings with.

### extend_fsa

The function `extend_fsa` takes an existing FST (which it assumes is an FSA),
a word (as a string) and a tag set (either a string or a set of strings). It
returns a new FST which returns everything the input FST did, plus the new word,
with its tag set.