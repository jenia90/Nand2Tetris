import sys

from ex6.Code import *
from ex6.SymbolTable import *

from ex6.Parser import *


def main():
    inp = sys.argv[1]
    file = open(inp, 'r')
    #filename = file.name.split('.', '\\')
    parser = Parser(file)



if __name__ == '__main__':
    main()
