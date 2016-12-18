import sys
import os

from Code import *
from SymbolTable import *
from Parser import *





def processAddressCommand(symbol, code, sTable):
    """
    Processes address command symbol. If it's already in the table returns it's
    address; otherwise adds to the table and returns the address
    :param symbol: Symbol to process
    :param code: Code table object
    :param sTable: SymbolTable object
    :return: address of the symbol as 16-bit binary representation string
    """
    if symbol[0].isalpha():
        address = sTable.GetAddress(symbol) if sTable.contains(symbol) \
                    else sTable.addEntry(symbol, sTable.GetCurrentAddress())
    else:
        address = symbol
    return code.dec2bin(address)


def firstPassProcessing(parser, sTable):
    index = 0
    while parser.hasMoreCommands():
        if parser.getCurrentType() is L_COMMAND:
            if index is 16:
                index += 1
            sTable.addEntry(parser.symbol(), index)

        else:
            index += 1

        parser.advance()

    parser.resetCount()


def secondPassProcessing(parser, outFile, code, sTable):
    while parser.hasMoreCommands():
        output = ''

        if parser.getCurrentType() is L_COMMAND:
            parser.advance()
            continue
        elif parser.getCurrentType() is A_COMMAND:
            output = processAddressCommand(parser.symbol(), code, sTable)

        elif parser.getCurrentType() is C_COMMAND:
            output = '1'
            output += code.comp(parser.comp()) + \
                      code.dest(parser.dest()) + \
                      code.jump(parser.jump())

        parser.advance()
        outFile.write(output + '\n')


def processFile(file):
    code = Code()
    sTable = SymbolTable()
    infile = open(file, 'r')
    outfile = open(infile.name.split('.')[0] + '.hack', 'w')
    parser = Parser(infile)

    firstPassProcessing(parser, sTable)
    secondPassProcessing(parser, outfile, code, sTable)

    infile.close()
    outfile.close()


def main(args):
    if os.path.isdir(args):
        if not args.endswith(os.sep):
            args += os.sep
        for f in os.listdir(args):
            if f.endswith('.asm'):
                processFile(args + f)

    elif os.path.isfile(args):
        processFile(args)

    else:
        Exception('The input is invalid!\nUsage: Assembler <input>')


if __name__ == '__main__':
    main(sys.argv[1])
