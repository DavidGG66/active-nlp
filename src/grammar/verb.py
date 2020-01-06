# Grammar rules for Verb-headed things
#
# src.grammar.verb
#

#
#  Lexical rules turning VerbLex into Verb
#

#  Finite (tensed) semantics
def finite_sem():
    return [{"rel": "EventTemp",
             "rolespecs": {
                 "EVENT": "x1",
                 "TEMP": "x2"}}]

def finite_hooks():
    return {
        "event": "x1",
        "temp": "x2",
        "tref": "x3"}

def pres_sem():

    relspecs = [
        {"rel": "TempMatch",
         "rolespecs": {
             "TEMP1": "x2",
             "TEMP2": "x3"}},
        {"rel": "PresTemp",
         "rolespecs": {
             "TEMP": "x3"}}]

    return finite_sem() + relspecs

def past_sem():

    relspecs = [
        {"rel": "TempMatch",
         "rolespecs": {
             "TEMP1": "x2",
             "TEMP2": "x3"}},
        {"rel": "PastTemp",
         "rolespecs": {
             "TEMP": "x3"}}]

    return finite_sem() + relspecs
    
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
    hooks = spec["hooks"]
    analyses = spec["analyses"]
    
    ret = {"name": name,
           "mother": {
               "syn": {"cat": "Verb",
                       "form": form},
               "sem": sem,
               "hooks": hooks},
           "dtrs": [
               {"dtr": "Head",
                "analyses": analyses}],
           "head": {
               "dtr": "Head"}}

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
    hooks = spec["hooks"]
    root_analyses = spec["root_analyses"]
    suff_analyses = spec["suff_analyses"]
    
    ret = {"name": name,
           "mother": {
               "syn": {"cat": "Verb",
                       "form": form},
               "sem": sem,
               "hooks": hooks},
           "dtrs": [
               {"dtr": "Head",
                "analyses": root_analyses},
               {"dtr": "Suff",
                "analyses": suff_analyses}],
           "head": {
               "dtr": "Head"}}

    return ret

def finite_binary_rule(spec):

    bspec = spec.copy()
    bspec["form"] = "finite"

    ret = binary_rule(bspec)

    ret["mother"]["syn"]["tense"] = spec["tense"]
    ret["mother"]["syn"]["agr"] = spec["agr"]

    ret["dtrs"][0]["hooks"] = {"event": "x1"}
    ret["dtrs"][1]["hooks"] = {"temp": "x2"}
    
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
         "sem": pres_sem(),
         "hooks": finite_hooks(),
         "analyses": [
             reg_lex_analysis("bare", "irrPlu"),
             lex_analysis("plPres")]}),

    finite_unary_rule(
        {"name": "Verb[sg: +, pers: 1] -> VerbLex[bare]",
         "tense": "present",
         "agr": {
             "sg": "+",
             "pers": "1"},
         "sem": pres_sem(),
         "hooks": finite_hooks(),
         "analyses": [
             reg_lex_analysis("bare", "irr1st"),
             lex_analysis("1sgPres")]}),

    unary_rule(
        {"name": "Verb[inf] -> VerbLex[bare]",
         "form": "infinitive",
         "sem": [],
         "hooks": {},
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
         "sem": pres_sem(),
         "hooks": finite_hooks(),
         "analyses": [lex_analysis("3sgPres")]}),

    finite_unary_rule(
        {"name": "Verb[tense: past] -> VerbLex[past]",
         "tense": "past",
         "agr": {
             "sg": "any",
             "pers": "any"},
         "sem": past_sem,
         "hooks": finite_hooks(),
         "analyses": [lex_analysis("past")]}),
    
    finite_unary_rule(
        {"name": "Verb[sg: +, tense: past] -> VerbLex[sgPast]",
         "tense": "past",
         "agr": {
             "sg": "+",
             "pers": "any"},
         "sem": past_sem,
         "hooks": finite_hooks(),
         "analyses": [lex_analysis("sgPast")]}),

    finite_unary_rule(
        {"name": "Verb[sg: -, tense: past] -> VerbLex[plPast]",
         "tense": "past",
         "agr": {
             "sg": "-",
             "pers": "any"},
         "sem": past_sem(),
         "hooks": finite_hooks(),
         "analyses": [lex_analysis("plPast")]}),

    unary_rule(
        {"name": "Verb[perf] -> VerbLex[pastPart]",
         "form": "perfect",
         "sem": perf_sem,
         "hooks": {},
         "analyses": [lex_analysis("pastPart")]}),
    
    {"name": "Verb[passive] -> VerbLex[pastPart]",
     "mother": {
         "syn": {"cat": "Verb",
                 "form": "passive"},
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
         "sem": finite_sem(),
         "hooks": finite_hooks(),
         "root_analyses": [root_lex_analysis("irr3ps")],
         "suff_analyses": [suff_lex_analysis("3ps")]}),

    finite_binary_rule(
        {"name": "Verb[past] -> VerbLex[bare] Suff[ed]",
         "tense": "past",
         "agr": {
             "sg": "any",
             "pers": "any"},
         "sem": finite_sem(),
         "hooks": {},
         "root_analyses": [reg_root_lex_analysis("irrPast")],
         "suff_analyses": [suff_lex_analysis("past")]}),

    binary_rule(
        {"name": "Verb[perf] -> VerbLex[bare] Suff[ed]",
         "form": "perfect",
         "sem": perf_sem,
         "hooks": {},
         "root_analyses": [reg_root_lex_analysis("irrPerf")],
         "suff_analyses": [suff_lex_analysis("past")]}),

    passivize(
        binary_rule(
            {"name": "Verb[passive] -> VerbLex[bare] Suff[ed]",
             "form": "passive",
             "sem": [],
             "hooks": {},
             "root_analyses": [reg_root_lex_analysis("irrPerf")],
             "suff_analyses": [suff_lex_analysis("past")]})),

    {"name": "Verb[prog] -> VerbLex[bare] Suff[ing]",
     "mother": {
         "syn": {
             "cat": "Verb",
             "form": "progressive"},
         "sem": [
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
         "hooks": {
             "event": "x1",
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
         "dtr": "Head"}
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

