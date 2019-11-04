# SynSem objects, pairings of syntactic and semantic information

import pprint

import src.common.synval
from src.common.semval import SemValue

class SynSem():

    def __init__(self, synVal, semVal):
        if type(semVal) is SemValue:
            semVal = [semVal]
        self.synVal = synVal
        self.semVal = semVal


    def __copy__(self):

        return SynSem(self.synVal.copy(), map(lambda x: x.copy(), self.semVal))


    def ToPrint(self):

        return (self.synVal.ToPrint(), map(lambda x: x.ToPrint(), self.semVal))

