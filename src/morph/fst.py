# Finite state transducers and such
#
# src.morph.fst
#

from src.common.utils import first_filter

class Arc():
    """ An arc, consisting of target and labels """
    
    def __init__(self, target, label):
        self.target = target
        self.add_label(label)

    def make_copy(self):
        ret = Arc(self.target, None)
        if hasattr(self, "units"):
            ret.units = set(self.units)
        if hasattr(self, "pairs"):
            ret.pairs = set(self.pairs)

        return ret

    def get_units(self):
        if hasattr(self, "units"):
            return self.units
        else:
            return set()


    def get_pairs(self):
        if hasattr(self, "pairs"):
            return self.pairs
        else:
            return set()

        
    def add_unit(self, s):
        """ Add a string or set of strings to the label units """
        if type(s) is str:
            s = {s}
        if hasattr(self, "units"):
            self.units.update(s)
        else:
            self.units = s

    def add_pair(self, p):
        if hasattr(self, "pairs"):
            self.pairs.add(p)
        else:
            self.pairs = {p}
            
    def add_label(self, label):
        """ Add a new label to any existing labels on an arc """
        if type(label) is str:
            if label[0] == "_" and label[-1] == "_":
                self.add_unit(label)
            else:
                self.add_unit(set(label))
        elif type(label) is tuple:
            self.add_pair(label)
            

    def to_print_from_state(self):
        label = []
        if hasattr(self, "units"):
            label.append(''.join(self.units))
        if hasattr(self, "pairs"):
            label.append(self.pairs)
        return label

    def to_print(self):
        
        return {
            "target": self.target,
            "label": self.to_print_from_state()}


class State():
    """ Information about a state

    The arcs leading from it
    The maximum number of characters following it
    """

    def __init__(self):
        self.arc_map = {}

    def add_arc(self, target, label):
        if target in self.arc_map:
            self.arc_map[target].add_label(label)
        else:
            self.arc_map[target] = Arc(target, label)

    def arc_list(self):
        return self.arc_map.items()
    
    def to_print(self):
        return {k:v.to_print_from_state() for k,v in self.arc_map.items()}

    
class FST():

    def __init__(self):
        self.initial = 0
        self.finals = {}
        self.next = 1
        self.states = {0: State()}

    def to_print(self):
        return {
            "finals": self.finals,
            "states": {k:v.to_print() for k,v in self.states.items()}}

    def add_state(self, source):
        if source not in self.states:
            self.states[source] = State()
            
    def add_arc(self, source, target, label):
        """ Add an arc with the given source, target & label """
        if source in self.states:
            self.states[source].add_arc(target, label)
        else:
            state = State()
            state.add_arc(target, label)
            self.states[source] = state

        if target not in self.states:
            self.states[target] = State()

    def copy_arc(self, source, target, arc):
        """ Add an arc with all the labels from a given arc """
        for letter in arc.get_units():
            self.add_arc(source, target, letter)
        for pair in arc.get_pairs():
            self.add_arc(source, target, pair)

    def arc_list(self, state):
        return self.states[state].arc_list()
    

def word_fst(word, tag):
    """ Make an FST that recognizes a single word with the given tag """
    ret = FST()
    source = ret.initial
    for letter in word:
        target = ret.next
        ret.next += 1
        ret.add_arc(source, target, letter)
        source += 1

    ret.finals = {source: {tag}}
    return ret


class StateTable():

    def __init__(self):
        self.next_state = 0
        self.state_map = {}


    def __contains__(self, state):
        return state in self.state_map

    
    def find_combo_state(self, agendum):
        if agendum not in self.state_map:
            self.state_map[agendum] = self.next_state
            self.next_state += 1
        return self.state_map[agendum]


def read_fst(fst_data):
    ret = FST()
    for k,v in fst_data.items():
        if k == "finals":
            ret.finals = v
        elif k == "next":
            ret.next = v
        elif k == "states":
            for source, arc in v.items():
                if source not in ret.states:
                    ret.states[source] = State()
                for target, label in arc.items():
                    ret.add_arc(source, target, label)
    return ret


def add_agendum(agenda, agendum, state_table):
    """ Add a new agenda item, as long as it hasn't already been seen """
    if agendum not in state_table:
        agenda.append(agendum)

        
def add_eps_arcs(eps_arc_list, other_arc_list, fst, source, state_table, agenda, epsilon1):
    """ Add arcs following surface epsilon transitions to the new fst """
    for eps_target, eps_arc in eps_arc_list:
        eps_pairs = list(filter(lambda x: x[1] == 'epsilon', eps_arc.get_pairs()))
        if eps_pairs:
            for other_target, other_arc in other_arc_list:
                if other_arc.get_units():
                    other_target = other_arc.target
                    if epsilon1:
                        new_target = (eps_target, other_target)
                    else:
                        new_target = (other_target, eps_target)
                    add_agendum(agenda, new_target, state_table)
                    combo_target = state_table.find_combo_state(new_target)
                    fst.add_state(combo_target)
                    for label in eps_pairs:
                        fst.add_arc(source, combo_target, label)

        
