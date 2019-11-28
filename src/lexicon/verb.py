# Verb lexicon
#
# src.lexicon.verb
#

from copy import copy

from src.common.synval import SynValue
from src.common.semval import Relspec, SemValue
from src.common.sign import Sign

from src.lexicon.core import add_lex

def verb_entry(rel):

    roles = {"_EVENT": "x1"}
    relspec = Relspec(rel, roles)
    
    syn_val = SynValue("VerbLex", True)
    hooks = {"event": "x1"}

    return syn_val, relspec, hooks
    

def intrans_verb_entry(rel, subj_role):

    syn_val, relspec, hooks = verb_entry(rel)
    relspec.roles[subj_role] = "x2"
    hooks["subj"] = "x2"

    return syn_val, relspec, hooks


def trans_verb_entry(rel, subj_role, obj_role):

    syn_val, relspec, hooks = intrans_verb_entry(rel, subj_role)
    relspec.roles[obj_role] = "x3"

    subcat = [
        {"arg": "Object",
         "analyses": [
             {"cat": "NP",
              "case": "acc"}],
         "hooks": {"root": "x3"}}],

    return syn_val, relspec, hooks, subcat


def subj_raise_verb_entry(rel, obj_role):

    syn_val, relspec, hooks = verb_entry(rel)

    relspec.roles[obj_role] = "x2"
    hooks["subj"] = "x3"

    subcat = [
        {"arg": "VPObj",
         "analyses": [
             {"cat": "VP",
              "form": "infinitive"}],
         "hooks": {
             "event": "x2",
             "subj": "x3"}}]

    return syn_val, relspec, hook, subcat


def subj_equi_verb_entry(rel, subj_role, obj_role):

    syn_val, relspec, hooks = intrans_verb_entry(rel, subj_role)
    relspec.roles[obj_role] = "x3"

    subcat = [
        {"arg": "VPObj",
         "analyses": [
             {"cat": "VP",
              "form": "infinitive"}],
         "hooks": {
             "event": "x3",
             "subj": "x2"}}]

    return syn_val, relspec, hook, subcat

intrans_verbs = [
    ("knock", "Knock", "KNOCKER"),
    ("walk", "Walk", "WALKER")]

def add_it_verbs_to_lex(lex, fsa):
    for form, rel, role in intrans_verbs:
        syn_val, relspec, hooks = intrans_verb_entry(rel, role)
        sem_val = SemValue()
        sem_val.add_relspec(relspec)
        
        sign = Sign()
        sign.syn_val = syn_val
        sign.sem_val = [sem_val]
        sign.hooks = hooks
        
        add_lex(form, lex, sign, fsa, "verb")
        
irr_intrans_verbs = [
    ("fall", "fell", "fallen", "Fall", "FALLER"),
    ("run", "ran", "run", "Run1", "RUNNER")
]

def add_irr_it_verbs_to_lex(lex, fsa):
    for bare, past, ppart, rel, role in irr_intrans_verbs:
        syn_val, relspec, hooks = intrans_verb_entry(rel, role)

        syn_val["regPast"] = False
        
        sem_val = SemValue()
        sem_val.add_relspec(relspec)

        sign = Sign()
        sign.sem_val = [sem_val]
        sign.hooks = hooks

        bare_sign = copy(sign)
        bare_sign.syn_val = copy(syn_val)
        bare_sign.syn_val["vform"] = "bare"

        past_sign = copy(sign)
        past_sign.syn_val = copy(syn_val)
        past_sign.syn_val["vform"] = "past"

        ppart_sign = copy(sign)
        ppart_sign.syn_val = copy(syn_val)
        ppart_sign.syn_val["vform"] = "ppart"

        add_lex(bare, lex, bare_sign, fsa, "verb")
        add_lex(past, lex, past_sign, fsa, "verb")
        add_lex(ppart, lex, ppart_sign, fsa, "verb")
        
inchoative_verbs = [
    ("stop", "Stop", "STOPPED")
]

trans_verbs = [
    ("chase", "Chase", "CHASER", "CHASED"),
    ("copy", "Copy", "COPIER", "COPIED"),
    ("display", "DISPLAYER", "DISPLAYED"),
    ("finish", "FINISHER", "FINISHED")
]

irr_trans_verbs = [
    ("eat", "ate", "eaten", "Eat", "EATER", "EATEN"),
    ("know", "knew", "known", "Know", "KNOWER", "KNOWN"),
    ("run", "ran", "run", "Run2", "RUNNER", "RAN")
]

opt_trans_verbs = [
    ("finish", "Finish", "FINISHER", "FINISHED")
]

ditrans_verbs = [
    ("offer", "Offer1", "OFFERER", "OFFEREE", "OFFERED"),
    ("tell", "Tell", "TELLER", "TELLEE", "TOLD")
]

intrans_prep_verbs = [
    ("rely", "Rely", "RELIER", "on", "ON")
]

trans_part_verbs = [
    ("turn", "on", "TurnOn", "TURNER", "TURNED")
]

subj_equi_verbs = [
    ("offer", "Offer2", "OFFERER", "OFFERED"),
    ("want", "Want", "WANTER", "WANTED")
]

subj_raising_verbs = [
    ("seem", "Seem", "SEEMED")
]

def add_verbs_to_lex(lex, fsa):

    add_it_verbs_to_lex(lex, fsa)
    add_irr_it_verbs_to_lex(lex, fsa)

