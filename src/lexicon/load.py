# Load the lexicon
#
# src.lexicon.load
#

from src.morph.fst import FST
from src.lexicon.det import add_dets_to_lex
from src.lexicon.noun import add_nouns_to_lex
from src.lexicon.pron import add_prons_to_lex
from src.lexicon.punc import add_puncs_to_lex
        
lexicon = {}
lex_fsa = FST()

add_nouns_to_lex(lexicon, lex_fsa)
add_dets_to_lex(lexicon, lex_fsa)
add_prons_to_lex(lexicon, lex_fsa)
add_puncs_to_lex(lexicon, lex_fsa)