def get_match_pairs(arc1, arc2):
    """ Get pairs where the surface from one matches a string from another """
    ret = {}
    ret.update(filter(lambda x: x[1] in arc2.get_units(), arc1.get_pairs()))
    ret.update(filter(lambda x: x[1] in arc1.get_units(), arc2.get_pairs()))
    return ret


def new_target(fst, target1, target2, agenda, state_table):
    """ Make a new target state and add it to the fst and agenda """

    new_agendum = (target1, target2)
    add_agendum(agenda, new_agendum, state_table)
    combo_target = state_table.find_combo_state(new_agendum)
    fst.add_state(combo_target)

    return combo_target


def add_and_arcs(fst, source, target1, arc1, target2, arc2, agenda, state_table):
    """ Add arcs for the intersection of the two input arcs """

    units = arc1.get_units().intersection(arc2.get_units())
    pairs = get_match_pairs(arc1, arc2)

    if units or pairs:
        combo_target = new_target(fst, target1, target2, agenda, state_table)

    if units:
        fst.add_arc(source, combo_target, ''.join(units))
    if pairs:
        for pair in pairs:
            fst.add_arc(source, combo_target, pair)


def add_final_and_states(fst, fst1, fst2, state_table):
    """ Set the accepting-state information for an anded fst """
    for agendum, state in state_table.state_map.items():
        state1, state2 = agendum
        finals1 = fst1.finals.get(state1, set())
        finals2 = fst2.finals.get(state2, set())
        new_finals = finals1.intersection(finals2)
        if new_finals:
            fst.finals[state] = new_finals


def add_final_or_states(fst, fst1, fst2, state_table):
    """ Set the accepting-state information for an or-ed fst """
    for agendum, state in state_table.state_map.items():
        state1, state2 = agendum
        finals1 = fst1.finals.get(state1, set())
        finals2 = fst2.finals.get(state2, set())
        if state1 == None and finals2:
            fst.finals[state] = finals2
        elif state2 == None and finals1:
            fst.finals[state] = finals1
        else:
            new_finals = finals1.union(finals2)
            if new_finals:
                fst.finals[state] = new_finals

def sinks_by_tags(fst):
    states = fst.states.items()
    sink_states = filter(lambda x: not x[1].arc_map, states)
    sinks = map(lambda x: x[0], sink_states)
    sinks_by_tag = []

    for sink in sinks:
        tags = fst.finals.get(sink, set())
        groups = list(filter(lambda x: x["tags"] == tags, sinks_by_tag))
        if groups:
            groups[0]["states"].add(sink)
        else:
            sinks_by_tag.append({"tags": tags, "states": {sink}})

    return sinks_by_tag


def drop_sinks(fst, states, first_state):

    def nondup(dict_item):
        state = dict_item[0]
        return (not state in states) or state == first_state
    
    fst.finals = dict(filter(nondup, fst.finals.items()))
    fst.states = dict(filter(nondup, fst.states.items()))


def zip_sinks(fst):
    """ Collapse identical states into a single state """

    sinks_by_tag = sinks_by_tags(fst)
    
    for sink_by_tag in sinks_by_tag:
        states = sink_by_tag["states"]
        first_state = min(states)

        drop_sinks(fst, states, first_state)

        for state in fst.states.values():
            for target, arc in list(state.arc_map.items()):
                if target in states and target != first_state:
                    del state.arc_map[target]
                    if not first_state in state.arc_map:
                        state.arc_map[first_state] = Arc(first_state, None)
                    if arc.get_units():
                        state.arc_map[first_state].add_label(''.join(arc.units))
                    if arc.get_pairs():
                        for pair in arc.pairs:
                            state.arc_map[first_state].add_label(pair)


def remove_fruitless_arcs(fst):
    """ Remove epsilon arcs that point to non-accepting sinks """

    def is_non_accepting_sink(state_entry):
        state_no, state = state_entry
        return not (state_no in fst.finals or state.arc_map)
    
    black_holes = list(map(lambda x: x[0], filter(is_non_accepting_sink, fst.states.items())))

    for source_state in fst.states.values():
        arcs = source_state.arc_map
        for target_no, target_arc in list(arcs.items()):
            if target_arc.target in black_holes:
                eps_pairs = set(filter(lambda x: x[1] == 'epsilon', target_arc.pairs))
                target_arc.pairs -= eps_pairs
                if not (target_arc.get_pairs() or target_arc.get_units()):
                    if target_no in arcs:
                        del arcs[target_no]
                    
    
