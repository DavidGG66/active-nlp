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

        return Relspec(self.rel, self.roles.copy())


class SemValue():

    def __init__(self):

        self._next_index = 1
        self.relspecs = []
        self.hooks = {}


    def __copy__(self):

        ret = SemValue()

        ret._next_index = self._next_index
        ret.relspecs = [x.copy() for x in self.relspecs]
        ret.hooks = self.hooks.copy()

        return ret


    def to_print(self):

        relspecs = [x.to_print() for x in self.relspecs]

        return (relspecs, self.hooks)

        
    def next_index(self):

        ret = "x" + str(self._next_index)
        self._next_index += 1
        return ret
    
        
    def add_relspec(self, relspec, hook_matches, expose_hooks):

        bindings = {}
        rel = relspec.rel
        roles = {}
        
        for role, filler in relspec.roles.items():
            if type(filler) is str and filler[0] == "x":
                if filler in bindings:
                    roles[role] = bindings[filler]
                elif filler in hook_matches:
                    use_filler = self.hooks[hook_matches[filler]]
                    bindings[filler] = use_filler
                    roles[role] = use_filler
                else:
                    use_filler = self.next_index()
                    bindings[filler] = use_filler
                    roles[role] = use_filler
            else:
                roles[role] = filler

        for hook, filler in expose_hooks.items():
            self.hooks[hook] = bindings[filler]

        self.relspecs.append(Relspec(rel, roles))


    def add_relspecs(self, relspecs, hook_matches, expose_hooks):

        for relspec in relspecs:
            self.add_relspec(relspec, hook_matches, expose_hooks)

            
