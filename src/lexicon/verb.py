# Verb lexicon
#
# src.lexicon.verb
#

from src.common.synval import SynValue
from src.common.semval import Relspec, SemValue
from src.common.sign import Sign

from src.lexicon.core import add_lex, get_next_index, add_role

def verb_syn_val():
    syn_val = SynValue("VerbLex", True)
    syn_val["regPast"] = True
    syn_val["vform"] = "bare"
    return syn_val


def add_subj(next_index, relspec, role, hooks):
    subj, next_index = add_role(next_index, relspec, role)
    hooks["subj"] = subj

    return subj, next_index

def add_obj(next_index, relspec, role, subcat, opt):
    obj, next_index = add_role(next_index, relspec, role)
    obj_subcat = {
        "arg": "Object",
        "optional": opt,
        "analyses": [
            {"cat": "NP",
             "case": "acc"}],
        "hooks": {"root": obj}}
    subcat.append(obj_subcat)

    return obj, next_index


def add_prep(next_index, relspec, role, prep, subcat):
    pobj, next_index = add_role(next_index, relspec, role)
    prep_subcat = {
        "arg": "PPObj",
        "analyses": [
            {"cat": "PP",
             "pform": prep}],
        "hooks": {"root": pobj}}
    subcat.append(prep_subcat)

    return pobj, next_index


def add_vp(next_index, relspec, obj_role, subcat, controller):
    vp, next_index = add_role(next_index, relspec, obj_role)
    vp_subcat = {
        "arg": "VPObj",
        "analyses": [
            {"cat": "VP",
             "form": "infinitive"}],
        "hooks": {
            "event": vp,
            "subj": controller}}
    subcat.append(vp_subcat)

    return vp, next_index


def irr(entry, vform):
    entry[0]["regPast"] = False
    entry[0]["vform"] = vform

    return entry


def verb_entry(rel, next_index):

    syn_val = verb_syn_val()
    relspec = Relspec(rel, {})
    event, next_index = add_role(next_index, relspec, "_EVENT")
    hooks = {"event": event}
    subcat = []

    return syn_val, relspec, hooks, subcat, next_index
    

def intrans_verb_entry(verb_lex, next_index):

    rel, subj_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, next_index)
    subj, next_index = add_subj(next_index, relspec, subj_role, hooks)

    return syn_val, [relspec], hooks, subcat, next_index

def irreg_intrans_verb_entry(verb_lex, vform, next_index):

    return irr(intrans_verb_entry(verb_lex[:-1], next_index), verb_lex[-1])

    
def trans_verb_entry(verb_lex, next_index):

    rel, subj_role, obj_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, next_index)
    subj, next_index = add_subj(next_index, relspec, subj_role, hooks)
    obj, next_index = add_obj(next_index, relspec, obj_role, subcat, False)

    return syn_val, [relspec], hooks, subcat, next_index

def irreg_trans_verb_entry(verb_lex, next_index):

    return irr(trans_verb_entry(verb_lex[:-1], next_index), verb_lex[-1])


def opt_trans_verb_entry(verb_lex, next_index):

    rel, subj_role, obj_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, next_index)
    subj, next_index = add_subj(next_index, relspec, subj_role, hooks)
    obj, next_index = add_obj(next_index, relspec, obj_role, subcat, True)

    return syn_val, [relspec], hooks, subcat, next_index

def irreg_opt_trans_verb_entry(verb_lex, next_index):

    return irr(opt_trans_verb_entry(verb_lex[:-1], next_index), verb_lex[-1])


def ditrans_verb_entry(verb_lex, next_index):

    rel, subj_role, obj1_role, obj2_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, next_index)
    subj, next_index = add_subj(next_index, relspec, subj_role, hooks)
    obj1, next_index = add_obj(next_index, relspec, obj1_role, subcat, False)
    obj2, next_index = add_obj(next_index, relspec, obj2_role, subcat, False)
    
    return syn_val, [relspec], hooks, subcat, next_index

def irreg_ditrans_verb_entry(verb_lex, next_index):

    return irr(ditrans_verb_entry(verb_lex[:-1], next_index), verb_lex[-1])


def intrans_verb_prep_entry(verb_lex, next_index):

    rel, subj_role, pform, obj_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, next_index)
    subj, next_index = add_subj(next_index, relspec, subj_role, hooks)
    prep, next_index = add_prep(next_index, relspec, obj_role, pform, subcat)

    return syn_val, [relspec], hooks, subcat, next_index

def irreg_intrans_verb_prep_entry(verb_lex, next_index):

    return irr(intrans_verb_prep_entry(verb_lex[:-1], next_index), verb_lex[-1])


