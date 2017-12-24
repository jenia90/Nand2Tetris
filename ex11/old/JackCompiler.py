import os
import sys

import VMWriter as VMW

from old import CompilationEngine as CE

SOURCE_EXT = '.jack'
DEST_EXT = '.vm'

def main(args):
    if args is None:
        Exception("Wrong argument!\nUsage: JackAnalyzer <input file\dir>")

    if os.path.isdir(args):  # process directories
        if not args.endswith(os.sep):
            args += os.sep
        for f in os.listdir(args):
            if f.endswith(SOURCE_EXT):
                in_f = open(args + f, 'r')
                vmwriter = VMW.VMWriter(in_f.name.split(SOURCE_EXT)[0] + DEST_EXT)
                comp_engine = CE.CompilationEngine(in_f, vmwriter)
                comp_engine.CompileClass()
                vmwriter.close()
                in_f.close()

    # process single file
    elif os.path.isfile(args) and args.endswith(SOURCE_EXT):
        in_f = open(args, 'r')
        vmwriter = VMW.VMWriter(in_f.name.split(SOURCE_EXT)[0] + DEST_EXT)
        comp_engine = CE.CompilationEngine(in_f, vmwriter)
        comp_engine.CompileClass()
        vmwriter.close()
        in_f.close()

if __name__ == '__main__':
    main(sys.argv[1])
