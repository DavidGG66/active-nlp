# Finite state transducers and such
#
# src.morph.fst
#

from src.common.utils import firstFilter

class Arc():
    """ An arc, consisting of target and labels """
    
    def __init__(self, target, label):
        self.target = target
        self.AddLabel(label)

    def MakeCopy(self):
        ret = Arc(self.target, None)
        if hasattr(self, "units"):
            ret.units = set(self.units)
        if hasattr(self, "pairs"):
            ret.pairs = set(self.pairs)

        return ret

    def Units(self):
        if hasattr(self, "units"):
            return self.units
        else:
            return set()


    def Pairs(self):
        if hasattr(self, "pairs"):
            return self.pairs
        else:
            return set()

        
    def AddUnit(self, s):
        """ Add a string or set of strings to the label units """
        if type(s) is str:
            s = {s}
        if hasattr(self, "units"):
            self.units.update(s)
        else:
            self.units = s

    def AddPair(self, p):
        if hasattr(self, "pairs"):
            self.pairs.add(p)
        else:
            self.pairs = {p}
            
    def AddLabel(self, label):
        """ Add a new label to any existing labels on an arc """
        if type(label) is str:
            if label[0] == "_" and label[-1] == "_":
                self.AddUnit(label)
            else:
                self.AddUnit(set(label))
        elif type(label) is tuple:
            self.AddPair(label)
            

    def ToPrintFromState(self):
        label = []
        if hasattr(self, "units"):
            label.append(''.join(self.units))
        if hasattr(self, "pairs"):
            label.append(self.pairs)
        return label

    def ToPrint(self):
        
        return {
            "target": self.target,
            "label": self.ToPrintFromState()}


class State():
    """ Information about a state

    The arcs leading from it
    The maximum number of characters following it
    """

    def __init__(self):
        self.arcMap = {}

    def AddArc(self, target, label):
        if target in self.arcMap:
            self.arcMap[target].AddLabel(label)
        else:
            self.arcMap[target] = Arc(target, label)

    def ArcList(self):
        return self.arcMap.items()
    
    def ToPrint(self):
        return {k:v.ToPrintFromState() for k,v in self.arcMap.items()}

    
class FST():

    def __init__(self):
        self.initial = 0
        self.finals = {}
        self.next = 1
        self.states = {0: State()}

    def ToPrint(self):
        return {
            "finals": self.finals,
            "states": {k:v.ToPrint() for k,v in self.states.items()}}

    def AddState(self, source):
        if source not in self.states:
            self.states[source] = State()
            
    def AddArc(self, source, target, label):
        """ Add an arc with the given source, target & label """
        if source in self.states:
            self.states[source].AddArc(target, label)
        else:
            state = State()
            state.AddArc(target, label)
            self.states[source] = state

        if target not in self.states:
            self.states[target] = State()

    def CopyArc(self, source, target, arc):
        """ Add an arc with all the labels from a given arc """
        for letter in arc.Units():
            self.AddArc(source, target, letter)
        for pair in arc.Pairs():
            self.AddArc(source, target, pair)

    def ArcList(self, state):
        return self.states[state].ArcList()
    

def WordFST(word, tag):
    """ Make an FST that recognizes a single word with the given tag """
    ret = FST()
    source = ret.initial
    for letter in word:
        target = ret.next
        ret.next += 1
        ret.AddArc(source, target, letter)
        source += 1

    ret.finals = {source: {tag}}
    return ret


class StateTable():

    def __init__(self):
        self.nextState = 0
        self.stateMap = {}


    def __contains__(self, state):
        return state in self.stateMap

    
    def findComboState(self, agendum):
        if agendum not in self.stateMap:
            self.stateMap[agendum] = self.nextState
            self.nextState += 1
        return self.stateMap[agendum]


def ReadFST(fst_data):
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
                    ret.AddArc(source, target, label)

    return ret


def AddAgendum(agenda, agendum, stateTable):
    """ Add a new agenda item, as long as it hasn't already been seen """
    if agendum not in stateTable:
        agenda.append(agendum)

        
