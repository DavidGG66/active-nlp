# Morpheme break lexicon
#
# src.punc.py
#

from src.common.synval import SynValue
from src.common.semval import SemValue
from src.common.sign import Sign

from src.lexicon.core import add_lex

def punc_lex(type):
    """ Make a morpheme break """

    syn_val = SynValue("PuncLex", True)
    sem_val = SemValue()

    ret = Sign()
    ret.syn_val = syn_val
    ret.sem_val = sem_val

    return ret


puncs = [
    (" ", "space"),
    (".", "period"),
    (",", "comma"),
    ("?", "question_mark"),
    ("!", "exclamation_point"),
    (":", "colon"),
    (";", "semicolon"),
    ("-", "hyphen"),
    ("'", "apostrophe"),
    ('"', "quote")]

def add_puncs_to_lex(lex, fsa):
    for form, type in puncs:
        add_lex(form, lex, punc_lex(type), fsa, "punc")
