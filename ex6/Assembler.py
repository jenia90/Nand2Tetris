import sys

from Code import *
from SymbolTable import *
from Parser import *

DEF_ADDRESS = '0000000000000000'

code = Code()
sTable = SymbolTable()


def dec2bin(address):
    binNum = bin(int(address))[2:]
    return DEF_ADDRESS[:-len(binNum)] + binNum


def parseAddressCommand(symbol):
    if symbol[0].isalpha():
        address = sTable.GetAddress(symbol) if sTable.contains(symbol) \
                    else sTable.addEntry(symbol, sTable.GetCurrentAddress())
    else:
        address = symbol

    return dec2bin(address)


def parseLabels(parser):
    index = 0
    while parser.hasMoreCommands():
        if parser.commandType() is L_COMMAND:
            sTable.addEntry(parser.symbol(), index)

        else:
            index += 1

        parser.advance()

    parser.resetCount()


def parseToFile(parser, outFile):
    while parser.hasMoreCommands():
        output = ''

        if parser.commandType() is L_COMMAND:
            parser.advance()
            continue
        elif parser.commandType() is A_COMMAND:
            output = parseAddressCommand(parser.symbol())

        elif parser.commandType() is C_COMMAND:
            output = '1'
            output += code.comp(parser.comp()) + \
                      code.dest(parser.dest()) + \
                      code.jump(parser.jump())

        parser.advance()
        outFile.write(output + '\n')


def main(args):
    inFile = open(args, 'r')
    outFile = open(inFile.name.split('.')[0] + '.hack', 'w')
    parser = Parser(inFile)

    parseLabels(parser)
    parseToFile(parser, outFile)

    inFile.close()
    outFile.close()


if __name__ == '__main__':
    main(sys.argv[1])