def init_fst_op(fst1, fst2):
    """ The initial result fst, agenda and state_table for an FST operation """
    ret = FST()
    state_table = StateTable()
    new_initial = (fst1.initial, fst2.initial)
    ret.initial = state_table.find_combo_state(new_initial)
    agenda = [new_initial]

    return ret, agenda, state_table


def and_fst(fst1, fst2):
    """ Return a new FST, running which would be the same as running
        the two given FSTs in parallel """

    ret, agenda, state_table = init_fst_op(fst1, fst2)
    
    while agenda:
        agendum = agenda.pop()
        state1, state2 = agendum
        source = state_table.find_combo_state(agendum)

        arc_list1 = fst1.arc_list(state1)
        arc_list2 = fst2.arc_list(state2)

        #
        # Add the arcs for epsilon transitions
        #
        if arc_list2:
            add_eps_arcs(arc_list1, arc_list2, ret, source, state_table, agenda, True)
        if arc_list1:
            add_eps_arcs(arc_list2, arc_list1, ret, source, state_table, agenda, False)

        for target1, arc1 in arc_list1:
            for target2, arc2 in arc_list2:
                add_and_arcs(ret, source, target1, arc1, target2, arc2, agenda, state_table)

    ret.next = state_table.next_state
    add_final_and_states(ret, fst1, fst2, state_table)
    remove_fruitless_arcs(ret)
    zip_sinks(ret)
    
    return ret


def copy_arc_list(arc_list):
    """ return an ArcList whose arcs are copies of those in the original """
    ret = {}
    for target, arc in arc_list:
        ret[target] = arc.make_copy()

    return ret

def add_or_arcs(fst, source, target1, arc1, target2, arc2, arcs_to_do1, arcs_to_do2, agenda, state_table):
    """ If the labels of the arcs intersect, Add a new arc """

    units = arc1.get_units().intersection(arc2.get_units())
    pairs = arc1.get_pairs().intersection(arc2.get_pairs())

    if units or pairs:
        combo_target = new_target(fst, target1, target2, agenda, state_table)

    if units:
        fst.add_arc(source, combo_target, ''.join(units))
        arcs_to_do1[target1].units -= units
        arcs_to_do2[target2].units -= units
    if pairs:
        for pair in pairs:
            fst.add_arc(source, combo_target, pair)
        arcs_to_do1[target1].pairs -= pairs
        arcs_to_do2[target2].pairs -= pairs
        

def add_idio_arcs(fst, source, target, arc, agenda, state_table, is_fst1):
    """ Add an arc that only exists in one source fst """

    if arc.get_units() or arc.get_pairs():
        if is_fst1:
            combo_target = new_target(fst, target, None, agenda, state_table)
        else:
            combo_target = new_target(fst, None, target, agenda, state_table)

        fst.copy_arc(source, combo_target, arc)
                                
    
def or_fst(fst1, fst2):
    """ Return a new FST accepting all the strings accepted by either input """

    ret, agenda, state_table = init_fst_op(fst1, fst2)

    while agenda:
        agendum = agenda.pop()
        state1, state2 = agendum
        source = state_table.find_combo_state(agendum)

        if state1 == None:
            for target, arc in copy_arc_list(fst2.arc_list(state2)).items():
                add_idio_arcs(ret, source, target, arc, agenda, state_table, False)
        elif state2 == None:
            for target, arc in copy_arc_list(fst1.arc_list(state1)).items():
                add_idio_arcs(ret, source, target, arc, agenda, state_table, True)
        else:
            arc_list1 = fst1.arc_list(state1)
            arc_list2 = fst2.arc_list(state2)

            arcs_to_do1 = copy_arc_list(arc_list1)
            arcs_to_do2 = copy_arc_list(arc_list2)

            for target1, arc1 in arc_list1:
                for target2, arc2 in arc_list2:
                    add_or_arcs(ret, source, target1, arc1, target2, arc2, arcs_to_do1, arcs_to_do2, agenda, state_table)

            for target, arc in arcs_to_do1.items():
                add_idio_arcs(ret, source, target, arc, agenda, state_table, True)

            for target, arc in arcs_to_do2.items():
                add_idio_arcs(ret, source, target, arc, agenda, state_table, False)

        ret.next = state_table.next_state
        add_final_or_states(ret, fst1, fst2, state_table)
        
    return ret


def extend_fsa(fst, word, tags):
    """ Assuming fst is a NFSA, OR a word onto it with the given tags """
    if type(tags) is str:
        tags = {tags}
    source = fst.initial
    for letter in word:
        arcs = fst.states[source].arc_map
        match_arc = first_filter(lambda x: letter in x[1].get_units(), arcs.items())
        if match_arc:
            source = match_arc[0]
        else:
            target = fst.next
            fst.next += 1
            fst.add_arc(source, target, letter)
            source = target

    if source in fst.finals:
        fst.finals[source] |= tags
    else:
        fst.finals[source] = tags
    

