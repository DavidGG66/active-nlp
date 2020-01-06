# Verb lexicon
#
# src.lexicon.verb
#

from src.common.synval import SynValue
from src.common.semval import Relspec, SemValue

from src.lexicon.core import add_lex, get_next_index, add_role, add_subj, add_obj, add_prep, add_vp, add_event

def verb_syn_val(vform, irr):
    syn_val = SynValue("VerbLex", True)
    syn_val["vform"] = vform

    if vform == "bare":
        syn_val["irrPlu"] = "-"
        syn_val["irr1st"] = "-"
        syn_val["irr3ps"] = "-"
        if irr:
            syn_val["irrPast"] = "+"
            syn_val["irrPerf"] = "+"
        else:
            syn_val["irrPast"] = "-"
            syn_val["irrPerf"] = "-"

    return syn_val


def verb_entry(rel, vform, irr, next_index):

    syn_val = verb_syn_val(vform, irr)
    relspec = Relspec(rel, {})
    hooks = {}
    next_index = add_event(next_index, relspec, hooks)
    subcat = []

    return syn_val, relspec, hooks, subcat, next_index


def reg(func, verb_lex, next_index):

    return func(verb_lex, "bare", False, next_index)

def irr(func, verb_lex, next_index):

    return func(verb_lex[:-1], verb_lex[-1], True, next_index)


## Copula Verbs

def copula_verb_entry(verb_lex, next_index):

    vform, = verb_lex
    syn_val = SynValue("VerbLex", True)
    syn_val["vform"] = vform

    if vform == "bare":
        syn_val["irrPlu"] = "+"
        syn_val["irr1st"] = "+"
        syn_val["irr3ps"] = "+"
        syn_val["irrPast"] = "+"
        syn_val["irrPerf"] = "+"

    return syn_val, [], {}, [], next_index


## Intransitive Verbs

def intrans_verb_entry(verb_lex, vform, irr, next_index):

    rel, subj_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, vform, irr, next_index)
    next_index = add_subj(next_index, relspec, subj_role, hooks)

    return syn_val, [relspec], hooks, subcat, next_index

def reg_intrans_verb_entry(verb_lex, next_index):

    return reg(intrans_verb_entry, verb_lex, next_index)

def irreg_intrans_verb_entry(verb_lex, next_index):

    return irr(intrans_verb_entry, verb_lex, next_index)


## Transitive Verbs
    
def trans_verb_entry(verb_lex, vform, irr, next_index):

    rel, subj_role, obj_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, vform, irr, next_index)
    next_index = add_subj(next_index, relspec, subj_role, hooks)
    next_index = add_obj(next_index, relspec, obj_role, subcat, False)

    return syn_val, [relspec], hooks, subcat, next_index

def reg_trans_verb_entry(verb_lex, next_index):

    return reg(trans_verb_entry, verb_lex, next_index)

def irreg_trans_verb_entry(verb_lex, next_index):

    return irr(trans_verb_entry, verb_lex, next_index)


## Optionally Transitive Verbs

def opt_trans_verb_entry(verb_lex, vform, irr, next_index):

    rel, subj_role, obj_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, vform, irr, next_index)
    next_index = add_subj(next_index, relspec, subj_role, hooks)
    next_index = add_obj(next_index, relspec, obj_role, subcat, True)

    return syn_val, [relspec], hooks, subcat, next_index

def reg_opt_trans_verb_entry(verb_lex, next_index):

    return reg(opt_trans_verb_entry, verb_lex, next_index)

def irreg_opt_trans_verb_entry(verb_lex, next_index):

    return irr(opt_trans_verb_entry, verb_lex, next_index)


## Ditransitive Verbs

def ditrans_verb_entry(verb_lex, vform, irr, next_index):

    rel, subj_role, obj1_role, obj2_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, vform, irr, next_index)
    next_index = add_subj(next_index, relspec, subj_role, hooks)
    next_index = add_obj(next_index, relspec, obj1_role, subcat, False)
    next_index = add_obj(next_index, relspec, obj2_role, subcat, False)
    
    return syn_val, [relspec], hooks, subcat, next_index

def reg_ditrans_verb_entry(verb_lex, next_index):

    return reg(ditrans_verb_entry, verb_lex, next_index)

def irreg_ditrans_verb_entry(verb_lex, next_index):

    return irr(ditrans_verb_entry, verb_lex, next_index)


## Intransitive + PP Verbs

def intrans_verb_prep_entry(verb_lex, vform, irr, next_index):

    rel, subj_role, pform, obj_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, vform, irr, next_index)
    next_index = add_subj(next_index, relspec, subj_role, hooks)
    next_index = add_prep(next_index, relspec, obj_role, pform, subcat)

    return syn_val, [relspec], hooks, subcat, next_index

