# Suffix lexicon
#
# src.lexicon.suffix
#

from src.common.synval import SynValue
from src.common.semval import Relspec
from src.common.sign import Sign

from src.lexicon.core import add_lex, add_role


def suff_syn_value(suff_type, orth_form):
    syn_val = SynValue("SuffLex", True)
    syn_val["suffType"] = suff_type
    syn_val["rootForm"] = orth_form

    return syn_val

def plu_suff_entry(plu_entry, next_index):

    orth_form, = plu_entry
    syn_val = suff_syn_value("plural", orth_form)

    relspec1 = Relspec("AbsVal", {})
    quant, next_index = add_role(next_index, relspec1, "NODE")
    val, next_index = add_role(next_index, relspec1, "VAL")

    relspec2 = Relspec("GreaterThan", {"GREATER": val, "LESS": 1})

    hooks = {"quant": quant}

    return syn_val, [relspec1, relspec2], hooks, [], next_index


def past_suff_entry(past_entry, next_index):

    syn_val = suff_syn_value("past", "preVowel")

    relspec1 = Relspec("TempMatch", {})
    temp, next_index = add_role(next_index, relspec1, "TEMP1")
    tref, next_index = add_role(next_index, relspec1, "TEMP2")
    relspec2 = Relspec("PastTemp", {"TEMP": tref})
    relspecs = [relspec1, relspec2]
    
    hooks = {
        "temp": temp,
        "tref": tref}
    subcat = []

    return syn_val, relspecs, hooks, subcat, next_index


suff_class_table = {
    "suff:plural": plu_suff_entry,
    "suff:past": past_suff_entry}

plural_suffixes = [
    ("es", "takesEs"),
    ("s", "takesS")]

past_suffixes = [
    "ed"]

def add_suffixes_to_lex(lex, fsa):

    for form, orth_form in plural_suffixes:
        add_lex(form, lex, ["suff:plural", orth_form], fsa, "suffix")

    for form in past_suffixes:
        add_lex(form, lex, ["suff:past"], fsa, "suffix")
