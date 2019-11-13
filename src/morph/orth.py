# Orthographic rule transducers
#
# src.morph.orth
#

from functools import reduce
from src.morph.fst import FST, State, Arc, read_fst, and_fst, or_fst, non_det_or_fst

vowel = "aeiouy"
vowel_no_y = "aeiou"
consonant = "bcdfghjklmnpqrstvwxz"

all_but_e = "abcdfghijklmnopqrstuvwxyz"

test1_data = {
    "finals": {0: {"preVowel"},
               1: {"preVowel"}},
    "next": 2,
    "states": {
        0: {0: "dgio",
            1: ('e', "epsilon")},
        1: {}}}

test2_data = {
    "finals": {
        1: {"preVowel"},
        2: {"preVowel"},
        4: {"preVowel"},
        7: {"preVowel"}},
    "next": 3,
    "states": {
        0: {1: "dg",
            2: "eioy"},
        1: {1: "dg",
            4: "eioy"},
        2: {1: "dg",
            2: "eioy"},
        3: {1: "dg",
            4: "eioy"},
        4: {2: "eioy",
            3: "dg",
            5: "d",
            6: "g"},
        5: {7: ('epsilon', 'd')},
        6: {7: ('epsilon', 'g')},
        7: {}}}

test3_data = {
    "finals": {0: {"preVowel"},
               1: {"preVowel"}},
    "next": 4,
    "states": {
        0: {0: "degio",
            1: ('y', 'i')},
        1: {}}}

test4_data = {
    "finals": {0: {"free"}},
    "next": 1,
    "states": {
        0: {0: "degioy"}}}

test_delete_final_e = read_fst(test1_data)
test_double_final_cons = read_fst(test2_data)
test_pv_y_to_i = read_fst(test3_data)

test_free = read_fst(test4_data)


delete_final_e_data = {
    "finals": {
        0: {"preVowel"},
        2: {"preVowel"}},
    "next": 3,
    "states": {
        0: {0: all_but_e,
            1: "e",
            2: ("e", "epsilon")},
        1: {0: all_but_e,
            1: "e",
            2: ("e", "epsilon")},
        2: {}}}

delete_final_e = read_fst(delete_final_e_data)

pv_y_to_i_data = {
    "finals": {
        0: {"preVowel"},
        1: {"preVowel"},
        3: {"preVowel"}},
    "next": 4,
    "states": {
        0: {0: consonant,
            1: vowel_no_y,
            2: "y",
            3: ("y", "i")},
        1: {0: consonant,
            1: vowel},
        2: {0: consonant,
            1: vowel},
        3: {}}}

pv_y_to_i = read_fst(pv_y_to_i_data)

double_final_cons_data = {
    "finals": {
        1: {"preVowel"},
        2: {"preVowel"},
        4: {"preVowel"},
        20: {"preVowel"}},
    "next": 21,
    "states": {
        0: {1: consonant,
            2: vowel},
        1: {1: consonant,
            4: vowel},
        2: {1: consonant,
            2: vowel},
        3: {1: consonant,
            4: vowel},
        4: {2: vowel,
            3: consonant,
            5: "b",
            6: "c",
            7: "d",
            8: "f",
            9: "g",
            10: "k",
            11: "l",
            12: "m",
            13: "n",
            14: "p",
            15: "r",
            16: "s",
            17: "t",
            18: "v",
            19: "z"},
        5: {20: ("epsilon", "b")},
        6: {20: ("epsilon", "k")},
        7: {20: ("epsilon", "d")},
        8: {20: ("epsilon", "f")},
        9: {20: ("epsilon", "g")},
        10: {20: ("epsilon", "k")},
        11: {20: ("epsilon", "l")},
        12: {20: ("epsilon", "m")},
        13: {20: ("epsilon", "n")},
        14: {20: ("epsilon", "p")},
        15: {20: ("epsilon", "r")},
        16: {20: ("epsilon", "s")},
        17: {20: ("epsilon", "t")},
        18: {20: ("epsilon", "v")},
        19: {20: ("epsilon", "z")},
        20: {}}}

double_final_cons = read_fst(double_final_cons_data)

t_e_sib_end_data = {
    "finals": {
        1: {"takesEs"}},
    "next": 3,
    "states": {
        0: {0: "abdefghijklmnopqrtuvwy",
            1: "sxz",
            2: "c"},
        1: {0: "abdefgijklmnopqrtuvwy",
            1: "hsxz",
            2: "c"},
        2: {0: "abdefgijklmnopqrtuvwy",
            1: "hsxz",
            2: "c"}}}

t_e_sib_end = read_fst(t_e_sib_end_data)

t_e_y_to_i_data = {
    "finals": {
        2: {"takesEs"}},
    "next": 3,
    "states": {
        0: {0: "bcdfghjklmnpqrstvwxyz",
            1: "aeiou",
            2: ("y", "i")},
        1: {0: "bcdfjhjklmnpqrstvwxyz",
            1: "aeiou"},
        2: {}}}

t_e_y_to_i = read_fst(t_e_y_to_i_data)

ends_ccv_data = {
    "finals": {
        3: {"takesEs"}},
    "next": 4,
    "states": {
        0: {0: "aeiou",
            1: "bcdfghjklmnpqrstvwxyz"},
        1: {0: "aeiou",
            2: "bcdfghjklmnpqrstvwxyz"},
        2: {0: "aeiou",
            2: "bcdfghjklmnpqrstvwxyz",
            3: "aiou"},
        3: {}}}

ends_ccv = read_fst(ends_ccv_data)

t_s_sib_end_data = {
    "finals": {
        0: {"takesS"},
        2: {"takesS"}},
    "next": 3,
    "states": {
        0: {0: "abdefghijklmnopqrtuvwy",
            1: "sxz",
            2: "c"},
        1: {0: "abdefgijklmnopqrtuvwy",
            1: "hsxz",
            2: "c"},
        2: {0: "abdefgijklmnopqrtuvwy",
            1: "hsxz",
            2: "c"}}}

t_s_sib_end = read_fst(t_s_sib_end_data)

t_s_y_to_i_data = {
    "finals": {
        0: {"takesS"},
        1: {"takesS"}},
    "next": 3,
    "states": {
        0: {0: "bcdfghjklmnpqrstvwxz",
            1: "aeiou",
            2: "y"},
        1: {0: "bcdfghjklmnpqrstvwxz",
            1: "aeiouy"},
        2: {0: "bcdfghjklmnpqrstvwxz",
            1: "aeiouy"}}}

t_s_y_to_i = read_fst(t_s_y_to_i_data)

free_data = {
    "finals": {0: {"free"}},
    "next": 1,
    "states": {
        0: {0: "abcdefghijklmnopqrstuvwxyz"}}}

free = read_fst(free_data)

punc_data = {
    "finals": {1: {"punc"}},
    "next": 2,
    "states": {
        0: {1: " .,?!:;-'\""},
        1: {1: ("epsilon", " ")}}}

punc = read_fst(punc_data)

pre_vowel = reduce(and_fst, [
    delete_final_e,
    pv_y_to_i,
    double_final_cons])

takes_es = reduce(or_fst, [
    t_e_sib_end,
    t_e_y_to_i,
    ends_ccv])

takes_s = reduce(and_fst, [
    t_s_y_to_i,
    t_s_sib_end])

full = reduce(
    non_det_or_fst,
    [
        free,
        pre_vowel,
        takes_es,
        takes_s,
        punc])

det_full = reduce(
    or_fst,
    [
        free,
        pre_vowel,
        takes_es,
        takes_s])