def AddEpsArcs(arcList, state, fst, source, stateTable, agenda, epsilon1):
    """ Add arcs following surface epsilon transitions to the new fst """
    for target, arc in arcList:
        epsPairs = list(filter(lambda x: x[1] == 'epsilon', arc.pairs))
        if epsPairs:
            if epsilon1:
                newTarget = (target, state)
            else:
                newTarget = (state, target)
            AddAgendum(agenda, newTarget, stateTable)
            comboTarget = stateTable.findComboState(newTarget)
            fst.AddState(comboTarget)
            for label in epsPairs:
                fst.AddArc(source, comboTarget, label)


def NewAddEpsArcs(epsArcList, otherArcList, fst, source, stateTable, agenda, epsilon1):
    """ Add arcs following surface epsilon transitions to the new fst """
    for epsTarget, epsArc in epsArcList:
        epsPairs = list(filter(lambda x: x[1] == 'epsilon', epsArc.Pairs()))
        if epsPairs:
            for otherTarget, otherArc in otherArcList:
                if otherArc.Units():
                    otherTarget = otherArc.target
                    if epsilon1:
                        newTarget = (epsTarget, otherTarget)
                    else:
                        newTarget = (otherTarget, epsTarget)
                    AddAgendum(agenda, newTarget, stateTable)
                    comboTarget = stateTable.findComboState(newTarget)
                    fst.AddState(comboTarget)
                    for label in epsPairs:
                        fst.AddArc(source, comboTarget, label)

        
def GetMatchPairs(arc1, arc2):
    """ Get pairs where the surface from one matches a string from another """
    ret = {}
    ret.update(filter(lambda x: x[1] in arc2.Units(), arc1.Pairs()))
    ret.update(filter(lambda x: x[1] in arc1.Units(), arc2.Pairs()))
    return ret


def NewTarget(fst, target1, target2, agenda, stateTable):
    """ Make a new target state and add it to the fst and agenda """

    newAgendum = (target1, target2)
    AddAgendum(agenda, newAgendum, stateTable)
    comboTarget = stateTable.findComboState(newAgendum)
    fst.AddState(comboTarget)

    return comboTarget


def AddAndArcs(fst, source, target1, arc1, target2, arc2, agenda, stateTable):
    """ Add arcs for the intersection of the two input arcs """

    units = arc1.Units().intersection(arc2.Units())
    pairs = GetMatchPairs(arc1, arc2)

    if units or pairs:
        comboTarget = NewTarget(fst, target1, target2, agenda, stateTable)

    if units:
        fst.AddArc(source, comboTarget, ''.join(units))
    if pairs:
        for pair in pairs:
            fst.AddArc(source, comboTarget, pair)


def AddFinalAndStates(fst, fst1, fst2, stateTable):
    """ Set the accepting-state information for an anded fst """
    for agendum, state in stateTable.stateMap.items():
        state1, state2 = agendum
        finals1 = fst1.finals.get(state1, set())
        finals2 = fst2.finals.get(state2, set())
        newFinals = finals1.intersection(finals2)
        if newFinals:
            fst.finals[state] = newFinals


def AddFinalOrStates(fst, fst1, fst2, stateTable):
    """ Set the accepting-state information for an or-ed fst """
    for agendum, state in stateTable.stateMap.items():
        state1, state2 = agendum
        finals1 = fst1.finals.get(state1, set())
        finals2 = fst2.finals.get(state2, set())
        if state1 == None and finals2:
            fst.finals[state] = finals2
        elif state2 == None and finals1:
            fst.finals[state] = finals1
        else:
            newFinals = finals1.union(finals2)
            if newFinals:
                fst.finals[state] = newFinals

def SinksByTags(fst):
    states = fst.states.items()
    sinkStates = filter(lambda x: not x[1].arcMap, states)
    sinks = map(lambda x: x[0], sinkStates)
    sinksByTag = []

    for sink in sinks:
        tags = fst.finals.get(sink, set())
        groups = list(filter(lambda x: x["tags"] == tags, sinksByTag))
        if groups:
            groups[0]["states"].add(sink)
        else:
            sinksByTag.append({"tags": tags, "states": {sink}})

    return sinksByTag


