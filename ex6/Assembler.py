import sys

from Code import *
from SymbolTable import *
from Parser import *


def main():
    inp = sys.argv[1]
    file = open(inp, 'r')
    filename = file.name
    sTable = SymbolTable()
    parser = Parser(file, Code)

    while parser.hasMoreCommands():
        if parser.commandType() is L_COMMAND:
            sTable.addEntry(parser.symbol())

        elif parser.commandType() is A_COMMAND and parser.symbol()[0].isalpha():
            sTable.addEntry(parser.symbol())

        parser.advance()



    file.close()

if __name__ == '__main__':
    main()