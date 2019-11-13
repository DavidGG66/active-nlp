# Syntactic classes

class SynValue():

    def __init__(self, cat, is_lexical):

        self.cat = cat
        self.is_lexical = is_lexical
        self.features = {}


    def __getitem__(self, key):

        return self.features[key]


    def __setitem__(self, key, value):

        self.features[key] = value


    def __copy__(self):

        return SynValue(self.cat, self.isLexical, self.features.copy())


    def to_print(self):

        return (self.cat, self.features)
    

    def lex_syn(cat):

        return SynValue(cat, True)


    def phrase_syn(cat):

        return SynValue(cat, False)
