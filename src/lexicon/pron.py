# Pronoun lexicon
#
# src.pron.py
#

from src.common.synval import SynValue
from src.common.semval import SemValue, Relspec
from src.common.sign import Sign

from src.lexicon.core import add_lex, add_role

def pron_entry(next_index):

    syn_val = SynValue("PronLex", True)
    relspec = Relspec("PronRel", {})
    root, next_index = add_role(next_index, relspec, "PRON")

    return syn_val, relspec, {"root": root}, [], next_index


def pers_pron_entry(pron_lex, next_index):

    pers, sg, case = pron_lex
    syn_val, relspec, hooks, subcat, next_index = pron_entry(next_index)
    syn_val["personal"] = "+"
    syn_val["pers"] = pers
    syn_val["agr"] = {"sg": sg}
    syn_val["case"] = case

    return syn_val, relspec, hooks, subcat, next_index


def animate_pron_entry(pron_lex, next_index):

    pers, sg, gen, case = pron_lex
    syn_val, relspec, hooks, subcat, next_index = pers_pron_entry([pers, sg, case], next_index)
    syn_val["animate"] = "+"
    syn_val["gender"] = gen

    return syn_val, [relspec], hooks, subcat, next_index


def inanimate_pron_entry(pron_lex, next_index):

    sg, case = pron_lex
    syn_val, relspec, hooks, subcat, next_index = pers_pron_entry(["3", sg, case], next_index)
    syn_val["animate"] = "-"

    return syn_val, [relspec], hooks, subcat, next_index


def dim_pron_entry(dim, next_index):

    syn_val, relspec, hooks, subcat, next_index = pron_entry(next_index)
    syn_val["indexical"] = "+"
    syn_val["dim"] = dim

    return syn_val, relspec, hooks, subcat, next_index
    

def quant_pron_entry(pron_lex, next_index):

    dim, quant = pron_lex
    syn_val, relspec, hooks, subcat, next_index = dim_pron_entry(dim, next_index)
    syn_val["quant"] = quant

    return syn_val, [relspec], hooks, subcat, next_index


def index_pron_entry(pron_lex, next_index):
    """ Make a located dimension pronoun, like 'then' """

    dim, loc = pron_lex
    syn_val, relspec, hooks, subcat, next_index = dim_pron_entry(dim, next_index)
    syn_val["loc"] = loc

    return syn_val, [relspec], hooks, subcat, next_index


def wh_pron_entry(pron_lex, next_index):

    wh_type, animate, case = pron_lex
    syn_val, relspec, hooks, subcat, next_index = pron_entry(next_index)
    syn_val["wh_type"] = wh_type
    syn_val["animate"] = animate
    syn_val["case"] = case
    syn_val["agr"] = {
        "sg": "+",
        "plu": "-"}

    return syn_val, [relspec], hooks, subcat, next_index


pron_class_table = {
    "pron:animate": animate_pron_entry,
    "pron:inanimate": inanimate_pron_entry,
    "pron:quant": quant_pron_entry,
    "pron:index": index_pron_entry,
    "pron:wh": wh_pron_entry}

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
    ("nowhere", "geo", "none"),
    ("somebody", "pers", "exist"),
    ("someone", "pers", "exist"),
    ("everybody", "pers", "univ"),
    ("everyone", "pers", "univ"),
    ("anybody", "pers", "negpol"),
    ("anyone", "pers", "negpol"),
    ("nobody", "pers", "none"),
    ("always", "temp", "univ"),
    ("never", "temp", "none")]

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
        add_lex(form, lex, ["pron:animate", pers, sg, gen,case], fsa, "pron")
    for form, sg, case in inanimate_prons:
        add_lex(form, lex, ["pron:inanimate", sg, case], fsa, "pron")
    for form, dim, quant in quant_prons:
        add_lex(form, lex, ["pron:quant", dim, quant], fsa, "pron")
    for form, dim, loc in index_prons:
        add_lex(form, lex, ["pron:index", dim, loc], fsa, "pron")
    for form, wh_type, animate, case in wh_prons:
        add_lex(form, lex, ["pron:wh", wh_type, animate, case], fsa, "pron")
