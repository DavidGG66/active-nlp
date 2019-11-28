# Syntactic classes

class SynValue():

    def __init__(self, cat, is_lexical):

        self.cat = cat
        self.is_lexical = is_lexical
        self.features = {}
        self.args = []


    def __getitem__(self, key):

        return self.features[key]


    def __setitem__(self, key, value):

        self.features[key] = value


    def __copy__(self):

        ret = SynValue(self.cat, self.is_lexical)

        ret.features = self.features.copy()
        ret.args = self.args

        return ret


    def to_print(self):

        ret = self.features.copy()
        ret["cat"] = self.cat
        ret["args"] = self.args
        
        return ret
    

    def lex_syn(cat):

        return SynValue(cat, True)


    def phrase_syn(cat):

        return SynValue(cat, False)
