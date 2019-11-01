# Rules for 'NP', 'NBar', etc

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
