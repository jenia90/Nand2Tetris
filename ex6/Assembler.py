import sys
import os

from Code import *
from SymbolTable import *
from Parser import *

DEF_ADDRESS = '0000000000000000'

code = Code()
sTable = SymbolTable()


def dec2bin(address):
    binNum = bin(int(address))[2:]
    return DEF_ADDRESS[:-len(binNum)] + binNum


def processAddressCommand(symbol):
    if symbol[0].isalpha():
        address = sTable.GetAddress(symbol) if sTable.contains(symbol) \
                    else sTable.addEntry(symbol, sTable.GetCurrentAddress())
    else:
        address = symbol
    return dec2bin(address)


def firstPassProcessing(parser):
    index = 0
    while parser.hasMoreCommands():
        if parser.commandType() is L_COMMAND:
            sTable.addEntry(parser.symbol(), index)

        else:
            index += 1

        parser.advance()

    parser.resetCount()


def secondPassProcessing(parser, outFile):
    while parser.hasMoreCommands():
        output = ''

        if parser.commandType() is L_COMMAND:
            parser.advance()
            continue
        elif parser.commandType() is A_COMMAND:
            output = processAddressCommand(parser.symbol())

        elif parser.commandType() is C_COMMAND:
            output = '1'
            output += code.comp(parser.comp()) + \
                      code.dest(parser.dest()) + \
                      code.jump(parser.jump())

        parser.advance()
        outFile.write(output + '\n')


def processFile(file):
    inFile = open(file, 'r')
    outFile = open(inFile.name.split('.')[0] + '.hack', 'w')
    parser = Parser(inFile)

    firstPassProcessing(parser)
    secondPassProcessing(parser, outFile)

    inFile.close()
    outFile.close()


def main(args):
    if os.path.isdir(args):
        for f in os.listdir(args):
            if f.endswith('.asm'):
                processFile(args + f)

    else:
        processFile(args)


if __name__ == '__main__':
    main(sys.argv[1])
