# Morpheme break lexicon
#
# src.punc.py
#

from src.common.synval import SynValue
from src.common.semval import SemValue
from src.common.synsem import SynSem

from src.lexicon.core import add_lex

def punc_lex(type):
    """ Make a morpheme break """

    synVal = SynValue("PuncLex", True)
    semVal = SemValue()

    return SynSem(synVal, semVal)


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
