# Noun lexicon
#
# src.lexicon.noun
#

from src.common.synval import SynValue
from src.common.semval import Relspec, SemValue
from src.common.synsem import SynSem

from src.lexicon.core import add_lex

def noun_lex(rel, role):

    syn_val = SynValue("NounLex", True)

    roles = {
        rel: "x1",
        "_EVENT": "x2"}

    hooks = {
        "head": "x1",
        "event": "x2"}
    
    relspec = Relspec(rel, roles)
    sem_val = SemValue()
    sem_val.add_relspec(relspec, {}, hooks)

    return SynSem(syn_val, sem_val)

def noun_count_lex(rel, role):

    ret = noun_lex(rel, role)
    ret.syn_val["quantType"] = "count"

    return ret


def noun_mass_lex(rel, role):

    ret = noun_lex(rel, role)
    ret.syn_val["quantType"] = "mass"

    return ret


def noun_reg_sg_lex(rel, role):

    ret = noun_count_lex(rel, role)
    ret.syn_val["regPlu"] = True
    ret.syn_val["plural"] = False

    return ret


def noun_irr_sg_lex(rel, role):

    ret = noun_count_lex(rel, role)
    ret.syn_val["regPlu"] = False
    ret.syn_val["plural"] = False

    return ret


def noun_irr_plu_lex(rel, role):

    ret = noun_count_lex(rel, role)
    ret.syn_val["regPlu"] = False
    ret.syn_val["plural"] = True

    return ret


reg_sg_nouns = [
    ("case", "Case", "CASE"),
    ("company", "Company", "COMPANY"),
    ("day", "Day", "DAY"),
    ("dog", "Dog", "DOG"),
    ("eye", "Eye", "EYE"),
    ("girl", "Girl", "GIRL"),
    ("hand", "Hand", "HAND"),
    ("number", "Number", "NUMBER"),
    ("pain", "Pain1", "PAIN"),
    ("part", "Part", "PART"),
    ("place", "Place", "PLACE"),
    ("point", "Point", "POINT"),
    ("rack", "Rack", "RACK"),
    ("telescope", "Telescope", "TELESCOPE"),
    ("thing", "Thing", "THING"),
    ("time", "Time", "TIME"),
    ("track", "Track", "TRACK"),
    ("way", "Way", "WAY"),
    ("week", "Week", "WEEK"),
    ("world", "World", "WORLD"),
    ("year", "Year", "YEAR")]


irr_nouns = [
    ("child", "children", "Child", "CHILD"),
    ("life", "lives", "Life", "LIFE"),
    ("man", "men", "Man", "MAN"),
    ("person", "people", "Person", "PERSON"),
    ("woman", "women", "Woman", "WOMAN")]


mass_nouns = [
    ("life", "Life", "LIFE"),
    ("pain", "Pain2", "PAIN"),
    ("paint", "paint", "PAIN"),
    ("work", "Work", "WORK")]


def add_nouns_to_lex(lex, fsa):
    def add_noun(form, synSem):
        add_lex(form, lex, synSem, fsa, "noun")
        
    for form, rel, role in reg_sg_nouns:
        add_noun(form, noun_reg_sg_lex(rel, role))
    for sgForm, plForm, rel, role in irr_nouns:
        add_noun(sgForm, noun_irr_sg_lex(rel, role))
        add_noun(plForm, noun_irr_plu_lex(rel, role))
    for form, rel, role in mass_nouns:
        add_noun(form, noun_mass_lex(rel, role))

