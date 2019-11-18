# parse chart classes
#
# src.parse.chart
#

from src.morph.fst import analyze_character, analyze_fsa_characters
from src.parse.morth import apply_morth

##  A parse chart consists of
#
#   *  A set of edges;
#      -  Each edge has
#         .  A begin position
#         .  An end position
#         .  A SynSem analysis
#         .  An activation level
#      -  Edges are adjacent if the end position of one
#         is separated from the begin position of the
#         other by a recognized separator
#      -  Create a new edge by
#         .  Combine adjacent edges according to the
#            grammar
#         .  Hypothosizing an edge according the the
#            grammar and an available daughter
#      
#   *  An agenda of morphological FST states
#      -  Each agendum has
#         .  A pointer to the orthographical FST
#         .  A pointer to the lexical FSA
#      -  Create a new edge by adding characters to the
#         morphological FST system until you get a new
#         word


class Edge():
    """ An entry in the chart - an analysis of some substring of the utterance """

    def __init__(self, begin, end, analysis, activation):
        self.begin = begin
        self.end = end
        self.activation = activation
        self.analysis = analysis


class Lexeme():
    """ a substring of the utterance analyzed as a single lexical morpheme """

    def __init__(self, agenda, agendum, lex_tags):
        self.begin = agendum.begin
        self.end = agendum.end
        self.form = agendum.result
        self.ortho_tags = agenda.ortho.finals[agendum.ortho_state]
        self.lex_tags = lex_tags
        self.left_bound = agendum.is_left_bound()
        self.right_bound = agendum.is_right_bound()


    def to_print(self):

        if self.left_bound:
            pform = "-"
        else:
            pform = "["
        pform = pform + self.form
        if self.right_bound:
            pform = pform + "-"
        else:
            pform = pform + "]"
            
        return [self.begin, self.end, pform, self.ortho_tags, self.lex_tags]
    

def is_boundary(char):
    """ is this character a word-boundary character """
    return char in {" ", ".", ",", "?", "!", ":", ";", "-", "'", '"'}


class MorphAgendum():

    def __init__(self, utterance, begin, end, ortho, lex, result):
        self.utterance = utterance
        self.begin = begin
        self.end = end
        self.ortho_state = ortho
        self.lex_state = lex
        self.result = result


    def to_print(self):
        return [self.begin, self.end, self.ortho_state, self.lex_state, self.result]


    def is_left_bound(self):
        return not (self.begin == 0 or is_boundary(self.utterance[self.begin-1]))

    def is_right_bound(self):
        return (self.end < len(self.utterance)) and not is_boundary(self.utterance[self.end])


class MorphAgenda():

    def __init__(self, ortho, lex, utterance):
        self.ortho = ortho
        self.lex = lex
        self.utterance = utterance
        self.index = 0
        init_agendum = MorphAgendum(utterance, 0, 0, ortho.initial, lex.initial, "")
        self.agenda = [init_agendum]
        self.successes = []


    def to_print(self):
        return {
            "utterance": (self.utterance[:self.index], self.utterance[self.index:]),
            "agenda": [agendum.to_print() for agendum in self.agenda],
            "successes": [success.to_print() for success in self.successes]}
    

    def is_success(self, agendum):
        """ is the agendum in a success state """
        ortho_tags = self.ortho.finals.get(agendum.ortho_state)
        lex_tags = self.lex.finals.get(agendum.lex_state)
        is_left_bound = agendum.is_left_bound()
        is_right_bound = agendum.is_right_bound()

        if ortho_tags and lex_tags:
            return apply_morth(lex_tags, ortho_tags, is_left_bound, is_right_bound)

    
    def consume_character(self):
        letter = self.utterance[self.index]
        self.index += 1
        new_agenda = []
        successes = []
        for agendum in self.agenda:
            begin = agendum.begin
            end = agendum.end
            ortho_outs = analyze_character(self.ortho, agendum.ortho_state, letter)
            for ortho_target, out_letters in ortho_outs:
                new_result = agendum.result + ''.join(out_letters)
                lex_targets = analyze_fsa_characters(self.lex, agendum.lex_state, out_letters)
                for lex_target in lex_targets:
                    new_agendum = MorphAgendum(self.utterance, begin, end+1, ortho_target, lex_target, new_result)
                    lex_tags = self.is_success(new_agendum)
                    if lex_tags:
                        successes.append(Lexeme(self, new_agendum, lex_tags))
                    new_agenda.append(new_agendum)
        if successes:
            self.successes.extend(successes)
            new_agenda.append(MorphAgendum(self.utterance, self.index, self.index, self.ortho.initial, self.lex.initial, ""))
        self.agenda = new_agenda
    
        
    def next_word(self):
        while self.agenda and self.utterance[self.index:] and not self.successes:
            self.consume_character()
        if self.successes:
            return self.successes.pop()
        
        
class Chart():

    def __init__(self, ortho, lex, grammar, utterance):
        self.grammar = grammar
        self.next_edge = 1
        self.edges = {}
        self.parents = {}
        self.morph_agenda = MorphAgenda(ortho, lex, utterance)


    def add_edge(self, edge):
        edge_num = self._next_edge
        self.next_edge += 1
        self.edges[edge_num] = edge
        edge.index = edge_num
        self.parents[edge_num] = []


    def add_parent(self, child, parent):
        if type(child) is Edge:
            child = child.index
        if type(parent) is Edge:
            parent = parent.index
        if child in self.parents:
            self.parents[child].append(parent)


    def get_edge(self, edge_num):
        if edge_num in self.edges:
            return self.edges[edge_num]

