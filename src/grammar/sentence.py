# Rules for 'S', a sentence

sentence_rules = [
    {"name": "S -> NP VP",
     "mother": {"cat": "S"},
     "dtrs": [
         {"dtr": "Subject",
          "analyses": [
              {"cat": "NP",
               "agr": "*1"}],
         {"dtr": "Predicate",
          "analyses": [
              {"cat": "VP",
               "tense": "finite",
               "agr": "*1"}]}],
     "head": {
         "dtr": "Predicate",
         "features": ["tense"]}}
    ]
