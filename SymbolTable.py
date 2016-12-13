class SymbolTable:
    def __init__(self):
        self.symbols = dict()

    def addEntry(self, symbol, address):
        dict[symbol] = address

    def contains(self, symbol):
        return not self.symbols.get(symbol)

    def GetAddress(self, symbol):
        return self.symbols.get(symbol)
