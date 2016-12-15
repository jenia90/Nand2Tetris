import sys

from Code import *
from SymbolTable import *
from Parser import *


def main():
    inp = sys.argv[1]
    file = open(inp, 'r')
    filename = file.name
    parser = Parser(file)

    file.close()



if __name__ == '__main__':
    main()