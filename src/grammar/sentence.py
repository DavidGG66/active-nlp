# Rules for 'S', a sentence

sentence_rules = [
    {"name": "S -> NP VP",
     "mother": {
         "syn": {"cat": "S"},
         "hooks": {"event": ["*Event"]}},
     "dtrs": [
         {"dtr": "Subject",
          "analyses": [
              {"cat": "NP",
               "case": "nom",
               "agr": ["*Agr"]}],
          "hooks": {
              "root": ["*Subj"]}},
         {"dtr": "Predicate",
          "analyses": [
              {"cat": "VP",
               "form": "finite",
               "agr": ["*Agr"]}],
          "hooks": {
              "subj": ["*Subj"],
              "event": ["*Event"]}}]}]
