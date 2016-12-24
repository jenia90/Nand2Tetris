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
            cw.writeArithmetic(parser.)

        parser.advance()

    return


def main(args):
    if os.path.isdir(args):  # process directories
        cw = CodeWriter(os.path.dirname(args).split(os.sep)[-1])
        if not args.endswith(os.sep):
            args += os.sep
        for f in os.listdir(args):
            if f.endswith(SOURCE_EXT):
                cw.setFileName(f)
                processFile(args + f, cw)

    # process single file
    elif os.path.isfile(args) and args.endswith(SOURCE_EXT):
        cw = CodeWriter(os.path.dirname(args).split(os.sep)[-1])
        processFile(args, cw)

    else:
        Exception(WRONG_USAGE_ERROR)


if __name__ == '__main__':
    main(argv[1])