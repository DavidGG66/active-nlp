# Orthographic rule transducers
#
# src.morph.orth
#

from functools import reduce
from src.morph.fst import FST, State, Arc, ReadFST, AndFST, OrFST, NonDetOrFST

vowel = "aeiouy"
vowelNoY = "aeiou"
consonant = "bcdfghjklmnpqrstvwxz"
nonDoubleCons = "hjqwx"

allButE = "abcdfghijklmnopqrstuvwxyz"

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

test_deleteFinalE = ReadFST(test1_data)
test_doubleFinalCons = ReadFST(test2_data)
test_pVyToI = ReadFST(test3_data)

test_free = ReadFST(test4_data)


deleteFinalE_data = {
    "finals": {
        0: {"preVowel"},
        2: {"preVowel"}},
    "next": 3,
    "states": {
        0: {0: allButE,
            1: "e",
            2: ("e", "epsilon")},
        1: {0: allButE,
            1: "e",
            2: ("e", "epsilon")},
        2: {}}}

deleteFinalE = ReadFST(deleteFinalE_data)

pVyToI_data = {
    "finals": {
        0: {"preVowel"},
        1: {"preVowel"},
        3: {"preVowel"}},
    "next": 4,
    "states": {
        0: {0: consonant,
            1: vowelNoY,
            2: "y",
            3: ("y", "i")},
        1: {0: consonant,
            1: vowel},
        2: {0: consonant,
            1: vowel},
        3: {}}}

pVyToI = ReadFST(pVyToI_data)

doubleFinalCons_data = {
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

doubleFinalCons = ReadFST(doubleFinalCons_data)

tEsibEnd_data = {
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

tEsibEnd = ReadFST(tEsibEnd_data)

tEyToI_data = {
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

tEyToI = ReadFST(tEyToI_data)

endsCCV_data = {
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

endsCCV = ReadFST(endsCCV_data)

tSsibEnd_data = {
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

tSsibEnd = ReadFST(tSsibEnd_data)

tSyToI_data = {
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

tSyToI = ReadFST(tSyToI_data)

free_data = {
    "finals": {0: {"free"}},
    "next": 1,
    "states": {
        0: {0: "abcdefghijklmnopqrstuvwxyz"}}}

free = ReadFST(free_data)

preVowel = reduce(AndFST, [
    deleteFinalE,
    pVyToI,
    doubleFinalCons])

takesEs = reduce(OrFST, [
    tEsibEnd,
    tEyToI,
    endsCCV])

takesS = reduce(AndFST, [
    tSyToI,
    tSsibEnd])

full = reduce(
    NonDetOrFST,
    [
        free,
        preVowel,
        takesEs,
        takesS])

det_full = reduce(
    OrFST,
    [
        free,
        preVowel,
        takesEs,
        takesS])
