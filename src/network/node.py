# Parser nodes and networks

class Error(Exception):
    pass

class SynCat():

    def __init__(self):
        self.cat = None
        self.features = {}

class LexCat(SynCat):

    def __init__(self):
        SynCat.__init__(self)
        self.lex = {}

class PhraseCat(SynCat):

    def __init__(self):
        SynCat.__init__(self)
        self.filled = []
        self.open = []

class Node():

    def __init__(self):
        self.activation = None
        self.range = None
        self.parents = []
        self.__analysis = None
        self.operations = []

    def AddAnalysis(self, analysis):
        if analysis.cat == Node:
            raise SynCatError(analysis, "No category set")

        self.__analysis = analysis

    def GetAnalysis(self):
        return self.__analysis

class NodeError(Error):

    def __init__(self, node, message):
        self.node = node,
        self.message = message
        
class Network():

    def __init__(self):
        self.__nextNode = 1
        self.__nodes = {}

    def AddNode(self, node):
        if node.activation == None:
            raise NodeError(node, "No activation set")
        elif node.range == None:
            raise NodeError(node, "No range set")
        elif node.analysis == None:
            raise NodeError(node, "No analysis set")
        
        self.nodes[self.nextNode] = node
        self.nextNode += 1

    def GetNode(self, idx):
        return self.__nodes[idx]
