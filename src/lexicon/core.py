# Core lexicon file
#
# src.lexicon.core
#

from src.morph.fst import ExtendFSA

def AddLex(form, lex, synSem, fsa, tag):
    """ Add a form to the lexicon and lexical fsa """
    if form in lex:
        lex[form].append(synSem)
    else:
        lex[form] = [synSem]
        ExtendFSA(fsa, form, tag)