def reg_intrans_verb_prep_entry(verb_lex, next_index):

    return reg(intrans_verb_prep_entry, verb_lex, next_index)

def irreg_intrans_verb_prep_entry(verb_lex, next_index):

    return irr(intrans_verb_prep_entry, verb_lex, next_index)


## Inchoative verbs

def inchoative_verb_entry(verb_lex, vform, irr, next_index):

    rel, obj_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry("Cause", vform, irr, next_index)
    next_index = add_subj(next_index, relspec, "CAUSER", hooks)
    sub_event, next_index = add_role(next_index, relspec, "CAUSED")
    sub_relspec = Relspec(rel, {"_EVENT": sub_event})
    next_index = add_obj(next_index, sub_relspec, obj_role, subcat, False)

    return syn_val, [relspec, sub_relspec], hooks, subcat, next_index

def reg_inchoative_verb_entry(verb_lex, next_index):

    return reg(inchoative_verb_entry, verb_lex, next_index)

def irreg_inchoative_verb_entry(verb_lex, next_index):

    return irr(inchoative_verb_etnry, verb_lex, next_index)


## Transitive + Particle Verbs

def trans_particle_verb_entry(verb_lex, vform, irr, next_index):

    pform, rel, subj_role, obj_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, vform, irr, next_index)
    next_index = add_subj(next_index, relspec, subj_role, hooks)
    next_index = add_obj(next_index, relspec, obj_role, subcat, False)
    subcat.append(
        {"arg": "Particle",
         "analyses": [
             {"cat": "Prep",
              "pform": pform}]})

    return syn_val, [relspec], hooks, subcat, next_index

def reg_trans_particle_verb_entry(verb_lex, next_index):

    return reg(trans_particle_verb_entry, verb_lex, next_index)

def irreg_trans_particle_verb_entry(verb_lex, next_index):

    return irr(trans_particle_verb_entry, verb_lex, next_index)


## Subject-Subject Raising Verbs

def subj_raising_verb_entry(verb_lex, vform, irr, next_index):

    rel, obj_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, vform, irr, next_index)
    subj, next_index = get_next_index(next_index)
    hooks["subj"] = subj
    next_index = add_vp(next_index, relspec, obj_role, "infinitive", subcat, subj)
    
    return syn_val, [relspec], hooks, subcat, next_index

def reg_subj_raising_verb_entry(verb_lex, next_index):

    return reg(subj_raising_verb_entry, verb_lex, next_index)

def irreg_subj_raising_verb_entry(verb_lex, next_index):

    return irr(subj_raising_verb_entry, verb_lex, next_index)


## Custom Subject-Subject Raising Verbs

def custom_subj_raising_verb_entry(verb_lex, vform, irr, next_index):

    irr_feat, rel, obj_role, event_role, sub_vform = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, vform, irr, next_index)
    if vform == "bare" and irr:
        syn_val[irr_feat] = "+"
        
    subj, next_index = get_next_index(next_index)
    hooks["subj"] = subj
    next_index = add_vp(next_index, relspec, obj_role, sub_vform, subcat, subj)

    return syn_val, [relspec], hooks, subcat, next_index


def reg_custom_subj_raising_verb_entry(verb_lex, next_index):

    return reg(custom_subj_raising_verb_entry, verb_lex, next_index)

def irreg_custom_subj_raising_verb_entry(verb_lex, next_index):

    return irr(custom_subj_raising_verb_entry, verb_lex, next_index)


## Subject-Subject Equi Verbs

def subj_equi_verb_entry(verb_lex, vform, irr, next_index):

    rel, subj_role, obj_role = verb_lex
    syn_val, relspec, hooks, subcat, next_index = verb_entry(rel, vform, irr, next_index)
    next_index = add_subj(next_index, relspec, subj_role, hooks)
    next_index = add_vp(next_index, relspec, obj_role, "infinitive", subcat, subj)
    
    return syn_val, [relspec], hooks, subcat, next_index

def reg_subj_equi_verb_entry(verb_lex, next_index):

    return reg(subj_equi_verb_entry, verb_lex, next_index)

def irreg_subj_equi_verb_entry(verb_lex, next_index):

    return irr(subj_equi_verb_entry, verb_lex, next_index)


