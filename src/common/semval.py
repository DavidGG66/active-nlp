# Semantic classes

class Relspec():

    def __init__(self, rel, roles):

        self.rel = rel
        self.roles = roles


    def ToPrint(self):

        return (self.rel, self.roles)


    def FillerFor(self, roleName):

        return self.roles[roleName]


    def __copy__(self):

        return Relspec(self.rel, self.roles.copy())


class SemValue():

    def __init__(self):

        self.nextIndex = 1
        self.relspecs = []
        self.hooks = {}


    def __copy__(self):

        ret = SemValue()

        ret.nextIndex = self.nextIndex
        ret.relspecs = [x.copy() for x in self.relspecs]
        ret.hooks = self.hooks.copy()

        return ret


    def ToPrint(self):

        relspecs = [x.ToPrint() for x in self.relspecs]

        return (relspecs, self.hooks)

        
    def NextIndex(self):

        ret = "x" + str(self.nextIndex)
        self.nextIndex += 1
        return ret
    
        
    def AddRelspec(self, relspec, hookMatches, exposeHooks):

        bindings = {}
        rel = relspec.rel
        roles = {}
        
        for role, filler in relspec.roles.items():
            if type(filler) is str and filler[0] == "x":
                if filler in bindings:
                    roles[role] = bindings[filler]
                elif filler in hookMatches:
                    useFiller = self.hooks[hookMatches[filler]]
                    bindings[filler] = useFiller
                    roles[role] = useFiller
                else:
                    useFiller = self.NextIndex()
                    bindings[filler] = useFiller
                    roles[role] = useFiller
            else:
                roles[role] = filler

        for hook, filler in exposeHooks.items():
            self.hooks[hook] = bindings[filler]

        self.relspecs.append(Relspec(rel, roles))


    def AddRelspecs(self, relspecs, hookMatches, exposeHooks):

        for relspec in relspecs:
            self.AddRelspec(relspec, hookMatches, exposeHooks)

            
