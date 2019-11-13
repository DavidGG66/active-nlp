# Pronoun lexicon
#
# src.pron.py
#

from src.common.synval import SynValue
from src.common.semval import SemValue
from src.common.synsem import SynSem

from src.lexicon.core import add_lex

def pron_lex():
    """ Make a pronoun """

    syn_val = SynValue("PronLex", True)
    semVal = SemValue()

    return SynSem(syn_val, semVal)

def pers_pron_lex(pers, sg, case):
    """ Make a personal pronoun """

    ret = pron_lex()

    ret.syn_val["personal"] = "+"
    ret.syn_val["pers"] = pers
    ret.syn_val["agr"] = {"sg": sg}
    ret.syn_val["case"] = case

    return ret

def animate_pron_lex(pers, sg, gen, case):
    """ Make an animate personal pronoun, like 'me' """

    ret = pers_pron_lex(pers, sg, case)
    ret.syn_val["animate"] = "+"
    ret.syn_val["gender"] = gen

    return ret

def inanimate_pron_lex(sg, case):
    """ Make an inanimate personal pronoun, like 'it' """

    ret = pers_pron_lex("3", sg, case)
    ret.syn_val["animate"] = "-"

    return ret
    
def dim_pron_lex(dim):
    """ Make a pronoun on the geo, pers or temp dimension """

    ret = pron_lex()
    ret.syn_val["indexical"] = "+"
    ret.syn_val["dim"] = dim

    return ret

def quant_pron_lex(dim, quant):
    """ Make a quantified dimension pronoun, like 'everybody' """

    ret = dim_pron_lex(dim)
    ret.syn_val["quant"] = quant
    
    return ret

def index_pron_lex(dim, loc):
    """ Make a located dimension pronoun, like 'then' """

    ret = dim_pron_lex(dim)
    ret.syn_val["loc"] = loc

    return ret

def wh_pron_lex(wh_type, animate, case):
    """ Make a WH pronoun """

    ret = pron_lex()
    ret.syn_val["wh_type"] = wh_type
    ret.syn_val["case"] = case
    ret.syn_val["agr"] = {
        "sg": "+",
        "plu": "-"}

    return ret

animate_prons = [
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


inanimate_prons = [
    ("it", "+", "nom_acc"),
    ("its", "+", "any_gen"),
    ("itself", "+", "refl")]

quant_prons = [
    ("somewhere", "geo", "exist"),
    ("everywhere", "geo", "univ"),
    ("anywhere", "geo", "negpol"),
    ("somebody", "pers", "exist"),
    ("someone", "pers", "exist"),
    ("everybody", "pers", "univ"),
    ("everyone", "pers", "univ"),
    ("anybody", "pers", "negpol"),
    ("anyone", "pers", "negpol")]

index_prons = [
    ("here", "geo", "prox"),
    ("there", "geo", "dist"),
    ("now", "temp", "prox"),
    ("then", "temp", "dist")]

wh_prons = [
    ("what", "ques", "-", "nom_acc"),
    ("who", "any", "+", "nom_acc"),
    ("whom", "any", "+", "acc"),
    ("which", "comp", "any", "nom_acc"),
    ("whose", "ques", "+", "any_gen"),
    ("whose", "comp", "any", "any_gen")]

def add_prons_to_lex(lex, fsa):
    def add_pron(form, syn_sem):
        add_lex(form, lex, syn_sem, fsa, "pron")

    for form, pers, sg, gen, case in animate_prons:
        add_pron(form, animate_pron_lex(pers, sg, gen, case))
    for form, sg, case in inanimate_prons:
        add_pron(form, inanimate_pron_lex(sg, case))
    for form, dim, quant in quant_prons:
        add_pron(form, quant_pron_lex(dim, quant))
    for form, dim, loc in index_prons:
        add_pron(form, index_pron_lex(dim, loc))
    for form, wh_type, animate, case in wh_prons:
        add_pron(form, wh_pron_lex(wh_type, animate, case))
