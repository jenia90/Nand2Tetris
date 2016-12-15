import sys

from Code import *
from SymbolTable import *
from Parser import *

def dec2bin(address):
    binNum = bin(address)[2:]
    return '000000000000000'[:-len(binNum)] + binNum



def main():
    inp = sys.argv[1]
    inFile = open(inp, 'r')
    filename = inFile.name.split('.')[0]
    outFile = open(filename + '.hack', 'w')
    sTable = SymbolTable()
    parser = Parser(inFile, Code)

    while parser.hasMoreCommands():
        if parser.commandType() is L_COMMAND:
            sTable.addEntry(parser.symbol(), parser.currentIndex + 1)

        parser.advance()

    parser.resetCount()

    while parser.hasMoreCommands():
        instruction = ''
        address = ''
        if parser.commandType() is A_COMMAND:
            symbol = parser.symbol()
            if symbol.[0].isalpha():
                if sTable.contains(symbol):
                    outFile.write('1' + dec2bin(sTable.GetAddress(symbol)))
                else:
                    sTable.addEntry(parser.symbol(), sTable)
                    outFile.write('1' + dec2bin(sTable.GetCurrentAddress()))

            else:
                outFile.write('1' + dec2bin(symbol))




    inFile.close()
    outFile.close()

if __name__ == '__main__':
    main()