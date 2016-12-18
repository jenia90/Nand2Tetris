import sys
import os

from Code import *
from SymbolTable import *
from Parser import *

INSTRUCTION_LENGTH = 16

EXT_SEP = '.'
WRONG_USAGE_ERROR = 'The input is invalid!\nUsage: Assembler <input>'
SOURCE_EXT = '.asm'
READ_ACCESS = 'r'
WRITE_ACCESS = 'w'
OUTFILE_EXT = '.hack'
C_COMMAND_PREFIX = '1'


def processAddressCommand(symbol, sym_table):
    """
    Processes address command symbol. If it's already in the table returns it's
    address; otherwise adds to the table and returns the address
    :param symbol: Symbol to process
    :param code: Code table object
    :param sym_table: SymbolTable object
    :return: address of the symbol as 16-bit binary representation string
    """
    if symbol[0].isalpha():
        address = sym_table.GetAddress(symbol) if sym_table.contains(symbol) \
            else sym_table.addEntry(symbol, sym_table.getNextAddress())
    else:
        address = symbol
    return bin(int(address))[2:].zfill(INSTRUCTION_LENGTH)


def labelSymbolProcessing(parser, sym_table):
    """
    Processes the labels in the ASM file and adds them to the symbol table
    :param parser: ASM file parser object
    :param sym_table: symbol table object
    """
    index = 0
    while parser.hasMoreCommands():
        if parser.getCurrentType() is L_COMMAND:
            sym_table.addEntry(parser.symbol(), index)

        else:
            index += 1

        parser.advance()

    parser.resetCount()


def assembling(parser, outfile, code, sym_table):
    """
    Parses each line in the ASM file and converts it into binary representation
    and then writes the binary string to the output file
    :param parser: Parser object
    :param outfile: output file object
    :param code: code table object
    :param sym_table: symbol table object
    """
    while parser.hasMoreCommands():
        if parser.getCurrentType() is L_COMMAND:
            parser.advance()
            continue
        elif parser.getCurrentType() is A_COMMAND:
            output = processAddressCommand(parser.symbol(), sym_table)

        elif parser.getCurrentType() is C_COMMAND:
            output += C_COMMAND_PREFIX + code.comp(parser.comp()) + \
                      code.dest(parser.dest()) + \
                      code.jump(parser.jump())

        parser.advance()
        outfile.write(output + '\n')


def processFile(file):
    """
    Creates a new code and symbol tables for the file and the process each line
    and writes the binary string into the appropriate output file.
    :param file: input file object
    """
    code = Code()
    sym_table = SymbolTable()
    infile = open(file, READ_ACCESS)
    outfile = open(infile.name.split(EXT_SEP)[0] + OUTFILE_EXT, WRITE_ACCESS)
    parser = Parser(infile)

    labelSymbolProcessing(parser, sym_table)
    assembling(parser, outfile, code, sym_table)

    infile.close()
    outfile.close()


def main(args):
    if os.path.isdir(args):  # process directories
        if not args.endswith(os.sep):
            args += os.sep
        for f in os.listdir(args):
            if f.endswith(SOURCE_EXT):
                processFile(args + f)

    elif os.path.isfile(args):  # process single file
        processFile(args)

    else:
        Exception(WRONG_USAGE_ERROR)


if __name__ == '__main__':
    main(sys.argv[1])
