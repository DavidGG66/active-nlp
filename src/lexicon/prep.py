# Preposition lexicon
#
# src.lexicon.prep
#

from src.common.synval import SynValue
from src.common.semval import Relspec

from src.lexicon.core import add_lex, add_obj, add_event, add_head, add_obj_subcat, add_hook, get_next_index

def prep_syn_val():

    syn_val = SynValue("PrepLex", True)
    return syn_val


def arg_prep_entry(pform, next_index):
    syn_val = prep_syn_val()
    syn_val["pform"] = pform

    return syn_val, [], {}, [], next_index


def adj_prep_entry(rel, role, next_index):

    syn_val = prep_syn_val()
    relspec = Relspec(rel, {})
    hooks = {}
    next_index = add_event(next_index, relspec, hooks)
    next_index = add_head(next_index, relspec, role, hooks)

    return syn_val, relspec, hooks, [], next_index


def adv_prep_entry(rel, role, next_index):

    syn_val = prep_syn_val()
    relspec = Relspec(rel, {})

    hooks = {}
    next_index = add_hook(next_index, relspec, role, hooks, "modevent")

    return syn_val, relspec, hooks, [], next_index

    
def arg_intrans_prep_entry(prep_lex, next_index):

    pform, = prep_lex
    
    return arg_prep_entry(pform, next_index)


def arg_trans_prep_entry(prep_lex, next_index):

    pform, = prep_lex

    syn_val, relspecs, hooks, subcat, next_index = arg_prep_entry(pform, next_index)
    root, next_index = get_next_index(next_index)
    hooks["root"] = root

    add_obj_subcat(subcat, root, False)

    return syn_val, relspecs, hooks, subcat, next_index


def adj_intrans_prep_entry(prep_lex, next_index):

    rel, head_role = prep_lex
    syn_val, relspec, hooks, subcat, next_index = adj_prep_entry(rel, head_role, next_index)

    return syn_val, [relspec], hooks, subcat, next_index

    
def adj_trans_prep_entry(prep_lex, next_index):

    rel, head_role, obj_role = prep_lex
    syn_val, relspec, hooks, subcat, next_index = adj_prep_entry(rel, head_role, next_index)

    next_index = add_obj(next_index, relspec, obj_role, subcat, False)

    return syn_val, [relspec], hooks, subcat, next_index


def adv_intrans_prep_entry(prep_lex, next_index):

    rel, event_role = prep_lex
    syn_val, relspec, hooks, subcat, next_index = adv_prep_entry(rel, event_role, next_index)

    return syn_val, [relspec], hooks, subcat, next_index


def adv_trans_prep_entry(prep_lex, next_index):

    rel, event_role, obj_role = prep_lex
    syn_val, relspec, hooks, subcat, next_index = adv_prep_entry(rel, event_role, next_index)

    next_index = add_obj(next_index, relspec, obj_role, subcat, False)

    return syn_val, [relspec], hooks, subcat, next_index


prep_class_table = {
    "prep:arg-intrans": arg_intrans_prep_entry,
    "prep:arg-trans": arg_trans_prep_entry,
    "prep:adj-intrans": adj_intrans_prep_entry,
    "prep:adj-trans": adj_trans_prep_entry,
    "prep:adv-intrans": adv_intrans_prep_entry,
    "prep:adv-trans": adv_trans_prep_entry}

arg_intrans_preps = [
    ("in", "in")]

def add_arg_intrans_preps_to_lex(lex, fsa):
    for form, pform in arg_intrans_preps:
        add_lex(form, lex, ["prep:arg-intrans", pform], fsa, "prep")


arg_trans_preps = [
    ("on", "on")]

def add_arg_trans_preps_to_lex(lex, fsa):
    for form, pform in arg_trans_preps:
        add_lex(form, lex, ["prep:arg-trans", pform], fsa, "prep")

        
adj_intrans_preps = [
    ("off", "OutOfOperation", "OPERATED"),
    ("on", "InOperation", "OPERATED")]

def add_adj_intrans_preps_to_lex(lex, fsa):
    for form, rel, role in adj_intrans_preps:
        add_lex(form, lex, ["prep:adj-intrans", rel, role], fsa, "prep")

        
adj_trans_preps = [
    ("in", "Contains", "CONTAINED", "CONTAINER"),
    ("with", "Own", "OWNER", "OWNED")]

def add_adj_trans_preps_to_lex(lex, fsa):
    for form, rel, head_role, obj_role in adj_trans_preps:
        add_lex(form, lex, ["prep:adj-trans", rel, head_role, obj_role], fsa, "prep")


adv_intrans_preps = [
    ("alone", "Alone", "ACTION")]

def add_adv_intrans_preps_to_lex(lex, fsa):
    for form, rel, role in adv_intrans_preps:
        add_lex(form, lex, ["prep:adv-intrans", rel, role], fsa, "prep")


adv_trans_preps = [
    ("with", "Instrument", "EVENT", "INSTRUMENT")]

def add_adv_trans_preps_to_lex(lex, fsa):
    for form, rel, event_role, obj_role in adv_trans_preps:
        add_lex(form, lex, ["prep:adv-trans", rel, event_role, obj_role], fsa, "prep")


def add_preps_to_lex(lex, fsa):
    add_arg_intrans_preps_to_lex(lex, fsa)
    add_arg_trans_preps_to_lex(lex, fsa)
    add_adj_intrans_preps_to_lex(lex, fsa)
    add_adj_trans_preps_to_lex(lex, fsa)
    add_adv_intrans_preps_to_lex(lex, fsa)
    add_adv_trans_preps_to_lex(lex, fsa)