def inchoative_verb_entry(verb_lex, next_index):

    rel, obj_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry("Cause", next_index)
    subj, next_index = add_subj(next_index, relspec, "CAUSER", hooks)
    sub_event, next_index = add_role(next_index, relspec, "CAUSED")
    sub_relspec = Relspec(rel, {"_EVENT": sub_event})
    obj, next_index = add_obj(next_index, sub_relspec, obj_role, subcat, False)

    return syn_val, [relspec, sub_relspec], hooks, subcat, next_index

def irreg_inchoative_verb_entry(verb_lex, next_index):

    return irr(inchoative_verb_entry(verb_lex[:-1], next_index), verb_lex[-1])


def trans_particle_verb_entry(verb_lex, next_index):

    pform, rel, subj_role, obj_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, next_index)
    subj, next_index = add_subj(next_index, relspec, subj_role, hooks)
    obj, next_index = add_obj(next_index, relspec, obj_role, subcat, False)
    subcat.append(
        {"arg": "Particle",
         "analyses": [
             {"cat": "Prep",
              "pform": pform}]})

    return syn_val, [relspec], hooks, subcat, next_index

def irreg_trans_particle_verb_entry(verb_lex, next_index):

    return irr(trans_particle_verb_entry(verb_lex[:-1], next_index), verb_lex[-1])


def subj_raising_verb_entry(verb_lex, next_index):

    rel, obj_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, next_index)
    subj, next_index = get_next_index(next_index)
    hooks["subj"] = subj
    vp, next_index = add_vp(next_index, relspec, obj_role, subcat, subj)
    
    return syn_val, [relspec], hooks, subcat, next_index

def irreg_subj_raising_verb_entry(verb_lex, next_index):

    return irr(subj_raising_verb_entry(verb_lex[:-1], next_index), verb_lex[-1])


def subj_equi_verb_entry(verb_lex, next_index):

    rel, subj_role, obj_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, next_index)
    subj, next_index = add_subj(next_index, relspec, subj_role, hooks)
    vp, next_index = add_vp(next_index, relspec, obj_role, subcat, subj)
    
    return syn_val, [relspec], hooks, subcat, next_index

def irreg_subj_equi_verb_entry(verb_lex, next_index):

    return irr(subj_equi_verb_entry(verb_lex[:-1], next_index), verb_lex[-1])

verb_class_table = {
    "verb:intransitive": intrans_verb_entry,
    "verb:irr-intransitive": irreg_intrans_verb_entry,
    "verb:inchoative": inchoative_verb_entry,
    "verb:irr-inchoative": irreg_inchoative_verb_entry,
    "verb:transitive": trans_verb_entry,
    "verb:irr-transitive": irreg_trans_verb_entry,
    "verb:optional-trans": opt_trans_verb_entry,
    "verb:irr-optional-trans": irreg_opt_trans_verb_entry,
    "verb:ditransitive": ditrans_verb_entry,
    "verb:irr-ditransitive": irreg_ditrans_verb_entry,
    "verb:intrans-prep": intrans_verb_prep_entry,
    "verb:irr-intrans-prep": irreg_intrans_verb_prep_entry,
    "verb:trans-particle": trans_particle_verb_entry,
    "verb:irr-trans-particle": irreg_trans_particle_verb_entry,
    "verb:subj-raising": subj_raising_verb_entry,
    "verb:irr-subj-raising": irreg_subj_raising_verb_entry,
    "verb:subj-equi": subj_equi_verb_entry,
    "verb:irr-subj-equi": irreg_subj_equi_verb_entry}


intrans_verbs = [
    ["knock", "Knock", "KNOCKER"],
    ["walk", "Walk", "WALKER"]]

def add_it_verbs_to_lex(lex, fsa):
    for form, rel, subj_role in intrans_verbs:        
        add_lex(form, lex, ["verb:intransitive", rel, subj_role], fsa, "verb")

        
irr_intrans_verbs = [
    ["fall", "fell", "fallen", "Fall", "FALLER"],
    ["run", "ran", "run", "Run1", "RUNNER"]]

def add_irr_it_verbs_to_lex(lex, fsa):
    for bare, past, ppart, rel, role in irr_intrans_verbs:
        add_lex(bare, lex, ["verb:irr-intransitive", rel, role, "bare"], fsa, "verb")
        add_lex(past, lex, ["verb:irr-intransitive", rel, role, "past"], fsa, "verb")
        add_lex(ppart, lex, ["verb:irr-intransitive", rel, role, "ppart"], fsa, "verb")
        
inchoative_verbs = [
    ("stop", "Stop", "STOPPED")]

def add_inchoative_verbs_to_lex(lex, fsa):
    for form, rel, obj_role in inchoative_verbs:
        add_lex(form, lex, ["verb:inchoative", rel, obj_role], fsa, "verb")
        add_lex(form, lex, ["verb:intransitive", rel, obj_role], fsa, "verb")

