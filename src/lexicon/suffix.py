# Suffix lexicon
#
# src.lexicon.suffix
#

from src.common.synval import SynValue
from src.common.semval import Relspec, SemValue
from src.common.sign import Sign

from src.lexicon.core import add_lex

def plu_suff_lex(orth_form):

    rel1 = "AbsVal"
    roles1 = {
        "NODE": "x1",
        "VAL": "x2"}

    rel2 = "GreaterThan"
    roles2 = {
        "GREATER": "x2",
        "LESS": 1}

    relspec1 = Relspec(rel1, roles1)
    relspec2 = Relspec(rel2, roles2)
    
    syn_val = SynValue("SuffLex", True)
    syn_val["suffType"] = "plural"
    syn_val["rootForm"] = orth_form

    sem_val = SemValue()
    sem_val.add_relspec(relspec1)
    sem_val.add_relspec(relspec2)

    hooks = {"quant": "x1"}

    ret = Sign()
    ret.syn_val = syn_val
    ret.sem_val = [sem_val]
    ret.hooks = hooks

    return ret


suffixes = [
    ("es", "takesEs"),
    ("s", "takesS")]


def add_suffixes_to_lex(lex, fsa):
    def add_suff(form, synSem):
        add_lex(form, lex, synSem, fsa, "suffix")

    for form, orth_form in suffixes:
        add_suff(form, plu_suff_lex(orth_form))
