import sys
from Parser import *
from Code import *
from SymbolTable import *

def main():
    inp = sys.argv[1]
    file = open(inp, 'r')
    filename = file.name.split('.')[0]
    parser = Parser(file)

if __name__ == '__main__':
    main()
