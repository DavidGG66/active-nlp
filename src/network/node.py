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

    def add_analysis(self, analysis):
        if analysis.cat == None:
            raise SynCatError(analysis, "No category set")

        self.__analysis = analysis

    def get_analysis(self):
        return self.__analysis

class NodeError(Error):

    def __init__(self, node, message):
        self.node = node,
        self.message = message
        
class Network():

    def __init__(self):
        self.__next_node = 1
        self.__nodes = {}

    def add_node(self, node):
        if node.activation == None:
            raise NodeError(node, "No activation set")
        elif node.range == None:
            raise NodeError(node, "No range set")
        elif node.analysis == None:
            raise NodeError(node, "No analysis set")
        
        self.__nodes[self.__next_node] = node
        self.next_node += 1

    def get_node(self, idx):
        return self.__nodes[idx]
