# Noun lexicon

import src.common.synval as syn
import src.common.semval as sem
import src.common.synsem as ss

from src.lexicon.core import AddLex

def NounLex(rel, role):

    synVal = syn.SynValue("NounLex", True)

    roles = {
        rel: "x1",
        "_EVENT": "x2"}

    hooks = {
        "head": "x1",
        "event": "x2"}
    
    relspec = sem.Relspec(rel, roles)
    semVal = sem.SemValue()
    semVal.AddRelspec(relspec, {}, hooks)

    return ss.SynSem(synVal, semVal)

def NounCountLex(rel, role):

    ret = NounLex(rel, role)
    ret.synVal["quantType"] = "count"

    return ret


def NounMassLex(rel, role):

    ret = NounLex(rel, role)
    ret.synVal["quantType"] = "mass"

    return ret


def NounRegSgLex(rel, role):

    ret = NounCountLex(rel, role)
    ret.synVal["regPlu"] = True
    ret.synVal["plural"] = False

    return ret


def NounIrrSgLex(rel, role):

    ret = NounCountLex(rel, role)
    ret.synVal["regPlu"] = False
    ret.synVal["plural"] = False

    return ret


def NounIrrPluLex(rel, role):

    ret = NounCountLex(rel, role)
    ret.synVal["regPlu"] = False
    ret.synVal["plural"] = True

    return ret


regSgNouns = [
    ("case", "Case", "CASE"),
    ("company", "Company", "COMPANY"),
    ("day", "Day", "DAY"),
    ("dog", "Dog", "DOG"),
    ("eye", "Eye", "EYE"),
    ("girl", "Girl", "GIRL"),
    ("hand", "Hand", "HAND"),
    ("number", "Number", "NUMBER"),
    ("part", "Part", "PART"),
    ("place", "Place", "PLACE"),
    ("point", "Point", "POINT"),
    ("telescope", "Telescope", "TELESCOPE"),
    ("thing", "Thing", "THING"),
    ("time", "Time", "TIME"),
    ("way", "Way", "WAY"),
    ("week", "Week", "WEEK"),
    ("world", "World", "WORLD"),
    ("year", "Year", "YEAR")]


irrNouns = [
    ("child", "children", "Child", "CHILD"),
    ("life", "lives", "Life", "LIFE"),
    ("man", "men", "Man", "MAN"),
    ("person", "people", "Person", "PERSON"),
    ("woman", "women", "Woman", "WOMAN")]


massNouns = [
    ("life", "Life", "LIFE"),
    ("work", "Work", "WORK")]


def AddNounsToLex(lex, fsa):
    def AddNoun(form, synSem):
        AddLex(form, lex, synSem, fsa, "noun")
        
    for form, rel, role in regSgNouns:
        AddNoun(form, NounRegSgLex(rel, role))
    for sgForm, plForm, rel, role in irrNouns:
        AddNoun(sgForm, NounIrrSgLex(rel, role))
        AddNoun(plForm, NounIrrPluLex(rel, role))
    for form, rel, role in massNouns:
        AddNoun(form, NounMassLex(rel, role))