irr_inchoative_verbs = []

def add_irr_inchoative_verbs_to_lex(lex, fsa):
    for bare, past, ppart, rel, obj_role in irr_inchoative_verbs:
        add_lex(bare, lex, ["verb:irr-inchoative", rel, obj_role, "bare"], fsa, "verb")
        add_lex(bare, lex, ["verb:irr-intransitive", rel, obj_role, "bare"], fsa, "verb")
        add_lex(past, lex, ["verb:irr-inchoative", rel, obj_role, "past"], fsa, "verb")
        add_lex(past, lex, ["verb:irr-intransitive", rel, obj_role, "past"], fsa, "verb")
        add_lex(ppart, lex, ["verb:irr-inchoative", rel, obj_role, "ppart"], fsa, "verb")
        add_lex(ppart, lex, ["verb:irr-intransitive", rel, obj_role, "ppart"], fsa, "verb")

    
trans_verbs = [
    ("chase", "Chase", "CHASER", "CHASED"),
    ("copy", "Copy", "COPIER", "COPIED"),
    ("display", "Display", "DISPLAYER", "DISPLAYED")]

def add_trans_verbs_to_lex(lex, fsa):
    for form, rel, subj_role, obj_role in trans_verbs:
        add_lex(form, lex, ["verb:transitive", rel, subj_role, obj_role], fsa, "verb")
        
irr_trans_verbs = [
    ("eat", "ate", "eaten", "Eat", "EATER", "EATEN"),
    ("know", "knew", "known", "Know", "KNOWER", "KNOWN"),
    ("run", "ran", "run", "Run2", "RUNNER", "RAN")]

def add_irr_trans_verbs_to_lex(lex, fsa):
    for bare, past, ppart, rel, subj_role, obj_role in irr_trans_verbs:
        add_lex(bare, lex, ["verb:irr-transitive", rel, subj_role, obj_role, "bare"], fsa, "verb")
        add_lex(past, lex, ["verb:irr-transitive", rel, subj_role, obj_role, "past"], fsa, "verb")
        add_lex(ppart, lex, ["verb:irr-transitive", rel, subj_role, obj_role, "ppart"], fsa, "verb")
    

opt_trans_verbs = [
    ("finish", "Finish", "FINISHER", "FINISHED")]

def add_opt_trans_verbs_to_lex(lex, fsa):
    for form, rel, subj_role, obj_role in opt_trans_verbs:
        add_lex(form, lex, ["verb:optional-trans", rel, subj_role, obj_role], fsa, "verb")

irr_opt_trans_verbs = []

def add_irr_opt_trans_verbs_to_lex(lex, fsa):
    for bare, past, ppart, rel, subj_role, obj_role in irr_opt_trans_verbs:
        add_lex(bare, lex, ["verb:irr-optional-trans", rel, subj_role, obj_role, "bare"], fsa, "verb")
        add_lex(past, lex, ["verb:irr-optional-trans", rel, subj_role, obj_role, "past"], fsa, "verb")
        add_lex(ppart, lex, ["verb:irr-optional-trans", rel, subj_rule, obj_role, "ppart"], fsa, "verb")


ditrans_verbs = [
    ("offer", "Offer1", "OFFERER", "OFFEREE", "OFFERED"),
    ("tell", "Tell", "TELLER", "TELLEE", "TOLD")]

def add_ditrans_verbs_to_lex(lex, fsa):
    for form, rel, subj_role, obj1_role, obj2_role in ditrans_verbs:
        add_lex(form, lex, ["verb:ditransitive", rel, subj_role, obj1_role, obj2_role], fsa, "verb")

irr_ditrans_verbs = []

def add_irr_ditrans_verbs_to_lex(lex, fsa):
    for bare, past, ppart, rel, subj_role, obj1_role, obj2_role in irr_ditrans_verbs:
        add_lex(bare, lex, ["verb:irr-ditransitive", rel, subj_role, obj1_role, obj2_role, "bare"], fsa, "verb")
        add_lex(past, lex, ["verb:irr-ditransitive", rel, subj_role, obj1_role, obj2_role, "past"], fsa, "verb")
        add_lex(ppart, lex, ["verb:irr-ditransitive", rel, subj_role, obj1_role, obj2_role, "ppart"], fsa, "verb")


intrans_prep_verbs = [
    ("rely", "Rely", "RELIER", "on", "RELIEDON")]

def add_intrans_prep_verbs_to_lex(lex, fsa):
    for form, rel, subj_role, pform, obj_role in intrans_prep_verbs:
        add_lex(form, lex, ["verb:intrans-prep", rel, subj_role, pform, obj_role], fsa, "verb")

