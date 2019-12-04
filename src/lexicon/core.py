# Core lexicon file
#
# src.lexicon.core
#

from src.morph.fst import extend_fsa

def add_lex(form, lex, sign, fsa, tag):
    """ Add a form to the lexicon and lexical fsa """
    if form in lex:
        lex[form].append(sign)
    else:
        lex[form] = [sign]

    extend_fsa(fsa, form, tag)

def get_next_index(next_index):
    return 'x' + str(next_index), next_index + 1

def add_role(next_index, relspec, role):
    if type(next_index) is 'str':
        relspec.roles[role] = next_index
    else:
        index, next_index = get_next_index(next_index)
        relspec.roles[role] = index
        return index, next_index
