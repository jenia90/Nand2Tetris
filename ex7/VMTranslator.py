import os
from sys import argv

from Parser import *
from CodeWriter import *


EXT_SEP = '.'
WRONG_USAGE_ERROR = 'The input is invalid!\nUsage: VMTranslator <input>'
SOURCE_EXT = '.vm'
READ_ACCESS = 'r'


def processFile(file, cw):
    f = open(file, READ_ACCESS)
    parser = Parser(f)

    while parser.hasMoreCommands():
        commandType = parser.commandType()
        if commandType is ARITHMETIC_COMM:
            cw.writeArithmetic(parser.getCommandString())
        elif commandType is POP_COMM or commandType is PUSH_COMM:
            cw.writePushPop(commandType, parser.arg1(),
                            parser.arg2())

        parser.advance()


def main(args):
    if os.path.isdir(args):  # process directories
        if not args.endswith(os.sep):
            args += os.sep
        cw = CodeWriter(os.path.dirname(args) + os.sep+ os.path.dirname(args).split(os.sep)[
            -1] + OUTFILE_EXT)
        for f in os.listdir(args):
            if f.endswith(SOURCE_EXT):
                cw.setFileName(f)
                processFile(args + f, cw)
                cw.close()

    # process single file
    elif os.path.isfile(args) and args.endswith(SOURCE_EXT):
        cw = CodeWriter(args.split(SOURCE_EXT)[0] + OUTFILE_EXT)
        processFile(args, cw)
        cw.close()

    else:
        Exception(WRONG_USAGE_ERROR)


if __name__ == '__main__':
    main(argv[1])