def DropSinks(fst, states, firstState):

    def nondup(dictItem):
        state = dictItem[0]
        return (not state in states) or state == firstState
    
    fst.finals = dict(filter(nondup, fst.finals.items()))
    fst.states = dict(filter(nondup, fst.states.items()))

def ZipSinks(fst):
    """ Collapse identical states into a single state """

    sinksByTag = SinksByTags(fst)
    
    for sinkByTag in sinksByTag:
        states = sinkByTag["states"]
        firstState = min(states)

        DropSinks(fst, states, firstState)

        for state in fst.states.values():
            delTargets = []
            for target, arc in list(state.arcMap.items()):
                if target in states and target != firstState:
                    del state.arcMap[target]
                    if not firstState in state.arcMap:
                        state.arcMap[firstState] = Arc(firstState, None)
                    if arc.Units():
                        state.arcMap[firstState].AddLabel(''.join(arc.units))
                    if arc.Pairs():
                        for pair in arc.pairs:
                            state.arcMap[firstState].AddLabel(pair)


def RemoveFruitlessArcs(fst):
    """ Remove epsilon arcs that point to non-accepting sinks """

    def IsNonAcceptingSink(stateEntry):
        stateNo, state = stateEntry
        return not (stateNo in fst.finals or state.arcMap)
    
    blackHoles = list(map(lambda x: x[0], filter(IsNonAcceptingSink, fst.states.items())))

    for sourceNo, sourceState in fst.states.items():
        arcs = sourceState.arcMap
        for targetNo, targetArc in list(arcs.items()):
            if targetArc.target in blackHoles:
                epsPairs = set(filter(lambda x: x[1] == 'epsilon', targetArc.pairs))
                targetArc.pairs -= epsPairs
                if not (targetArc.Pairs() or targetArc.Units()):
                    if targetNo in arcs:
                        del arcs[targetNo]
                    
    
def InitFstOp(fst1, fst2):
    """ The initial result fst, agenda and stateTable for an FST operation """
    ret = FST()
    stateTable = StateTable()
    newInitial = (fst1.initial, fst2.initial)
    ret.initial = stateTable.findComboState(newInitial)
    agenda = [newInitial]

    return ret, agenda, stateTable

def AndFST(fst1, fst2):
    """ Return a new FST, running which would be the same as running
        the two given FSTs in parallel """

    ret, agenda, stateTable = InitFstOp(fst1, fst2)
    
    while agenda:
        agendum = agenda.pop()
        state1, state2 = agendum
        source = stateTable.findComboState(agendum)

        arcList1 = fst1.ArcList(state1)
        arcList2 = fst2.ArcList(state2)

        #
        # Add the arcs for epsilon transitions
        #
        if arcList2:
            NewAddEpsArcs(arcList1, arcList2, ret, source, stateTable, agenda, True)
        if arcList1:
            NewAddEpsArcs(arcList2, arcList1, ret, source, stateTable, agenda, False)

        for target1, arc1 in arcList1:
            for target2, arc2 in arcList2:
                AddAndArcs(ret, source, target1, arc1, target2, arc2, agenda, stateTable)

    ret.next = stateTable.nextState
    AddFinalAndStates(ret, fst1, fst2, stateTable)
    RemoveFruitlessArcs(ret)
    ZipSinks(ret)
    
    return ret


