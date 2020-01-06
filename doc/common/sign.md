# Signs

Think of it like a Saussurean sign, an association between a signifier (the
syntactic form of an expression) and a signified (its semantics).

A sign is made up of four member items:

1. syn_val - the syntactic form of the expression
2. sem_val - a set of relspecs, the semantic value of the expression
3. hooks - a dictionary associating hook names to indices from sem_val
4. subcat - a list of (specs for) subcategorized complements

The *hooks* and *subcat* information are used to keep the semantics straight
when syntactic lexemes, words and phrases are combined

## syn_val

The syntactic value of the sign is a dictionary from names of syntactic
features to their values. Features common to many syntactic values include
*cat* and *args*.

### cat

This is the major syntactic category for the sign. Every syn_val will have a
value for this feature.

### args

This is a list of the components of this syntactic object. For instance, the
sentence "he meditates" is made up of two components, the subject "he" and the
predicate "meditates". The args value for this sentence would look like this:

```
[{"arg": "Subject",
  "syn": {"cat": "NP",
          "sign": X}},
 {"arg": "Predicate",
  "syn": {"cat": "VP",
          "sign": Y}}]
```
Each member of *args* has an argument name (*arg*) and a syntactic description
(*syn*). The syntactic description contains the major syntactic category of the
argument, and a pointer to another sign, which is what *X* and *Y* are meant to
indicate. There are other features in an argument structure relating to how
semantics is kept track of, explained below

### Example

Here is an example of the syn_val for the word "the":
```
{"cat": "Det",
 "agr": {"plu": "any",
         "sg": "+"},
 "quant": "open"}
```

## sem_val

The semantic value of a sign is a list of relspecs. Each relspec is made up of
a relationship name (*rel*) and a *rolespecs* dictionary from role names to
indices. Think of a relspec like a proposition in predicate logic. The *rel* is
the predicate, and the indices are the (unbound) variables. Relspecs use role
names rather than position to keep track variables. So in predicate logic,
"x1 likes x2" looks like this:

`like(x1, x2)`

As a relspec, it looks like this:

```
{"rel": "Like",
 "rolespecs": {"LIKER": "x1",
               "LIKED": "x2",
	       "_EVENT": "x3"}}
```

Notice the "extra" index, `x3`, which fills the "_EVENT" role. Most relspecs
have such a role. While `x1` represents the thing that's doing the liking, and
`x2` represents the thing that is liked, `x3` represents the liking situation
itself.

More complicated meanings are made up by multiple relspecs that share indices.
For instance, 'x1 wants to eat x2' would have something like this sem_val:

```
[{"rel": "Want",
  "rolespecs": {"WANTER": "x1",
                "WANTED": "x3",
		"_EVENT": "x4"}},
 {"rel": "Eat",
 "rolespecs": {"EATER": "x1",
               "EATEN": "x2",
	       "_EVENT": "x3"}}]
```
`x1` wants the `x3` event of `x1` eating `x2`.

## hooks

A hook is a way of picking out an index that serves a particular function in a
semantic value. Grammatical rules refer to those indices when specifying how
the meanings of daughter phrases combine to create the meaning of the mother.

The hooks of a sign are represented as a dictionary from hook names to indices.
For example, here is the sem_val for the word "dog", along with its hooks:

```
{"sem_val": [{"rel": "Dog",
              "rolespecs": {"_EVENT": "x1",
                            "DOG": "x2"}}],
 "hooks": {"head": "x2",
           "event": "x1"}}
```
This indicates that `x1` is the event hook for this sign, and `x2` is the head
hook. The rule adding intersective modifiers references the head hook; the rule
adding non-intersective modifiers references the event hook. For example:

"black dog"
```
{"sem_val": [{"rel": "Dog",
              "rolespecs": {"_EVENT": "x1",
                            "DOG": "x2"}},
             {"rel": "Color",
              "rolespecs": {"_EVENT": "x3",
                            "COLORED": "x2",
	                    "COLOR": "x4" [black]}}],
 "hooks": {"head": "x2",
           "event": "x1"}}
```

"fake dog"
```
{"sem_val": [{"rel": "Dog",
              "rolespecs": {"_EVENT": "x1",
                            "DOG": "x2"}},
             {"rel": "Fake",
              "rolespecs": {"_EVENT": "x3",
                            "FAKE": "x1"}}]
 "hooks": {"head": "x2",
           "event": "x1"}}
```

Different types of hooks are typical for different syntactic categories. For
example, *head* and *event* are typical for nouns; *head* and *root* are
typical for noun phrases; *subj* is typical for verb phrases. The different
hook types are explained in the documentation for each particular syntactic
category.

## subcat

Signs can combine with other signs to make new signs in two ways. In the first
way, a grammatical rule can license two adjacent signs to form a larger sign.
For example, subject noun phrases combine with predicate verb phrases to form
a sentence. This is licensed by a rule, call it the 'S -> NP VP' rule.

In the second way, a "head" sign can specify "argument" signs that can combine
with it. For example, the verb "eat" *subcategorizes* for an object noun
phrase. This combination of signs is handled by subcategorization rather than
by a distinct grammatical rule, because the behavior of taking an object noun
phrase is somewhat dependent on the identity of the particular verb. Some verbs
take an object and others don't.

The *subcat* of a sign is a list of subcategorization frames, each one of which
is a dictionary with four indices: *arg*, *analyses*, *hooks* and *optional*.

As an example, here is the subcat frame for the direct object of a verb like
"eat":

```
{"arg": "Object",
 "analyses": [{"case": "acc",
               "cat": "NP"}],
 "hooks": {"root": "x3"},
 "optional": False}
```
### arg

The value of *arg* is the role that the argument sign plays in the resulting
structure. See the description of the *args* feature of *sem_val* above. In this
example, it says that the subcategorized-for sign will be the Object of the
resulting sign.

### analyses

The value of *analyses* is a list of syntactic descriptions. A sign can be used
as an argument in this frame if its *syn_val* matches one of these descriptions.
In this example, any sign whose syn_val specifies an accusative NP can be used
as the Object.

### hooks

The hooks in a subcat frame tell which indices of the argument sign are to be
identified with which indices of the head sign when building the result sign.
The value of *hooks* is a dictionary from hook names to indices. The hook name
is used to specify a particular index in the sem_val of the argument sign. It is
found by looking up the hook name in the *hooks* property of the argument sign.
The index pointed to by the hook name here in the subcat frame is an index from
the *sem_val* of this head sign.

Here is the whole sign for the verb "eat":

```
{"syn_val": {"cat": "VerbLex",
             "vform": "bare"},
 "sem_val": [{"rel": "Eat",
              "rolespecs": {"_EVENT": "x1",
                            "EATER": "x2",
                            "EATEN: "x3"}}],
 "hooks": {"event": "x1",
           "subj": "x2"},
 "subcat": [{"arg": "Object",
             "analyses": [{"case": "acc",
                           "cat": "NP"}],
             "hooks": {"root": "x3"},
             "optional": False}]}
```
The `{"root": "x3"}` value of `subcat.hooks` says that whatever index is the
*root* index of the argument sign should be identified with the index `x3` from
the root sign (namely, the value of the `EATEN` role of the `Eat` relationship).
