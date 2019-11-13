# Core lexicon file
#
# src.lexicon.core
#

from src.morph.fst import extend_fsa

def add_lex(form, lex, syn_sem, fsa, tag):
    """ Add a form to the lexicon and lexical fsa """
    if form in lex:
        lex[form].append(syn_sem)
    else:
        lex[form] = [syn_sem]
        extend_fsa(fsa, form, tag)
