import sys, os
import CompilationEngine as CE

SOURCE_EXT = '.jack'
DEST_EXT = '.xml'

def main(args):
    if args is None:
        Exception("Wrong argument!\nUsage: JackAnalyzer <input file\dir>")

    if os.path.isdir(args):  # process directories
        if not args.endswith(os.sep):
            args += os.sep
        for f in os.listdir(args):
            if f.endswith(SOURCE_EXT):
                in_f = open(args + f, 'r')
                out_f = open(in_f.name.split(SOURCE_EXT)[0] + DEST_EXT, 'w')
                comp_engine = CE.CompilationEngine(in_f, out_f)
                comp_engine.CompileClass()
                out_f.close()
                in_f.close()

    # process single file
    elif os.path.isfile(args) and args.endswith(SOURCE_EXT):
        in_f = open(args, 'r')
        out_f = open(in_f.name.split(SOURCE_EXT)[0] + DEST_EXT, 'w')
        comp_engine = CE.CompilationEngine(in_f, out_f)
        comp_engine.CompileClass()
        out_f.close()
        in_f.close()


if __name__ == '__main__':
    main(sys.argv[1])
