# Sign objects, pairings of syntactic and semantic information

class Sign():

    def __init__(self, syn_val, sem_val, hooks):
        self.syn_val = syn_val
        self.sem_val = sem_val
        self.hooks = hooks
        self.subcat = []
        self.index_maps = {}


    def __copy__(self):

        ret = Sign(self.syn_val, self.sem_val, self.hooks)
        ret.subcat = self.subcat
        ret.index_maps = self.index_maps

        return ret


    def to_print(self):

        ret = {
            "syn": self.syn_val.to_print(),
            "sem": self.sem_val.to_print(),
            "hooks": self.hooks}

        if self.subcat:
            ret["subcat"] = self.subcat

        if self.index_maps:
            ret["index_maps"] = self.index_maps
            
        return ret
    

