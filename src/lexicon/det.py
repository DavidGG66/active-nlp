# Determiner lexicon

from src.common.synval import SynValue
from src.common.semval import Relspec, SemValue
from src.common.sign import Sign

from src.lexicon.core import add_lex

def det_lex(sg, plu, df, width):

    syn_val = SynValue("DetLex", True)
    syn_val["agr"] = {
        "sg": sg,
        "plu": plu}

    roles = {
        "RESTR": "x1",
        "SCOPE": "x2",
        "QUANT": "x3",
        "DEF": df,
        "WIDTH": width}

    hooks = {
        "head": "x1",
        "root": "x2",
        "quant": "x3"}

    relspec = Relspec("Quant", roles)
    sem_val = SemValue()
    sem_val.add_relspec(relspec)

    return syn_val, sem_val, hooks


def det_fixed_lex(sg, plu, df, width, rel, val):

    syn_val, sem_val, hooks = det_lex(sg, plu, df, width)
    syn_val["quant"] = "fixed"

    roles = {
        "NODE": "x3",
        "VAL": 1}
    
    relspec = Relspec("AbsVal", roles)
    sem_val.add_relspec(relspec)

    ret = Sign()
    ret.syn_val = syn_val
    ret.sem_val = [sem_val]
    ret.hooks = hooks
    
    return ret


def det_rel_lex(sg, plu, width, val):

    return det_fixed_lex(sg, plu, "indef", width, "RelVal", val)


def det_open_lex(sg, plu, df, width):

    syn_val, sem_val, hooks = det_lex(sg, plu, df, width)
    syn_val["quant"] = "open"

    ret = Sign()
    ret.syn_val = syn_val
    ret.sem_val = [sem_val]
    ret.hooks = hooks
    
    return ret


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
    def add_det(form, synSem):
        add_lex(form, lex, synSem, fsa, "det")

    for form, sg, plu, df, width, rel, val in fixed_dets:
        add_det(form, det_fixed_lex(sg, plu, df, width, rel, val))
    for form, sg, plu, width, val in rel_dets:
        add_det(form, det_rel_lex(sg, plu, width, val))
    for form, sg, plu, df, width in open_dets:
        add_det(form, det_open_lex(sg, plu, df, width))
               
