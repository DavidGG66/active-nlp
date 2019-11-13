# parse chart classes
#
# src.parse.chart
#

from src.morph.fst import analyze_character, analyze_fsa_characters

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

    def __init__(self, begin, end, analysis, activation):
        self.begin = begin
        self.end = end
        self.activation = activation
        self.analysis = analysis


class Lexeme():

    def __init__(self, agenda, agendum):
        self.begin = agendum.begin
        self.end = agendum.end
        self.form = agendum.result
        self.ortho_tags = agenda.ortho.finals[agendum.ortho_state]
        self.lex_tags = agenda.lex.finals[agendum.lex_state]


    def to_print(self):
        return [self.begin, self.end, self.form, self.ortho_tags, self.lex_tags]
    
        
class MorphAgendum():

    def __init__(self, begin, end, ortho, lex, result):
        self.begin = begin
        self.end = end
        self.ortho_state = ortho
        self.lex_state = lex
        self.result = result


    def to_print(self):
        return [self.begin, self.end, self.ortho_state, self.lex_state, self.result]


class MorphAgenda():

    def __init__(self, ortho, lex, utterance):
        self.ortho = ortho
        self.lex = lex
        self.utterance = utterance
        self.index = 0
        init_agendum = MorphAgendum(0, 0, ortho.initial, lex.initial, "")
        self.agenda = [init_agendum]
        self.successes = []


    def to_print(self):
        return {
            "utterance": (self.utterance[:self.index], self.utterance[self.index:]),
            "agenda": [agendum.to_print(self) for agendum in self.agenda],
            "successes": [success.to_print(self) for success in self.successes]
        }
    

    def is_success(self, agendum):
        """ is the agendum in a success state """
        return agendum.ortho_state in self.ortho.finals and agendum.lex_state in self.lex.finals
    
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
                    new_agendum = MorphAgendum(begin, end+1, ortho_target, lex_target, new_result)
                    if self.is_success(new_agendum):
                        successes.append(Lexeme(self, new_agendum))
                    new_agenda.append(new_agendum)
        if successes:
            self.successes.extend(successes)
            new_agenda.append(MorphAgendum(self.index, self.index, self.ortho.initial, self.lex.initial, ""))
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

