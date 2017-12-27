GLOBAL_SCOPE = 'global'


class SymbolTable:
    def __init__(self):
        self.classSymbols = {}
        self.symbolCounter = {}
        self.subroutinesDict = {}
        self.currentScopeSymbols = self.classSymbols

    def countUpdate(self, kind, command=0):
        """
        Updates the symbol counter according to the command
        :param kind: symbol kind
        :param command: 0 - get value.
                        1 - increment (or add).
                        2 - reset
        :return:
        """
        count = 0

        if kind not in self.symbolCounter:
            self.symbolCounter[kind] = 0

        if command == 0:
            return self.symbolCounter[kind]
        elif command == 1:
            count = self.symbolCounter[kind]
            self.symbolCounter[kind] += 1
        elif command == 2:
            self.symbolCounter[kind] = 0

        return count

    def startSubroutine(self, name):
        """
        Starts new subroutine scope.
        :return:
        """
        self.subroutinesDict[name] = {}
        for k in ['var', 'if', 'while', 'arg']:
            self.countUpdate(k, 2)

    def define(self, name, type, kind):
        """
        Defines new identifier of the given name, kind and type and assigns
        it a running index. STATIC and FIELD identifiers have a class scope,
        while ARG and VAR identifiers have a subroutine scope.
        :param name: name of the identifier
        :param type: type of the identifier
        :param kind: kind of the identifier
        """
        if kind in ['static', 'field']:
            self.classSymbols[name] = (type, kind,
                                       self.countUpdate(kind, 1))
        elif kind in ['var', 'arg']:
            self.currentScopeSymbols[name] = (type, kind,
                                              self.countUpdate(kind, 1))

    def varCount(self, kind):
        """
        Returns the number of the variables of the given kind already
        defined n the current scope.
        :param kind: kind of the variable.
        :return: number of variables.
        """
        if kind not in self.symbolCounter:
            return 0
        return self.symbolCounter[kind]

    def kindOf(self, name):
        """
        Returns the kind of the named identifier in the current scope. If
        the identifier is unknown in the current scope, returns None.
        :param name: name of the identifier.
        :return: kind of the identifier.
        """
        if name in self.classSymbols:
            return self.classSymbols[name][1]
        elif name in self.currentScopeSymbols:
            return self.currentScopeSymbols[name][1]
        else:
            return 'ERROR'

    def typeOf(self, name):
        """
        Returns the type of the named identifier in the current scope. If
        the identifier is unknown in the current scope, returns None.
        :param name: name of the identifier.
        :return: type of the identifier
        """
        if name in self.classSymbols:
            return self.classSymbols[name][0]
        elif name in self.currentScopeSymbols:
            return self.currentScopeSymbols[name][0]
        else:
            return 'ERROR'

    def indexOf(self, name):
        """
        Returns the index of the named identifier in the current scope. If
        the identifier is unknown in the current scope, returns None.
        :param name: name of the identifier.
        :return: index of the identifier
        """
        if name in self.classSymbols:
            return self.classSymbols[name][2]
        elif name in self.currentScopeSymbols:
            return self.currentScopeSymbols[name][2]
        else:
            return 'ERROR'

    def setScope(self, name):
        if name == 'global':
            self.currentScopeSymbols = self.classSymbols
        else:
            self.currentScopeSymbols = self.subroutinesDict[name]
