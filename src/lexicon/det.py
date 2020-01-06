# Determiner lexicon

from src.common.synval import SynValue
from src.common.semval import Relspec
from src.common.sign import Sign

from src.lexicon.core import add_lex, get_next_index, add_role

def det_syn_val(sg, plu):
    syn_val = SynValue("DetLex", True)
    syn_val["agr"] = {
        "sg": sg,
        "plu": plu}
    return syn_val

def det_entry(sg, plu, df, width, next_index):

    syn_val = det_syn_val(sg, plu)

    relspec = Relspec("Quant", {})
    head, next_index = add_role(next_index, relspec, "RESTR")
    root, next_index = add_role(next_index, relspec, "SCOPE")
    quant, next_index = add_role(next_index, relspec, "QUANT")
    relspec.roles["DEF"] = df
    relspec.roles["WIDTH"] = width

    hooks = {
        "head": head,
        "root": root,
        "quant": quant}

    return syn_val, relspec, hooks, [], next_index


def fixed_det_entry(det_lex, next_index):

    sg, plu, df, width, rel, val = det_lex
    syn_val, relspec, hooks, subcat, next_index = det_entry(sg, plu, df, width, next_index)
    syn_val["quant"] = "fixed"
    val_roles = {
        "NODE": hooks["quant"],
        "VAL": 1}
    val_relspec = Relspec("AbsVal", val_roles)

    return syn_val, [relspec, val_relspec], hooks, subcat, next_index


def rel_det_entry(det_lex, next_index):

    sg, plu, width, val = det_lex
    return fixed_det_entry([sg, plu, "indef", width, "RelVal", val], next_index)


def open_det_entry(det_lex, next_index):

    sg, plu, df, width = det_lex
    syn_val, relspec, hooks, subcat, next_index = det_entry(sg, plu, df, width, next_index)
    syn_val["quant"] = "open"

    return syn_val, [relspec], hooks, subcat, next_index

det_class_table = {
    "det:relative": rel_det_entry,
    "det:open": open_det_entry,
    "det:fixed": fixed_det_entry}

fixed_dets = [("a", "+", "-", "indef", "narrow", "AbsVal", 1)]

rel_dets = [
    ("all", "any", "+", "narrow", 1),
    ("each", "+", "-", "wide", 1),
    ("every", "+", "-", "narrow", 1)]
        
open_dets = [
    ("some", "any", "any", "indef", "narrow"),
    ("that", "+", "any", "distal", "narrow"),
    ("the", "any", "any", "definite", "narrow"),
    ("those", "-", "+", "distal", "narrow")]

def add_dets_to_lex(lex, fsa):
    for form, sg, plu, df, width, rel, val in fixed_dets:
        add_lex(form, lex, ["det:fixed", sg, plu, df, width, rel, val], fsa, "det")
    for form, sg, plu, width, val in rel_dets:
        add_lex(form, lex, ["det:rel", sg, plu, width, val], fsa, "det")
    for form, sg, plu, df, width in open_dets:
        add_lex(form, lex, ["det:open", sg, plu, df, width], fsa, "det")

