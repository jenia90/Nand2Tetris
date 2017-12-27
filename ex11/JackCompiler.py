import os
import sys

import CompilationEngine as CE

SOURCE_EXT = '.jack'
DEST_EXT = '.xml'


def process_file(f):
    in_f = open(f, 'r')
    out_f = open(in_f.name.split(SOURCE_EXT)[0] + DEST_EXT, 'w')
    c = CE.CompilationEngine(in_f, out_f)
    c.compile_class()
    out_f.close()
    in_f.close()


def main(args):
    if args is None:
        Exception("Wrong argument!\nUsage: JackAnalyzer <input file\dir>")

    if os.path.isdir(args):  # process directories
        if not args.endswith(os.sep):
            args += os.sep
        for f in os.listdir(args):
            if f.endswith(SOURCE_EXT):
                process_file(args + f)

    # process single file
    elif os.path.isfile(args) and args.endswith(SOURCE_EXT):
        process_file(args)


if __name__ == '__main__':
    main(sys.argv[1])
