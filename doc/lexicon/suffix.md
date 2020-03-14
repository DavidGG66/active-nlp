
# Suffixes

There are two types of suffixes, plural and past.

## Plural suffixes

There are two plural suffixes, "es" and "s". Here is the edge for "s":
```
syn: {"cat": "SuffLex",
      "suffType": "plural",
      "rootForm": "takesS"}
sem: [{"rel": "AbsVal",
       "rolespecs": {"NODE": "x1",
                     "VAL": "x2"}},
      {"rel": "GreaterThan",
       "rolespecs": {"GREATER": "x2,
                     "LESS": 1}}]
hooks: {"quant": "x1"}
```

The semantics says that it is an absolute value which is greater than 1.

The `rootForm` feature specifies what form the root that this suffix attaches
to must be in.

## Past suffix

There is one past suffix: "ed":
```
syn: {"cat": "SuffLex",
      "suffType": "past",
      "rootForm": "preVowel"},
sem: [{"rel": "TempMatch",
       "rolespecs": {"TEMP1": "x1",
                     "TEMP2": "x2"}},
      {"rel": "PastTemp",
       "rolespecs": {"TEMP": "x2"}}],
hooks: {"temp": "x1",
        "tref": "x2"}
```

The semantics says that this is a time which matches the reference time, which
is some time in the past.