irr_intrans_prep_verbs = []

def add_irr_intrans_prep_verbs_to_lex(lex, fsa):
    for bare, past, ppart, rel, subj_role, pform, obj_role in irr_intrans_prep_verbs:
        add_lex(bare, lex, ["verb:irr-intrans-prep", rel, subj_role, pform, obj_role, "bare"], fsa, "verb")
        add_lex(past, lex, ["verb:irr-intrans-prep", rel, subj_role, pform, obj_role, "past"], fsa, "verb")
        add_lex(ppart, lex, ["verb:irr-intrans-prep", rel, subj_role, pform, obj_role, "ppart"], fsa, "verb")


trans_part_verbs = [
    ("turn", "on", "TurnOn", "TURNER", "TURNED")]

def add_trans_part_verbs_to_lex(lex, fsa):
    for form, pform, rel, subj_role, obj_role in trans_part_verbs:
        add_lex(form, lex, ["verb:trans-particle", pform, rel, subj_role, obj_role], fsa, "verb")

irr_trans_part_verbs = []

def add_irr_trans_part_verbs_to_lex(lex, fsa):
    for bare, past, ppart, pform, rel, subj_role, obj_role in irr_trans_part_verbs:
        add_lex(bare, lex, ["verb:irr-trans-particle", pform, rel, subj_role, obj_role, "bare"], fsa, "verb")
        add_lex(past, lex, ["verb:irr-trans-particle", pform, rel, subj_role, obj_role, "past"], fsa, "verb")
        add_lex(ppart, lex, ["verb:irr-trans-particle", pform, rel, subj_role, obj_role, "ppart"], fsa, "verb")


subj_equi_verbs = [
    ("offer", "Offer2", "OFFERER", "OFFERED"),
    ("want", "Want", "WANTER", "WANTED")]

def add_subj_equi_verbs_to_lex(lex, fsa):
    for form, rel, subj_role, obj_role in subj_equi_verbs:
        add_lex(form, lex, ["verb:subj-equi", rel, subj_role, obj_role], fsa, "verb")

irr_subj_equi_verbs = []

def add_irr_subj_equi_verbs_to_lex(lex, fsa):
    for bare, past, ppart, rel, subj_role, obj_role in irr_subj_equi_verbs:
        add_lex(bare, lex, ["verb:irr-subj-equi", rel, subj_role, obj_role, "bare"], fsa, "verb")
        add_lex(past, lex, ["verb:irr-subj-equi", rel, subj_role, obj_role, "past"], fsa, "verb")
        add_lex(ppart, lex, ["verb:irr-subj-equi", rel, subj_role, obj_role, "ppart"], fsa, "verb")


subj_raising_verbs = [
    ("seem", "Seem", "SEEMED")]

def add_subj_raising_verbs_to_lex(lex, fsa):
    for form, rel, subj_role in subj_raising_verbs:
        add_lex(form, lex, ["verb:subj-raising", rel, subj_role], fsa, "verb")

irr_subj_raising_verbs = []

def add_irr_subj_raising_verbs_to_lex(lex, fsa):
    for bare, past, ppart, rel, subj_role in irr_subj_raising_verbs:
        add_lex(bare, lex, ["verb:irr-subj-raising", rel, subj_role, "bare"], fsa, "verb")
        add_lex(past, lex, ["verb:irr-subj-raising", rel, subj_role, "past"], fsa, "verb")
        add_lex(ppart, lex, ["verb:irr-subj-raising", rel, subj_role, "ppart"], fsa, "verb")


def add_verbs_to_lex(lex, fsa):

    add_it_verbs_to_lex(lex, fsa)
    add_irr_it_verbs_to_lex(lex, fsa)
    add_inchoative_verbs_to_lex(lex, fsa)
    add_irr_inchoative_verbs_to_lex(lex, fsa)
    add_trans_verbs_to_lex(lex, fsa)
    add_irr_trans_verbs_to_lex(lex, fsa)
    add_opt_trans_verbs_to_lex(lex, fsa)
    add_irr_opt_trans_verbs_to_lex(lex, fsa)
    add_ditrans_verbs_to_lex(lex, fsa)
    add_irr_ditrans_verbs_to_lex(lex, fsa)
    add_intrans_prep_verbs_to_lex(lex, fsa)
    add_irr_intrans_prep_verbs_to_lex(lex, fsa)
    add_trans_part_verbs_to_lex(lex, fsa)
    add_irr_trans_part_verbs_to_lex(lex, fsa)
    add_subj_equi_verbs_to_lex(lex, fsa)
    add_irr_subj_equi_verbs_to_lex(lex, fsa)
    add_subj_raising_verbs_to_lex(lex, fsa)
    add_irr_subj_raising_verbs_to_lex(lex, fsa)
