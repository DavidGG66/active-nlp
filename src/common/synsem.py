# SynSem objects, pairings of syntactic and semantic information

import pprint

import src.common.synval
import src.common.semval

class SynSem():

    def __init__(self, synVal, semVal):
        self.synVal = synVal
        self.semVal = semVal


    def __copy__(self):

        return SynSem(self.synVal.copy(), self.semVal.copy())


    def ToPrint(self):

        return (self.synVal.ToPrint(), self.semVal.ToPrint())

