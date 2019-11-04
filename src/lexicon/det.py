# Determiner lexicon

import src.common.synval as syn
import src.common.semval as sem
import src.common.synsem as ss

from src.lexicon.core import AddLex

def DetLex(sg, plu, df, width):

    synVal = syn.SynValue("DetLex", True)
    synVal["agr"] = {
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

    relspec = sem.Relspec("Quant", roles)
    semVal = sem.SemValue()
    semVal.AddRelspec(relspec, {}, hooks)

    return synVal, semVal


def DetFixedLex(sg, plu, df, width, rel, val):

    synVal, semVal = DetLex(sg, plu, df, width)
    synVal["quant"] = "fixed"

    roles = {
        "NODE": "x3",
        "VAL": 1}
    
    relspec = sem.Relspec("AbsVal", roles)
    semVal.AddRelspec(relspec, {"x3": "quant"}, {})

    return ss.SynSem(synVal, semVal)


def DetRelLex(sg, plu, width, val):

    return DetFixedLex(sg, plu, "indef", width, "RelVal", val)


def DetOpenLex(sg, plu, df, width):

    synVal, semVal = DetLex(sg, plu, df, width)
    synVal["quant"] = "open"

    return ss.SynSem(synVal, semVal)

fixedDets = [("a", "+", "-", "indef", "narrow", "AbsVal", 1)]


relDets = [
    ("all", "any", "+", "narrow", 1),
    ("each", "+", "-", "wide", 1),
    ("every", "+", "-", "narrow", 1)]
        
openDets = [
    ("some", "any", "any", "indef", "narrow"),
    ("that", "+", "any", "distal", "narrow"),
    ("the", "any", "any", "definite", "narrow"),
    ("those", "-", "+", "distal", "narrow")]

def AddDetsToLex(lex, fsa):
    def AddDet(form, synSem):
        AddLex(form, lex, synSem, fsa, "det")

    for form, sg, plu, df, width, rel, val in fixedDets:
        AddDet(form, DetFixedLex(sg, plu, df, width, rel, val))
    for form, sg, plu, width, val in relDets:
        AddDet(form, DetRelLex(sg, plu, width, val))
    for form, sg, plu, df, width in openDets:
        AddDet(form, DetOpenLex(sg, plu, df, width))
               
