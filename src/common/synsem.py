# SynSem objects, pairings of syntactic and semantic information

from src.common.semval import SemValue

class SynSem():

    def __init__(self, syn_val, sem_val):
        if type(sem_val) is SemValue:
            sem_val = [sem_val]
        self.syn_val = syn_val
        self.sem_val = sem_val


    def __copy__(self):

        return SynSem(self.syn_val.copy(), map(lambda x: x.copy(), self.sem_val))


    def to_print(self):

        return (self.syn_val.to_print(), map(lambda x: x.to_print(), self.sem_val))

