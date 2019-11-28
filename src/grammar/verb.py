# Grammar rules for Verb-headed things
#
# src.grammar.verb
#

#
#  Lexical rules turning VerbLex into Verb
#

#  Finite (tensed) semantics
def finite_sem(tense_rel):
    return {
        "relspecs": [
            {"rel": "EventTemp",
             "roles": {
                 "EVENT": "x1",
                 "TEMP": "x2"}},
            {"rel": "TempMatch",
             "roles": {
                 "TEMP1": "x2",
                 "TEMP2": "x3"}},
            {"rel": tense_rel,
             "roles": {
                 "TEMP": "x3"}}],
        "hooks": {
            "event": "x1",
            "ref_time": "x3"}}

#  Perfect form semantics
perf_sem = {
    "relspecs": [
        {"rel": "PfvTime",
         "roles": {
             "EVENT": "x1",
             "TIME": "x2"}},
        {"rel": "Before",
         "roles": {
             "EARLY": "x2",
             "LATE": "__ref__"}}],
    "hooks": {"event": "x1"}}

def lex_analysis(vform):
    """ The lexical analysis for an unbound form """
    
    return {"cat": "VerbLex",
            "vform": vform}


def reg_lex_analysis(vform, irrFeat):
    """ The lexical analysis for an overridably regular unbound form """

    ret = lex_analysis(vform)
    ret[irrFeat] = False

    return ret


def root_lex_analysis():
    """ The lexical analysis for a bound root """

    return {"cat": "VerbLex",
            "vform": "bare",
            "orthoForm": ["*RootForm"]}


def reg_root_lex_analysis(irrFeat):
    """ The lexical analysis for an overridably regular bound root """

    ret = root_lex_analysis()
    ret[irrFeat] = False

    return ret


def suff_lex_analysis(suff_type):
    """ The lexical analysis for a suffix """

    return {"cat": "SuffLex",
            "suffType": suff_type,
            "rootForm": ["*RootForm"]}


def unary_rule(spec):
    """ Return a rule rewriting a Verb as an unbound lexical verb """
    
    name = spec["name"]
    form = spec["form"]
    sem = spec["sem"]
    analyses = spec["analyses"]
    
    ret = {"name": name,
           "mother": {
               "syn": {"cat": "Verb",
                       "form": form},
               "sem": sem},
           "dtrs": [
               {"dtr": "Head",
                "analyses": analyses}],
           "head": {
               "dtr": "Head",
               "hooks": "all"}}

    return ret


def finite_unary_rule(spec):
    """ Return a rule rewriting a finite Verb as an unbound lexical verb """

    uspec = spec.copy()
    uspec["form"] = "finite"
    
    ret = unary_rule(uspec)

    ret["mother"]["syn"]["tense"] = spec["tense"]
    ret["mother"]["syn"]["agr"] = spec["agr"]

    return ret


def binary_rule(spec):
    """ Return a rule rewriting a Verb as a lexical verb root plus suffix """

    name = spec["name"]
    form = spec["form"]
    sem = spec["sem"]
    root_analyses = spec["root_analyses"]
    suff_analyses = spec["suff_analyses"]
    
    ret = {"name": name,
           "mother": {
               "syn": {"cat": "Verb",
                       "form": form},
               "sem": sem},
           "dtrs": [
               {"dtr": "Head",
                "analyses": root_analyses},
               {"dtr": "Suff",
                "analyses": suff_analyses}],
           "head": {
               "dtr": "Head",
               "hooks": "all"}}

    return ret

def finite_binary_rule(spec):

    bspec = spec.copy()
    bspec["form"] = "finite"

    ret = binary_rule(bspec)

    ret["mother"]["syn"]["tense"] = spec["tense"]
    ret["mother"]["syn"]["agr"] = spec["agr"]

    return ret


def passivize(rule):
    """ Add the subcat and hooks info to finish the passive rule"""
    rule["mother"]["subcat"] = {
        "obj": None,
        "preps": {
            "by": [["*Subj"]]}}

    rule["mother"]["hooks"] = {
        "head": ["*Obj"]}

    rule["dtrs"][0]["subcat"] = {
        "obj": ["*Obj"]}

    rule["dtrs"][0]["hooks"] = {
        "subj": ["*Subj"]}

    return rule

    
