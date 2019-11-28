# Sign objects, pairings of syntactic and semantic information

from src.common.semval import SemValue

class Sign():

    def __init__(self):
        self.syn_val = None
        self.sem_val = []
        self.hooks = {}
        self.subcat = []
        self.index_maps = {}


    def add_sem_val(self, sem_val):
        this.sem_val.append(sem_val)


    def __copy__(self):

        ret = Sign()
        ret.syn_val = self.syn_val
        ret.sem_val = self.sem_val
        ret.hooks = self.hooks
        ret.subcat = self.subcat
        ret.index_maps = self.index_maps

        return ret


    def to_print(self):

        ret = {
            "syn": self.syn_val.to_print(),
            "sem": list(map(lambda x: x.to_print(), self.sem_val)),
            "hooks": self.hooks}

        if self.subcat:
            ret["subcat"] = self.subcat

        if self.index_maps:
            ret["index_maps"] = self.index_maps
            
        return ret
    

