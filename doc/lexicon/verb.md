
# Verbs

The lexicon stores information about the lexical forms of verbs, and the
syntax-semantics interface of verbs

## Lexical verb forms

Each verb lexeme keeps track of its lexical form in the syntactic feature
`vform`, whose values are

- bare     ("be",   "eat",   "have",   "know",  "walk")
- plPres   ("are"   -        -         -        -)
- 1sgPres  ("am"    -        -         -        -)
- 3sgPres  ("is"    -        "has"     -        -)
- past     (-       "ate",   "had",    "knew"   -)
- sgPast   ("was"   -        -         -        -)
- plPast   ("were"  -        -         -        -)
- pastPart ("been", "eaten"  -         "known"  -)

Each of these verb forms combine with suffixes, or get promoted directly, to
make verbs with particular syntactic features - see the documentation for verb
rules.

On any bare-form verb lexeme, there are 5 features that keep track of what, if
any, irregular forms that verb has. For example, here is the syntax for the
edge for the verb "eat":
```
syn: {"cat": "VerbLex",
      "vform": "bare",
      "irr1st": "-",
      "irr3ps": "-",
      "irrPast": "+",
      "irrPerf": "+",
      "irrPlu": "-"}
```

These specifications say that "eat" does not have an irregular 1st person or
second person present form, nor an irregular plural form, but it does have an
irregular past and an irregular perfect. This setting will prevent from firing
the rule that adds 'ed' to a bare form to make a past or a perfect verb.

## Syntax-semantics interface

The semantics of a verb typically consists of a single relspec. There are
`event` and `subj` hooks, and `subcat` entries for arguments of the verb.
As an example, here is the edge for the entry for "ate":
```
syn: {"cat": "VerbLex",
      "vform": "past"}
sem: [{"rel": "Eat",
       "rolespecs": {"_EVENT": "x1",
                      "EATER": "x2",
       		      "EATEN": "x3"}}]
hooks: {"event": "x1",
        "subj": "x2"}
subcat: [{"arg": "Object",
          "analyses": [{"cat": "NP",
	                "case": "acc"}],
	  "hooks": {"root": "x3"},
	  "optional": False}]
```

This says "ate" is a `past` form verb lexeme whose meaning is an "Eat" event,
where the subject of the verb is the eater and the object of the verb is the
eaten thing.

There are a number of distinct categories that verbs fall into, where each
category determines the set of things the verb subcategorizes for. They are
intransitive, transitive, inchoative, ditransitive, intransitive with prep
phrase, transitive with particle, subject raising, subject equi and copula.

### intransitive

An intransitive verb has only a "subj" hook, with no subcategorized arguments.
As an example, "smoke":
```
syn: {"cat": "VerbLex"}
sem: [{"rel": "Smoke",
       "rolespecs": {"_EVENT": "x1",
                     "SMOKER": "x2"}}]
hooks: {"event": "x1",
        "subj": "x2"}
subcat: []
```
### transitive

A transitive verb has a subject and a subcategorized object. As an example,
"chase":
```
syn: {"cat": "VerbLex"}
sem: [{"rel": "Chase",
       "rolespecs": {"_EVENT": "x1",
                     "CHASER": "x2",
		     "CHASED": "x3"}}],
hooks: {"event": "x1",
        "subj": "x2"}
subcat: [{"arg": "Object",
          "analyses": [{"cat": "NP",
                        "case": "acc"}],
          "hooks": {"root": "x3"},
          "optional": False}]
```
The root hook of the object, which must be an NP in accusative case, points to
the chased thing in the semantics. Note that this object is marked as
`{"optional": False}`, which means it must appear in order to make a well-formed
verb phrase (* "I chased"). Some verbs, such as "eat" are marked True for this
feature. ("I ate the cookie", "I ate").

### inchoative

Some verbs have more than one related semantic frame. For instance, the verb
"stop" has both an intransitive frame, where the subject is the thing that
ceases activity ("the machine stopped"), and a transitive frame, where the
subject causes something to stop ("Terry stopped the machine"). Here are the
two edges for "stop":
```
syn: {"cat": "VerbLex"},
sem: [{"rel": "Stop",
       "rolespecs": {"_EVENT": "x1",
                     "STOPPED": "x2"}}]
hooks: {"event": "x1",
        "subj": "x2"}
subcat: []

-----

syn: {"cat": "VerbLex"}
sem: [{"rel": "Cause",
       "rolespecs": {"_EVENT": "x1",
                     "CAUSER": "x2",
		     "CAUSED": "x3"}},
      {"rel": "Stop",
       "rolespecs": {"_EVENT": "x3",
                     "STOPPED": "x4}}],
hooks: {"event": "x1",
        "subj": "x2"}
subcat: [{"arg": "Object",
          "analyses": [{"cat": "NP",
                        "case": "acc"}],
          "hooks": {"root": "x4"},
          "optional": False}]
```

There are two relspecs in the semantics for the transitive frame, a "Cause"
and a "Stop" relspec. The caused thing in the Cause relspec is the Stop event
itself. The `subj` hook points to the causer, and the root hook of the Object
points to the stopped thing

### ditransitive

Ditransitive verbs take two objects. An example is "tell":
```
syn: {"cat": "VerbLex"}
sem: [{"rel": "Tell",
       "rolespecs": {"_EVENT": "x1",
                     "TELLER": "x2",
		     "TELLEE": "x3",
                     "TOLD": "x4"}}],
hooks: {"event": "x1",
        "subj": "x2"}
subcat: [{"arg": "Object",
          "analyses": [{"cat": "NP",
                        "case": "acc"}],
          "hooks": {"root": "x3"},
          "optional": False},
         {"arg": "Object",
          "analyses": [{"cat": "NP",
                        "case": "acc"}],
          "hooks": {"root": "x4"},
          "optional": False}]
```

