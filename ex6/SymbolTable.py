class SymbolTable:
    """
    Represents a table of all the symbols and variables in RAM
    """
    def __init__(self):
        self.symbols = {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10,
                        'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 'SCREEN': 16384, 'KBD': 24576, 'SP': 0,
                        'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4}
        self.currentAddress = 16

    def addEntry(self, symbol, address):
        """
        Adds a symbol with a given address to the symbol table
        :param symbol: Symbol string to add
        :param address: Address int to add
        :return: the address
        """
        self.symbols[symbol] = address
        return address

    def contains(self, symbol):
        """
        Checks if the given symbol is in the table
        :param symbol: Symbol string to check
        :return: true if in the table; false otherwise
        """
        return symbol in self.symbols

    def GetAddress(self, symbol):
        """
        Returns the address of a given symbol.
        :param symbol: symbol to find
        :return: Address of the symbol
        """
        return self.symbols[symbol]

    def getNextAddress(self):
        """
        Gets the next available address
        :return: int of the next available address
        """
        address = self.currentAddress
        self.currentAddress += 1
        return address