def AndFST1(fst1, fst2):
    """ Return a new FST, running which would be the same as running
        the two given FSTs in parallel """

    ret, agenda, stateTable = InitFstOp(fst1, fst2)
    
    while agenda:
        agendum = agenda.pop()
        state1, state2 = agendum
        source = stateTable.findComboState(agendum)

        arcList1 = fst1.ArcList(state1)
        arcList2 = fst2.ArcList(state2)

        #
        # Add the arcs for epsilon transitions
        #
        if arcList2 or True:
            AddEpsArcs(arcList1, state2, ret, source, stateTable, agenda, True)
        if arcList1 or True:
            AddEpsArcs(arcList2, state1, ret, source, stateTable, agenda, False)

        for target1, arc1 in arcList1:
            for target2, arc2 in arcList2:
                AddAndArcs(ret, source, target1, arc1, target2, arc2, agenda, stateTable)

    AddFinalAndStates(ret, fst1, fst2, stateTable)
    
    return ret


def CopyArcList(arcList):
    """ return an ArcList whose arcs are copies of those in the original """
    ret = {}
    for target, arc in arcList:
        ret[target] = arc.MakeCopy()

    return ret

def AddOrArcs(fst, source, target1, arc1, target2, arc2, arcsToDo1, arcsToDo2, agenda, stateTable):
    """ If the labels of the arcs intersect, Add a new arc """

    units = arc1.Units().intersection(arc2.Units())
    pairs = arc1.Pairs().intersection(arc2.Pairs())

    if units or pairs:
        comboTarget = NewTarget(fst, target1, target2, agenda, stateTable)

    if units:
        fst.AddArc(source, comboTarget, ''.join(units))
        arcsToDo1[target1].units -= units
        arcsToDo2[target2].units -= units
    if pairs:
        for pair in pairs:
            fst.AddArc(source, comboTarget, pair)
        arcsToDo1[target1].pairs -= pairs
        arcsToDo2[target2].pairs -= pairs
        

def AddIdioArcs(fst, source, target, arc, agenda, stateTable, isFst1):
    """ Add an arc that only exists in one source fst """

    if arc.Units() or arc.Pairs():
        if isFst1:
            comboTarget = NewTarget(fst, target, None, agenda, stateTable)
        else:
            comboTarget = NewTarget(fst, None, target, agenda, stateTable)

        fst.CopyArc(source, comboTarget, arc)
                                
    
def OrFST(fst1, fst2):
    """ Return a new FST accepting all the strings accepted by either input """

    ret, agenda, stateTable = InitFstOp(fst1, fst2)

    while agenda:
        agendum = agenda.pop()
        state1, state2 = agendum
        source = stateTable.findComboState(agendum)

        if state1 == None:
            for target, arc in CopyArcList(fst2.ArcList(state2)).items():
                AddIdioArcs(ret, source, target, arc, agenda, stateTable, False)
        elif state2 == None:
            for target, arc in CopyArcList(fst1.ArcList(state1)).items():
                AddIdioArcs(ret, source, target, arc, agenda, stateTable, True)
        else:
            arcList1 = fst1.ArcList(state1)
            arcList2 = fst2.ArcList(state2)

            arcsToDo1 = CopyArcList(arcList1)
            arcsToDo2 = CopyArcList(arcList2)

            for target1, arc1 in arcList1:
                for target2, arc2 in arcList2:
                    AddOrArcs(ret, source, target1, arc1, target2, arc2, arcsToDo1, arcsToDo2, agenda, stateTable)

            for target, arc in arcsToDo1.items():
                AddIdioArcs(ret, source, target, arc, agenda, stateTable, True)

            for target, arc in arcsToDo2.items():
                AddIdioArcs(ret, source, target, arc, agenda, stateTable, False)

        ret.next = stateTable.nextState
        AddFinalOrStates(ret, fst1, fst2, stateTable)
        
    return ret


def ExtendFSA(fst, word, tags):
    """ Assuming fst is a NFSA, OR a word onto it with the given tags """
    if type(tags) is str:
        tags = {tags}
    source = fst.initial
    for letter in word:
        arcs = fst.states[source].arcMap
        matchArc = firstFilter(lambda x: letter in x[1].Units(), arcs.items())
        if matchArc:
            source = matchArc[0]
        else:
            target = fst.next
            fst.next += 1
            fst.AddArc(source, target, letter)
            source = target

    if source in fst.finals:
        fst.finals[source] |= tags
    else:
        fst.finals[source] = tags
    

