# Load the lexicon
#
# src.lexicon.load
#

from src.common.semval import SemValue
from src.common.sign import Sign
from src.morph.fst import FST
from src.lexicon.det import add_dets_to_lex, det_class_table
from src.lexicon.noun import add_nouns_to_lex, noun_class_table
from src.lexicon.prep import add_preps_to_lex, prep_class_table
from src.lexicon.pron import add_prons_to_lex, pron_class_table
from src.lexicon.punc import add_puncs_to_lex, punc_class_table
from src.lexicon.suffix import add_suffixes_to_lex, suff_class_table
from src.lexicon.verb import add_verbs_to_lex, verb_class_table
        
lexicon = {}
lex_fsa = FST()

add_nouns_to_lex(lexicon, lex_fsa)
add_dets_to_lex(lexicon, lex_fsa)
add_preps_to_lex(lexicon, lex_fsa)
add_prons_to_lex(lexicon, lex_fsa)
add_puncs_to_lex(lexicon, lex_fsa)
add_suffixes_to_lex(lexicon, lex_fsa)
add_verbs_to_lex(lexicon, lex_fsa)

lex_class_tables = [
    det_class_table,
    noun_class_table,
    prep_class_table,
    pron_class_table,
    punc_class_table,
    suff_class_table,
    verb_class_table]

lex_class_table = {k: v for table in lex_class_tables for k, v in table.items()}

def lex_entry_to_edge(lex_entry, next_index):

    func = lex_class_table.get(lex_entry[0])
    if func:
        syn_val, relspecs, hooks, subcat, next_index = func(lex_entry[1:], next_index)
        sign = Sign(syn_val, SemValue(relspecs), hooks)
        sign.subcat = subcat

        return sign, next_index


def word_to_edges(word):
    return list(map(lambda entry: lex_entry_to_edge(entry, 1), lexicon[word]))
