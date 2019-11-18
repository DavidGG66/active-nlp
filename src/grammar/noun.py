# Rules for 'NP', 'NBar', etc

noun_lex_rules = [
    {"name": "Noun -> NounLex[sg]",
     "mother": {
         "syn": {
             "cat": "Noun",
             "agr": {"plu": "-",
                     "sg": "+"}},
         "sem": {
             "relspecs": [
                 {"rel": "AbsVal",
                  "roles": {
                      "NODE": "x1",
                      "VAL": 1}}],
             "hooks": {"quant": "x1"}}},
     "dtrs": [
         {"dtr": "Head",
          "analyses": [
              {"cat": "NounLex",
               "plural": False}]}],
     "head": {
         "dtr": "Head",
         "hooks": ["head", "event"]}},
    {"name": "Noun -> NounLex[mass]",
     "mother": {
         "syn": {
             "cat": "Noun",
             "agr": {"plu": "+",
                     "sg": "+"}},
         "sem": {
             "relspecs": [
                 {"rel": "RelVal",
                  "roles": {
                      "NODE": "x1",
                      "VAL": 1}}],
             "hooks": {"quant": "x1"}}},
     "dtrs": [
         {"dtr": "Head",
          "analyses": [
              {"cat": "NounLex",
               "quantType": "mass"}]}],
     "head": {
         "dtr": "Head",
         "hooks": ["head", "event"]}},
    {"name": "Noun -> NounLex[sg] Suff[s]",
     "mother": {
         "syn": {
             "cat": "Noun",
             "agr": {"plu": "+",
                     "sg": "+"}},
         "sem": {"hooks": {"quant": "*Quant"}}},
     "dtrs": [
         {"dtr": "Head",
          "analyses": [
              {"cat": "NounLex",
               "plural": False,
               "orthForm": "takesS"}]},
         {"dtr": "Suff"}
     ],
     "head": {}}
]

noun_rules = [
    {"name": "NP -> Det (AP) NBar PostMod*",
     "mother": {
         "syn": {}
         "cat": "NP",
         "agr": "*1"},
     "dtrs": [
         {"dtr": "Det",
          "analyses": [
              {"cat": "Det",
               "agr": "*1"}]},
         {"dtr": "PreAdj",
          "repeatable": True,
          "optional": True,
          "analyses": [
              {"cat": "AdjP"}]},
         {"dtr": "Head",
          "analyses": [
              {"cat": "NBar",
               "agr": "*1"}]},
         {"dtr": "PostMod",
          "repeatable": True,
          "optional": True,
          "analyses": [
              {"cat": "PP"},
              {"cat": "RelC"},
              {"cat": "VP",
               "tense": "non-finite"}]}],
     "head": {
         "dtr": "Head",
         "features": []}},

    {"name": "NBar -> N",
     "mother": {
         "cat": "NBar"},
     "dtrs": [
         {"dtr": "Head",
          "analyses": [
              {"cat": "Noun"}]}]},

    {"name": "NBar -> NBar+ Conj NBar",
     "mother": {
         "cat": "NBar"},
     "dtrs": [
         {"dtr": "Initials",
          "repeatable": True,
          "analyses": [
              {"cat": "NBar"}]},
         {"dtr": "Operator",
          "analyses": [
              {"cat": "Conj"}]},
         {"dtr": "Final",
          "analyses": [
              {"cat": "NBar"}]}]}]
