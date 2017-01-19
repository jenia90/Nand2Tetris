STATIC = 'static'
FIELD = 'field'
ARG = 'argument'
LCL = 'local'


class SymbolTable:
    def __init__(self):
        self.classSymbols = dict()
        self.subroutineSymbols = None

    def startSubroutine(self):
        """
        Starts new subroutine scope.
        :return:
        """
        self.subroutineSymbols = dict()

    def define(self, name, type, kind):
        """
        Defines new identifier of the given name, kind and type and assigns
        it a running index. STATIC and FIELD identifiers have a class scope,
        while ARG and VAR identifiers have a subroutine scope.
        :param name: name of the identifier
        :param type: type of the identifier
        :param kind: kind of the identifier
        """
        if kind == STATIC:
            self.classSymbols[kind] = name

    def varCount(self, kind):
        """
        Returns the number of the variables of the given kind already
        defined n the current scope.
        :param kind: kind of the variable.
        :return: number of variables.
        """
        pass

    def kindOf(self, name):
        """
        Returns the kind of the named identifier in the current scope. If
        the identifier is unknown in the current scope, returns None.
        :param name: name of the identifier.
        :return: kind of the identifier.
        """
        pass

    def typeOf(self, name):
        """
        Returns the type of the named identifier in the current scope. If
        the identifier is unknown in the current scope, returns None.
        :param name: name of the identifier.
        :return: type of the identifier
        """
        pass

    def indexOf(self, name):
        """
        Returns the index of the named identifier in the current scope. If
        the identifier is unknown in the current scope, returns None.
        :param name: name of the identifier.
        :return: index of the identifier
        """
        pass