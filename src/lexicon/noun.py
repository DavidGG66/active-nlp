# Noun lexicon
#
# src.lexicon.noun
#

from src.common.synval import SynValue
from src.common.semval import Relspec, SemValue
from src.common.sign import Sign

from src.lexicon.core import add_lex, add_role

def noun_syn_val():
    syn_val = SynValue("NounLex", True)
    syn_val["regPlu"] = True
    return syn_val


def irr(entry, plural):
    entry[0]["regPlu"] = False
    entry[0]["plural"] = plural

    return entry


def noun_entry(rel, role, next_index):

    syn_val = noun_syn_val()
    relspec = Relspec(rel, {})
    event, next_index = add_role(next_index, relspec, "_EVENT")
    head, next_index = add_role(next_index, relspec, role)
    hooks = {
        "head": head,
        "event": event}

    return syn_val, relspec, hooks, [], next_index


def mass_noun_entry(noun_lex, next_index):

    rel, role = noun_lex
    syn_val, relspec, hooks, subcat, next_index = noun_entry(rel, role, next_index)
    syn_val["quantType"] = "mass"

    return syn_val, [relspec], hooks, subcat, next_index


def count_noun_entry(noun_lex, next_index):

    rel, role = noun_lex
    syn_val, relspec, hooks, subcat, next_index = noun_entry(rel, role, next_index)
    syn_val["quantType"] = "count"
    syn_val["plural"] = False

    return syn_val, [relspec], hooks, subcat, next_index

def irr_count_noun_entry(noun_lex, next_index):

    return irr(count_noun_entry(noun_lex[:-1], next_index), noun_lex[-1])


noun_class_table = {
    "noun:count": count_noun_entry,
    "noun:irr-count": irr_count_noun_entry,
    "noun:mass": mass_noun_entry}

reg_sg_nouns = [
    ("case", "Case", "CASE"),
    ("company", "Company", "COMPANY"),
    ("day", "Day", "DAY"),
    ("dog", "Dog", "DOG"),
    ("eye", "Eye", "EYE"),
    ("girl", "Girl", "GIRL"),
    ("hand", "Hand", "HAND"),
    ("list", "Enumeration", "ENUMERATION"),
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
    ("watch", "Watch", "WATCH"),
    ("way", "Way", "WAY"),
    ("week", "Week", "WEEK"),
    ("world", "World", "WORLD"),
    ("year", "Year", "YEAR")]

def add_count_nouns_to_lex(lex, fsa):
    for form, rel, role in reg_sg_nouns:
        add_lex(form, lex, ["noun:count", rel, role], fsa, "noun")

irr_nouns = [
    ("child", "children", "Child", "CHILD"),
    ("life", "lives", "Life", "LIFE"),
    ("man", "men", "Man", "MAN"),
    ("person", "people", "Person", "PERSON"),
    ("woman", "women", "Woman", "WOMAN")]

def add_irr_nouns_to_lex(lex, fsa):
    for sg, plu, rel, role in irr_nouns:
        add_lex(sg, lex, ["noun:irr-count", rel, role, False], fsa, "noun")
        add_lex(plu, lex, ["noun:irr-count", rel, role, True], fsa, "noun")


mass_nouns = [
    ("life", "Life", "LIFE"),
    ("pain", "Pain2", "PAIN"),
    ("paint", "paint", "PAIN"),
    ("work", "Work", "WORK")]

def add_mass_nouns_to_lex(lex, fsa):
    for form, rel, role in mass_nouns:
        add_lex(form, lex, ["noun:mass", rel, role], fsa, "noun")

def add_nouns_to_lex(lex, fsa):
    add_count_nouns_to_lex(lex, fsa)
    add_irr_nouns_to_lex(lex, fsa)
    add_mass_nouns_to_lex(lex, fsa)

