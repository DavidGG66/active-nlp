# Syntactic classes

import pprint

class SynValue():

    def __init__(self, cat, isLexical):

        self.cat = cat
        self.isLexical = isLexical
        self.features = {}


    def __getitem__(self, key):

        return self.features[key]


    def __setitem__(self, key, value):

        self.features[key] = value


    def __copy__(self):

        return SynValue(self.cat, self.isLexical, self.features.copy())


    def ToPrint(self):

        return (self.cat, self.features)
    

    def LexSyn(cat):

        return SynValue(cat, True)


    def PhraseSyn(cat):

        return SynValue(cat, False)