verb_class_table = {
    "verb:intransitive": reg_intrans_verb_entry,
    "verb:irr-intransitive": irreg_intrans_verb_entry,
    "verb:inchoative": reg_inchoative_verb_entry,
    "verb:irr-inchoative": irreg_inchoative_verb_entry,
    "verb:transitive": reg_trans_verb_entry,
    "verb:irr-transitive": irreg_trans_verb_entry,
    "verb:optional-trans": reg_opt_trans_verb_entry,
    "verb:irr-optional-trans": irreg_opt_trans_verb_entry,
    "verb:ditransitive": reg_ditrans_verb_entry,
    "verb:irr-ditransitive": irreg_ditrans_verb_entry,
    "verb:intrans-prep": reg_intrans_verb_prep_entry,
    "verb:irr-intrans-prep": irreg_intrans_verb_prep_entry,
    "verb:trans-particle": reg_trans_particle_verb_entry,
    "verb:irr-trans-particle": irreg_trans_particle_verb_entry,
    "verb:subj-raising": reg_subj_raising_verb_entry,
    "verb:irr-subj-raising": irreg_subj_raising_verb_entry,
    "verb:custom-subj-raising": reg_custom_subj_raising_verb_entry,
    "verb:irr-custom-subj-raising": irreg_custom_subj_raising_verb_entry,
    "verb:subj-equi": reg_subj_equi_verb_entry,
    "verb:irr-subj-equi": irreg_subj_equi_verb_entry,
    "verb:copula": copula_verb_entry}


copula_verbs = [
    ["be", "bare"],
    ["are", "plPres"],
    ["am", "1sgPres"],
    ["is", "3sgPres"],
    ["was", "sgPast"],
    ["were", "plPast"],
    ["been", "pastPart"]]

def add_copula_verbs_to_lex(lex, fsa):
    for form, vform in copula_verbs:
        add_lex(form, lex, ["verb:copula", vform], fsa, "verb")


intrans_verbs = [
    ["knock", "Knock", "KNOCKER"],
    ["smoke", "Smoke", "SMOKER"],
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
        add_lex(ppart, lex, ["verb:irr-intransitive", rel, role, "pastPart"], fsa, "verb")
        
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
        add_lex(ppart, lex, ["verb:irr-inchoative", rel, obj_role, "pastPart"], fsa, "verb")
        add_lex(ppart, lex, ["verb:irr-intransitive", rel, obj_role, "pastPart"], fsa, "verb")

    
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
        add_lex(bare, lex, ["verb:irr-subj-equi", rel, subj_role, obj_role, vform, "bare"], fsa, "verb")
        add_lex(past, lex, ["verb:irr-subj-equi", rel, subj_role, obj_role, vform, "past"], fsa, "verb")
        add_lex(ppart, lex, ["verb:irr-subj-equi", rel, subj_role, obj_role, vform, "ppart"], fsa, "verb")


subj_raising_verbs = [
    ("seem", "Seem", "SEEMED")]

def add_subj_raising_verbs_to_lex(lex, fsa):
    for form, rel, obj_role in subj_raising_verbs:
        add_lex(form, lex, ["verb:subj-raising", rel, obj_role], fsa, "verb")

irr_subj_raising_verbs = []

def add_irr_subj_raising_verbs_to_lex(lex, fsa):
    for bare, past, ppart, rel, obj_role in irr_subj_raising_verbs:
        add_lex(bare, lex, ["verb:irr-subj-raising", rel, obj_role, "bare"], fsa, "verb")
        add_lex(past, lex, ["verb:irr-subj-raising", rel, obj_role, "past"], fsa, "verb")
        add_lex(ppart, lex, ["verb:irr-subj-raising", rel, obj_role, "ppart"], fsa, "verb")

custom_subj_raising_verbs = []

def add_custom_subj_raising_verbs_to_lex(lex, fsa):
    for form, rel, obj_role, event_role, vform in custom_subj_raising_verbs:
        add_lex(form, lex, ["verb:custom-subj-raising", rel, obj_role, event_role, vform], fsa, "verb")

irr_custom_subj_raising_verbs = [
    ("have", "had", "had", "has", "irr3ps", "AchResult", "ACHIEVEMENT", "RESULT", "ppart")]

def add_irr_custom_subj_raising_verbs_to_lex(lex, fsa):
    for bare, past, ppart, tps, irr_feat, rel, obj_role, event_role, vform in irr_custom_subj_raising_verbs:
        add_lex(bare, lex, ["verb:irr-custom-subj-raising", irr_feat, rel, obj_role, event_role, vform, "bare"], fsa, "verb")
        add_lex(past, lex, ["verb:irr-custom-subj-raising", irr_feat, rel, obj_role, event_role, vform, "past"], fsa, "verb")
        add_lex(ppart, lex, ["verb:irr-custom-subj-raising", irr_feat, rel, obj_role, event_role, vform, "ppart"], fsa, "verb")
        add_lex(tps, lex, ["verb:irr-custom-subj-raising", irr_feat, rel, obj_role, event_role, vform, "3sgPres"], fsa, "verb")

def add_verbs_to_lex(lex, fsa):

    add_copula_verbs_to_lex(lex, fsa)
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
    add_custom_subj_raising_verbs_to_lex(lex, fsa)
    add_irr_custom_subj_raising_verbs_to_lex(lex, fsa)