verb_lex_rules = [

#
#   Unary rules for bare form
#


    finite_unary_rule(
        {"name": "Verb[sg: -] -> VerbLex[bare]",
         "tense": "present",
         "agr": {
             "sg": "-",
             "pers": "any"},
         "sem": finite_sem("PresTemp"),
         "analyses": [
             reg_lex_analysis("bare", "irrPlu"),
             lex_analysis("plPres")]}),

    finite_unary_rule(
        {"name": "Verb[sg: +, pers: 1] -> VerbLex[bare]",
         "tense": "present",
         "agr": {
             "sg": "+",
             "pers": 1},
         "sem": finite_sem("PresTemp"),
         "analyses": [
             reg_lex_analysis("bare", "irr1st"),
             lex_analysis("1sgPres")]}),

    unary_rule(
        {"name": "Verb[inf] -> VerbLex[bare]",
         "form": "infinitive",
         "sem": None,
         "analyses": [lex_analysis("bare")]}),
    
#
#  Unary rules for irregular forms
#

    finite_unary_rule(
        {"name": "Verb[sg: +, pers: 3] -> VerbLex[3sgPres]",
         "tense": "present",
         "agr": {
             "sg": "+",
             "pers": "3"},
         "sem": finite_sem("PresTemp"),
         "analyses": [lex_analysis("3sgPres")]}),

    finite_unary_rule(
        {"name": "Verb[sg: +, tense: past] -> VerbLex[sgPast]",
         "tense": "past",
         "agr": {
             "sg": "+",
             "pers": "any"},
         "sem": finite_sem("PastTemp"),
         "analyses": [lex_analysis("sgPast")]}),

    finite_unary_rule(
        {"name": "Verb[sg: -, tense: past] -> VerbLex[plPast]",
         "tense": "past",
         "agr": {
             "sg": "-",
             "pers": "any"},
         "sem": finite_sem("PastTemp"),
         "analyses": [lex_analysis("plPast")]}),

    unary_rule(
        {"name": "Verb[perf] -> VerbLex[pastPart]",
         "form": "perfect",
         "sem": perf_sem,
         "analyses": [lex_analysis("pastPart")]}),
    
    {"name": "Verb[passive] -> VerbLex[pastPart]",
     "mother": {
         "syn": {"cat": "Verb",
                 "form": "passivePart"},
         "subcat": {
             "obj": None,
             "preps": {
                 "by": [["*Subj"]]}},
         "hooks": {
             "head": ["*Obj"]}},
     "dtrs": [
         {"dtr": "Head",
          "analyses": [
              {"cat": "VerbLex",
               "vform": "pastPart"}],
          "subcat": {
              "obj": ["*Obj"]},
          "hooks": {
              "subj": ["*Subj"]}}],
     "head": {
         "dtr": "Head",
         "hooks": "all"}},

#
#  Binary rules for regular forms
#

    finite_binary_rule(
        {"name": "Verb[sg: +, pers: 3] -> VerbLex[bare] Suff[s]",
         "tense": "present",
         "agr": {
             "sg": "+",
             "pers": "3"},
         "sem": finite_sem("PresTemp"),
         "root_analyses": [root_lex_analysis()],
         "suff_analyses": [suff_lex_analysis("3ps")]}),

    finite_binary_rule(
        {"name": "Verb[past] -> VerbLex[bare] Suff[ed]",
         "tense": "past",
         "agr": {
             "sg": "any",
             "pers": "any"},
         "sem": finite_sem("PastTemp"),
         "root_analyses": [reg_root_lex_analysis("irrPast")],
         "suff_analyses": [suff_lex_analysis("past")]}),

    binary_rule(
        {"name": "Verb[perf] -> VerbLex[bare] Suff[ed]",
         "form": "perfect",
         "sem": perf_sem,
         "root_analyses": [reg_root_lex_analysis("irrPerf")],
         "suff_analyses": [suff_lex_analysis("past")]}),

    passivize(
        binary_rule(
            {"name": "Verb[passive] -> VerbLex[bare] Suff[ed]",
             "form": "passivePart",
             "sem": None,
             "root_analyses": [reg_root_lex_analysis("irrPerf")],
             "suff_analyses": [suff_lex_analysis("past")]})),

    {"name": "Verb[prog] -> VerbLex[bare] Suff[ing]",
     "mother": {
         "syn": {
             "cat": "Verb",
             "form": "passivePart"},
         "sem": {
             "relspecs": [
                 {"rel": "PfvToImpfv",
                  "roles": {
                      "IMPERF": "x1",
                      "PERF": "x2"}},
                 {"rel": "PfvTime",
                  "roles": {
                      "EVENT": "x2",
                      "TIME": "x3"}},
                 {"rel": "TimeInSpan",
                  "roles": {
                      "TIME": "x3",
                      "SPAN": "__ref__"}}],
             "hooks": {"event": "x1"}},
         "hooks": {
             "head": ["*Subj"],
             "subj": None}},
     "dtrs": [
         {"dtr": "Head",
          "analyses": [
              {"cat": "VerbLex",
               "vform": "bare",
               "orthForm": "preVowel"}],
          "hooks": {
              "subj": ["*Subj"]}},
         {"dtr": "Suff",
          "analyses": [
              {"cat": "SuffLex",
               "suffType": "prog"}]}],
     "head": {
         "dtr": "Head",
         "hooks": "all"}
    }
]

verb_phrase_rules = [
    {"name": "VP -> VP[-obj] NP",
     "mother": {
         "syn": {"cat": "VP"}},
     "dtrs": [
         {"dtr": "Head",
          "analyses": [
              {"cat": "VP"}]},
         {"dtr": "Object",
          "analyses": [
              {"cat": "NP",
               "case": "acc"}]}],
     "head": {
         "dtr": "Head",
         "hooks": ["event"],
         "subcat": {
             "slot": "obj",
             "filler": {
                 "dtr": "Object",
                 "hook": "root"}}}}
]

