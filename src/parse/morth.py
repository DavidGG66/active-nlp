# morphology / orthology constraints
#
# src.parse.morth
#

##  Certain combinations of tags from the orthographical and
#   lexical fsts are inconsistent. For example, pronouns
#   ('pron' tag from lexical fsa) only appear in full form
#   ('free' tag from orthographical fsa). Furthermore, they
#   are never left_bound or right_bound
#
#  Each entry in lex_rules is an association between a lexical tag and a
#  triple:
#     a set of orthographical tags (or 'any')
#     a left-bound value
#     a right-bound value
#
#  Each entry in ortho_rules is an association between an orthographical
#  tag and a pair:
#     a left-bound value
#     a right-bound value


lex_rules = {
    'pron': ({'free'}, "-", "-"),      # Pronouns appear in free form only, in an unbound context
    'det': ({'free'}, "-", "-"),       # Determiners likewise
    'noun': ("any", "any", "any"),     # Nouns can appear in any form in any context
    'punc': ({'punc'}, "+", "+"),      # punctuation is a bit different
    'suffix': ({'free'}, "+", "-")}    # suffixes must appear in left-bound context

ortho_rules = {
    'takesS': ("any", "+"),      # morphemes in takesS form must be right-bound
    'takesEs': ("any", "+"),     # same for takesEs
    'preVowel': ("any", "+")}    # and preVowel

def apply_morth(lex_tags, ortho_tags, is_left_bound, is_right_bound):

    ret_tags = set()
    
    for lex_tag in lex_tags:
        good_tags, left_bound, right_bound = lex_rules[lex_tag]
        tag_match = (good_tags == "any" or ortho_tags.intersection(good_tags))
        if left_bound == "any":
            left_match = True
        elif left_bound == "+":
            left_match = is_left_bound
        else:
            left_match = not is_left_bound
        if right_bound == "any":
            right_match = True
        elif right_bound == "+":
            right_match = is_right_bound
        else:
            right_match = not is_right_bound

        if tag_match and left_match and right_match:
            ret_tags.add(lex_tag)

    ortho_match = True
    for ortho_tag in ortho_tags:
        if ortho_tag in ortho_rules:
            left_bound, right_bound = ortho_rules[ortho_tag]
            if left_bound == "any":
                left_match = True
            elif left_bound == "+":
                left_match = is_left_bound
            else:
                left_match = not is_left_bound

            if right_bound == "any":
                right_match = True
            elif right_bound == "+":
                right_match = is_right_bound
            else:
                right_match = not is_right_bound

            ortho_match = ortho_match and left_match and right_match

    if ortho_match:
        return ret_tags