def unary_combo(state_num, state_table, is_fst1):
    if is_fst1:
        pair = (state_num, None)
    else:
        pair = (None, state_num)
    return state_table.find_combo_state(pair)


def copy_fst_into(target_fst, source_fst, state_table, is_fst1):
    """ Copy the arcs and finals from one FST to another """
    for source_num, state in source_fst.states.items():
        new_source = unary_combo(source_num, state_table, is_fst1)
        target_fst.states[new_source] = State()
        for target_num, arc in state.arc_map.items():
            new_target = unary_combo(target_num, state_table, is_fst1)
            target_fst.copy_arc(new_source, new_target, arc)

    for final_num, tags in source_fst.finals.items():
        new_final = unary_combo(final_num, state_table, is_fst1)
        target_fst.finals[new_final] = set(tags)


def fix_initial_loop(fst):
    """ Make sure the FST does not contain a self-loop on its initial state """
    initial_num = fst.initial
    initial_arcs = fst.states[initial_num].arc_map.values()
    if any(map(lambda v: v.target == initial_num, initial_arcs)):
        new_initial = fst.next
        fst.next += 1
        fst.states[new_initial] = State()
        fst.initial = new_initial
        if fst.finals[initial_num]:
            fst.finals[new_initial] = set(fst.finals[initial_num])
        for arc in initial_arcs:
            if arc.target == initial_num:
                fst.copy_arc(new_initial, initial_num, arc)
            else:
                fst.copy_arc(new_initial, arc.target, arc)

                
def non_det_or_fst(fst1, fst2):
    """ The same as OrFST, but allow more non-determinism """

    ret = FST()
    state_table = StateTable()

    fix_initial_loop(fst1)
    ret.initial = unary_combo(fst1.initial, state_table, True)
    copy_fst_into(ret, fst1, state_table, True)
    copy_fst_into(ret, fst2, state_table, False)

    initial2_num = fst2.initial
    initial2_state = fst2.states[initial2_num]
    for target_num, arc in initial2_state.arc_map.items():
        new_target = state_table.find_combo_state((None, target_num))
        ret.copy_arc(0, new_target, arc)

    ret.next = state_table.next_state
    return ret

class AzAgendum():
    """ An agendum used for analyzing a string with an FST """

    def __init__(self, state, result):
        self.state = state
        self.result = result


def analyze_eps_arcs(fst, agenda):

    ret = list(agenda)

    while agenda:
        new_agenda = []
        for agendum in agenda:
            state = agendum[0]
            results = list(agendum[1])
            for target, arc in fst.states[state].arc_map.items():
                for pair in arc.get_pairs():
                    if pair[1] == 'epsilon':
                        results = list(agendum[1])
                        results.append(pair[0])
                        new_agenda.append((target, results))
        ret.extend(new_agenda)
        agenda = new_agenda

    return ret

        
def analyze_character(fst, state, char):
    """ Analyze a single letter with an FST """

    ret = []
    for target, arc in fst.states[state].arc_map.items():
        if char in arc.get_units():
            ret.append((target, [char]))
        for pair in arc.get_pairs():
            if char == pair[1]:
                new_char = pair[0]
                if newChar == 'epsilon':
                    ret.append((target, []))
                else:
                    ret.append((target, [new_char]))

    return analyze_eps_arcs(fst, ret)

def analyze_fsa_character(fsa, state, char):
    """ Analyze a single letter with an FSA """
    ret = []
    for target, arc in fsa.states[state].arc_map.items():
        if char in arc.get_units():
            ret.append(target)
    return ret


def analyze_fsa_characters(fsa, state, chars):
    """ Analyze a sequence of characters, return the list of resulting states """
    agenda = [state]
    while agenda and chars:
        char = chars[0]
        chars = chars[1:]
        new_agenda = []
        for source in agenda:
            new_agenda.extend(analyze_fsa_character(fsa, source, char))
        agenda = new_agenda
    return agenda

    
def analyze(fst, utt):
    """ Transduce a string from surface to deep """
    agenda = [AzAgendum(fst.initial, "")]

    utt_to_go = utt
    seen = 0

    while utt_to_go and agenda:
        char = utt_to_go[0]
        utt_to_go = utt_to_go[1:]

        new_agenda = []
        for agendum in agenda:
            seen += 1
            updates = analyze_character(fst, agendum.state, char)
            for update in updates:
                new_agenda.append(AzAgendum(update[0], agendum.result + "".join(update[1])))
        agenda = new_agenda

    ret = {}

    for agendum in agenda:
        state = agendum.state
        result = agendum.result
        if state in fst.finals:
            tags = set(fst.finals[state])
            if result in ret:
                ret[result].update(tags)
            else:
                ret[result] = tags
    return ret