def UnaryCombo(stateNum, stateTable, isFst1):
    if isFst1:
        pair = (stateNum, None)
    else:
        pair = (None, stateNum)
    return stateTable.findComboState(pair)
        
def CopyFstInto(targetFst, sourceFst, stateTable, isFst1):
    """ Copy the arcs and finals from one FST to another """
    for sourceNum, state in sourceFst.states.items():
        newSource = UnaryCombo(sourceNum, stateTable, isFst1)
        targetFst.states[newSource] = State()
        for targetNum, arc in state.arcMap.items():
            newTarget = UnaryCombo(targetNum, stateTable, isFst1)
            targetFst.CopyArc(newSource, newTarget, arc)

    for finalNum, tags in sourceFst.finals.items():
        newFinal = UnaryCombo(finalNum, stateTable, isFst1)
        targetFst.finals[newFinal] = set(tags)


def FixInitialLoop(fst):
    """ Make sure the FST does not contain a self-loop on its initial state """
    initialNum = fst.initial
    initialArcs = fst.states[initialNum].arcMap.values()
    if any(map(lambda v: v.target == initialNum, initialArcs)):
        newInitial = fst.next
        fst.next += 1
        fst.states[newInitial] = State()
        fst.initial = newInitial
        if fst.finals[initialNum]:
            fst.finals[newInitial] = set(fst.finals[initialNum])
        for arc in initialArcs:
            if arc.target == initialNum:
                fst.CopyArc(newInitial, initialNum, arc)
            else:
                fst.CopyArc(newInitial, arc.target, arc)

                
def NonDetOrFST(fst1, fst2):
    """ The same as OrFST, but allow more non-determinism """

    ret = FST()
    stateTable = StateTable()

    FixInitialLoop(fst1)
    ret.initial = UnaryCombo(fst1.initial, stateTable, True)
    CopyFstInto(ret, fst1, stateTable, True)
    CopyFstInto(ret, fst2, stateTable, False)

    initial2Num = fst2.initial
    initial2State = fst2.states[initial2Num]
    for targetNum, arc in initial2State.arcMap.items():
        newTarget = stateTable.findComboState((None, targetNum))
        ret.CopyArc(0, newTarget, arc)

    ret.next = stateTable.nextState
    return ret

class AzAgendum():
    """ An agendum used for analyzing a string with an FST """

    def __init__(self, state, result):
        self.state = state
        self.result = result


def AnalyzeEpsArcs(fst, agenda):

    ret = list(agenda)

    while agenda:
        newAgenda = []
        for agendum in agenda:
            state = agendum[0]
            results = list(agendum[1])
            for target, arc in fst.states[state].arcMap.items():
                for pair in arc.Pairs():
                    if pair[1] == 'epsilon':
                        results = list(agendum[1])
                        results.append(pair[0])
                        newAgenda.append((target, results))
        ret.extend(newAgenda)
        agenda = newAgenda

    return ret

        
def AnalyzeCharacter(fst, state, char):
    """ Analyze a single letter with an FST """

    ret = []
    for target, arc in fst.states[state].arcMap.items():
        if char in arc.Units():
            ret.append((target, [char]))
        for pair in arc.Pairs():
            if char == pair[1]:
                newChar = pair[0]
                if newChar == 'epsilon':
                    ret.append((target, []))
                else:
                    ret.append((target, [newChar]))

    return AnalyzeEpsArcs(fst, ret)

def Analyze(fst, utt):
    """ Transduce a string from surface to deep """
    agenda = [AzAgendum(fst.initial, "")]

    uttToGo = utt
    seen = 0

    while uttToGo and agenda:
        char = uttToGo[0]
        uttToGo = uttToGo[1:]

        newAgenda = []
        for agendum in agenda:
            seen += 1
            updates = AnalyzeCharacter(fst, agendum.state, char)
            for update in updates:
                newAgenda.append(AzAgendum(update[0], agendum.result + "".join(update[1])))
        agenda = newAgenda

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