### intransitive with prep phrase

Some verbs subcategorize for a prepositional phrase. Here is an example with
the verb "rely", as in "rely on the alarm clock":

```
syn: {"cat": "VerbLex"}
sem: [{"rel": "Rely",
       "rolespecs": {"_EVENT": "x1",
                     "RELIER": "x2",
                     "RELIEDON": "x3"}}]
hooks: {"event": "x1",
        "subj": "x2"}
subcat: [{"arg": "PPObj",
          "analyses": [{"cat": "PP",
                        "pform": "on"}],
          "hooks": {"root": "x3"}}]
```
The subcat here says it can use an "on" PP as a PPObj argument. The root hook
of that PP points to the relied-on thing in the semantics. Here is the
appropriate entry for "on" which enables such a PP:
```
syn: {"cat": "PrepLex",
      "pform": "on"},
sem: [],
hooks: {"root": "x1"},
subcat: [{"arg": "Object",
          "analyses": [{"cat": "NP"}],
          "hooks": {"root": "x1"},
          "optional": False}]
```
The root of the object of the preposition becomes the root of the PP itself.

### transitive with particle

A verb can subcategorize for a particle as well as an object. This is the case
for the verb "turn", as in "turn on the alarm clock":
```
syn: {"cat": "VerbLex"}
sem: [{"rel": "TurnOn",
       "rolespecs": {"_EVENT": "x1",
                     "TURNER": "x2",
                     "TURNED": "x3"}}]
hooks: {"event": "x1",
        "subj": "x2"}
subcat: [{"arg": "Particle",
          "analyses": [{"cat": "Prep",
                        "pform": "on"}],
          "hooks": {},
          "optional": False},
         {"arg": "Object",
          "analyses": [{"cat": "NP",
                        "case": "acc"}],
          "hooks": {"root": "x3"},
          "optional": False}]
```
The particle argument is just a preposition - not a prepositional phrase. In
some cases it can appear either before or after the object ("turn on the alarm
clock", "turn the alarm clock on").

### subject raising

Some verbs take VP arguments. One type of verb that does this is the
subject-raising verb, such as "seem":
```
syn: {"cat": "VerbLex"}
sem: [{"rel": "Seem",
       "rolespecs": {"_EVENT": "x1",
                     "SEEMED": "x3"}}],
hooks: {"event": "x1",
        "subj": "x2"}
subcat: [{"arg": "VPObj",
          "analyses": [{"cat": "VP",
                        "form": "infinitive"}],
          "hooks": {"event": "x3",
                    "subj": "x2"}}]
```
Note here that the `subj` hook of "seem" ("x2") does not appear in the `Seem`
relationship itself. Rather, it is identified with the `subj` hook of the
subcategorized VP object.

### subject equi

Another verb that seems to fit the same pattern as raising, but doesn't, is the
subject-equi verb, such as "want", as in "They want to eat it":
```
syn: {"cat": "VerbLex"}
sem: [{"rel": "Want",
       "rolespecs": {"_EVENT": "x1",
                     "WANTER": "x2",
                     "WANTED": "x3"}}],
hooks: {"event": "x1",
        "subj": "x2"}
subcat: [{"arg": "VPObj",
          "analyses": [{"cat": "VP",
                        "form": "infinitive"}],
          "hooks": {"event": "x3",
                    "subj": "x2"}}]
```
This is just the same as for a subject-raising verb, except that the `subj` hook
not only appears in the subject role for the subordinate clause, but there is
also a role for it in the main clause (WANTER).

### object raising

Another type of verb is the object-raising verb, which is one possibility for
"want", as in "They want you to eat it":
```
syn: {"cat": "VerbLex"}
sem: [{"rel": "Want",
       "rolespecs": {"_EVENT": "x1",
                     "WANTER": "x2",
                     "WANTED": "x4"}}],
hooks: {"event": "x1",
        "subj": "x2"}
subcat: [{"arg": "Object",
          "analyses": [{"cat": "NP",
                        "case": "acc}],
	  "hooks": {"root": "x3"},
	  "optional": False},
	 {"arg": "VPObj",
          "analyses": [{"cat": "VP",
                        "form": "infinitive"}],
          "hooks": {"event": "x4",
                    "subj": "x3"}}]
```
Here, `x4` is the root of the verb's object as well as the `subj` hook of the
VP argument. Notice that it does not appear in any role of the verb's semantics
itself.

### object equi

A similar looking frame to object raising is object equi, such as "advise", as
in "We advise you to do it":
```
syn: {"cat": "VerbLex"}
sem: [{"rel": "Advise",
       "rolespecs": {"_EVENT": "x1",
                     "ADVISOR": "x2",
                     "ADVISEE": "x3",
		     "ADVICE": "x4"}}],
hooks: {"event": "x1",
        "subj": "x2"}
subcat: [{"arg": "Object",
          "analyses": [{"cat": "NP",
                        "case": "acc}],
	  "hooks": {"root": "x3"},
	  "optional": False},
	 {"arg": "VPObj",
          "analyses": [{"cat": "VP",
                        "form": "infinitive"}],
          "hooks": {"event": "x4",
                    "subj": "x3"}}]
```
Here, the root of the verbs object does appear in a role of the verb's semantics,
as well as being the `subj` hook of the VP argument.
 
### copula

The copula verb ("be") has no semantics of its own, and is referred to directly
by rule, which creates the resulting syntax-semantics interface. So the entry
for "be" is essentially empty:
```
syn: {"cat": "VerbLex",
      "copula": "+"}
sem: []
hooks: {}
subcat: []
```