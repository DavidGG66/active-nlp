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
    """ Return an index based on the current number, and increment that number """
    return 'x' + str(next_index), next_index + 1

def add_role(next_index, relspec, role):
    if type(next_index) == 'str':
        relspec.roles[role] = next_index
    else:
        index, next_index = get_next_index(next_index)
        relspec.roles[role] = index
        return index, next_index


def add_hook(next_index, relspec, role, hooks, hook_name):

    hook, next_index = add_role(next_index, relspec, role)
    hooks[hook_name] = hook

    return next_index

def add_event(next_index, relspec, hooks):

    return add_hook(next_index, relspec, "_EVENT", hooks, "event")


def add_head(next_index, relspec, role, hooks):

    return add_hook(next_index, relspec, role, hooks, "head")


def add_subj(next_index, relspec, role, hooks):

    return add_hook(next_index, relspec, role, hooks, "subj")


def add_obj_subcat(subcat, obj_root, opt):

    obj_subcat = {
        "arg": "Object",
        "optional": opt,
        "analyses": [
            {"cat": "NP",
             "case": "acc"}],
        "hooks": {"root": obj_root}}

    subcat.append(obj_subcat)


def add_obj(next_index, relspec, role, subcat, opt):
    obj, next_index = add_role(next_index, relspec, role)
    add_obj_subcat(subcat, obj, opt)

    return next_index


def add_prep(next_index, relspec, role, prep, subcat):
    pobj, next_index = add_role(next_index, relspec, role)
    prep_subcat = {
        "arg": "PPObj",
        "analyses": [
            {"cat": "PP",
             "pform": prep}],
        "hooks": {"root": pobj}}
    subcat.append(prep_subcat)

    return next_index


def add_vp(next_index, relspec, obj_role, form, subcat, controller):
    vp, next_index = add_role(next_index, relspec, obj_role)
    vp_subcat = {
        "arg": "VPObj",
        "analyses": [
            {"cat": "VP",
             "form": form}],
        "hooks": {
            "event": vp,
            "subj": controller}}
    subcat.append(vp_subcat)

    return next_index

