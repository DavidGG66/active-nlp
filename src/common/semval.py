# Semantic classes

class Relspec():

    def __init__(self, rel, roles):

        self.rel = rel
        self.roles = roles


    def to_print(self):

        return (self.rel, self.roles)


    def filler_for(self, roleName):

        return self.roles[roleName]


    def __copy__(self):

        return Relspec(self.rel, self.roles)


class SemValue():

    def __init__(self):

        self.relspecs = []


    def __copy__(self):

        ret = SemValue()

        ret.relspecs = self.relspecs.copy()

        return ret


    def to_print(self):

        return [x.to_print() for x in self.relspecs]

            
    def add_relspec(self, relspec):
        self.relspecs.append(relspec)


    def add_relspecs(self, relspecs):

        for relspec in relspecs:
            self.add_relspec(relspec)

            
