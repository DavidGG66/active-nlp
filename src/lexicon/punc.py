# Morpheme break lexicon
#
# src.punc.py
#

from src.common.synval import SynValue
from src.common.semval import SemValue
from src.common.sign import Sign

from src.lexicon.core import add_lex

def punc_entry(punc_lex, next_index):

    type, = punc_lex
    syn_val = SynValue("PuncLex", True)
    syn_val["type"] = type

    return syn_val, [], {}, [], next_index

punc_class_table = {"punc:punc": punc_entry}

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
        add_lex(form, lex, ["punc:punc", type], fsa, "punc")
