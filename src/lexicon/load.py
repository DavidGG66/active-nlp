# Load the lexicon
#
# src.lexicon.load
#

from src.morph.fst import FST
from src.lexicon.det import AddDetsToLex
from src.lexicon.noun import AddNounsToLex
from src.lexicon.pron import AddPronsToLex
        
lexicon = {}
lexFsa = FST()

AddNounsToLex(lexicon, lexFsa)
AddDetsToLex(lexicon, lexFsa)
AddPronsToLex(lexicon, lexFsa)
