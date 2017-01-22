STATIC = 'static'
FIELD = 'field'
ARG = 'argument'
LCL = 'local'


class SymbolTable:
    def __init__(self):
        self.classSymbols = dict()
        self.symbolCounter = dict()
        self.subroutineSymbols = None

    def countUpdate(self, kind, command=0):
        """
        Updates the symbol counter according to the command
        :param kind: symbol kind
        :param command: 0 - get value (-1 if non existent).
                        1 - increment (or add).
                        2 - decrement (or remove if <0).
                        3 - remove
        :return:
        """
        if kind not in self.symbolCounter:
            self.symbolCounter[kind] = 0
        elif command == 0:
            return self.symbolCounter.get(kind, -1)
        elif command == 1:
            self.symbolCounter[kind] += 1
        elif command == 2:
            self.symbolCounter[kind] -= 1
            if self.symbolCounter[kind] == -1:
                del self.symbolCounter[kind]
                return -1
        elif command == 3:
            del self.symbolCounter[kind]
            return

        return self.symbolCounter[kind]

    def startSubroutine(self):
        """
        Starts new subroutine scope.
        :return:
        """
        self.subroutineSymbols = dict()
        for k in ['constructor', 'function', 'method', 'var', 'if', 'while']:
            self.countUpdate(k, 3)

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
            self.classSymbols[name] = (kind, type, self.countUpdate(kind))
        elif self.subroutineSymbols is not None:
            self.subroutineSymbols[name] = (kind, type, self.countUpdate(kind))

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
            return self.classSymbols[name][0]
        elif name in self.subroutineSymbols:
            return self.subroutineSymbols[name][0]
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
            return self.classSymbols[name][1]
        elif name in self.subroutineSymbols:
            return self.subroutineSymbols[name][1]
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
        elif name in self.subroutineSymbols:
            return self.subroutineSymbols[name][2]
        else:
            return 'ERROR'

    def contains(self, name):
        """
        Checks if a given symbol is in one of the symbol table dictionaries.
        :param name: Symbol to check
        :return: true if the symbol is defined; false otherwise.
        """
        return name in self.classSymbols or \
               name in self.subroutineSymbols
