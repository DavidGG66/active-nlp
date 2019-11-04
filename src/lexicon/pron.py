# Pronoun lexicon
#
# src.pron.py
#

import src.common.synval as syn
import src.common.semval as sem
import src.common.synsem as ss

from src.lexicon.core import AddLex

def PronLex():
    """ Make a pronoun """

    synVal = syn.SynValue("PronLex", True)
    semVal = sem.SemValue()

    return ss.SynSem(synVal, semVal)

def PersPronLex(pers, sg, case):
    """ Make a personal pronoun """

    ret = PronLex()

    ret.synVal["personal"] = "+"
    ret.synVal["pers"] = pers
    ret.synVal["agr"] = {"sg": sg}
    ret.synVal["case"] = case

    return ret

def AnimatePronLex(pers, sg, gen, case):
    """ Make an animate personal pronoun, like 'me' """

    ret = PersPronLex(pers, sg, case)
    ret.synVal["animate"] = "+"
    ret.synVal["gender"] = gen

    return ret

def InanimatePronLex(sg, case):
    """ Make an inanimate personal pronoun, like 'it' """

    ret = PersPronLex("3", sg, case)
    ret.synVal["animate"] = "-"

    return ret
    
def DimPronLex(dim):
    """ Make a pronoun on the geo, pers or temp dimension """

    ret = PronLex()
    ret.synVal["indexical"] = "+"
    ret.synVal["dim"] = dim

    return ret

def QuantPronLex(dim, quant):
    """ Make a quantified dimension pronoun, like 'everybody' """

    ret = DimPronLex(dim)
    ret.synVal["quant"] = quant
    
    return ret

def IndexPronLex(dim, loc):
    """ Make a located dimension pronoun, like 'then' """

    ret = DimPronLex(dim)
    ret.synVal["loc"] = loc

    return ret

def WhPronLex(whType, animate, case):
    """ Make a WH pronoun """

    ret = PronLex()
    ret.synVal["whType"] = whType
    ret.synVal["case"] = case
    ret.synVal["agr"] = {
        "sg": "+",
        "plu": "-"}

    return ret

animateProns = [
    ("i", "1", "+", "any", "nom"),
    ("me", "1", "+", "any", "acc"),
    ("my", "1", "+", "any", "gendet"),
    ("mine", "1", "+", "any", "gennp"),
    ("myself", "1", "+", "any", "refl"),
    ("we", "1", "-", "any", "nom"),
    ("us", "1", "-", "any", "acc"),
    ("our", "1", "-", "any", "gendet"),
    ("ours", "1", "-", "any", "gennp"),
    ("ourselves", "1", "-", "any", "refl"),
    ("you", "2", "-", "any", "nom_acc"),
    ("your", "2", "-", "any", "gendet"),
    ("yours", "2", "-", "any", "gennp"),
    ("he", "3", "+", "masc", "nom"),
    ("him", "3", "+", "masc", "acc"),
    ("his", "3", "+", "masc", "any_gen"),
    ("himself", "3", "-", "masc", "refl"),
    ("she", "3", "+", "fem", "nom"),
    ("her", "3", "+", "fem", "acc"),
    ("her", "3", "+", "fem", "gendet"),
    ("hers", "3", "+", "fem", "gennp"),
    ("herself", "3", "+", "fem", "refl"),
    ("they", "3", "-", "any", "nom"),
    ("them", "3", "-", "any", "acc"),
    ("their", "3", "-", "any", "gendet"),
    ("theirs", "3", "-", "any", "gennp"),
    ("themselves", "3", "-", "any", "refl")]


inanimateProns = [
    ("it", "+", "nom_acc"),
    ("its", "+", "any_gen"),
    ("itself", "+", "refl")]

quantProns = [
    ("somewhere", "geo", "exist"),
    ("everywhere", "geo", "univ"),
    ("anywhere", "geo", "negpol"),
    ("somebody", "pers", "exist"),
    ("someone", "pers", "exist"),
    ("everybody", "pers", "univ"),
    ("everyone", "pers", "univ"),
    ("anybody", "pers", "negpol"),
    ("anyone", "pers", "negpol")]

indexProns = [
    ("here", "geo", "prox"),
    ("there", "geo", "dist"),
    ("now", "temp", "prox"),
    ("then", "temp", "dist")]

whProns = [
    ("what", "ques", "-", "nom_acc"),
    ("who", "any", "+", "nom_acc"),
    ("whom", "any", "+", "acc"),
    ("which", "comp", "any", "nom_acc"),
    ("whose", "ques", "+", "any_gen"),
    ("whose", "comp", "any", "any_gen")]

def AddPronsToLex(lex, fsa):
    def AddPron(form, synSem):
        AddLex(form, lex, synSem, fsa, "pron")

    for form, pers, sg, gen, case in animateProns:
        AddPron(form, AnimatePronLex(pers, sg, gen, case))
    for form, sg, case in inanimateProns:
        AddPron(form, InanimatePronLex(sg, case))
    for form, dim, quant in quantProns:
        AddPron(form, QuantPronLex(dim, quant))
    for form, dim, loc in indexProns:
        AddPron(form, IndexPronLex(dim, loc))
    for form, whType, animate, case in whProns:
        AddPron(form, WhPronLex(whType, animate, case))
