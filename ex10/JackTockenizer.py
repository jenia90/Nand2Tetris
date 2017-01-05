import re

GRP_TYPE_IDX = 1

IF_EXPR_IDX = 2
IF_STMNT_IDX = 3
ELIF_STMNT_IDX = 4

VAR_NAME_IDX = 2
ARR_LEN_IDX = 3
ASS_IDX = 4

DO_ROUTINE_IDX = 2

RET_IDX = 2

IF_EXP = '(if|while)\h+\(\h*([^)]+)\h*\)\s*\{\s*([^}]+)\s*\}\s*' \
         '(?:(else)\s*\{([^)]+)\})?'
LET_EXP = '^(let)\h+(\D[^\[ ]*)(?:\[(\d+)\])?\h*=\h*([^;]+);$'
DO_EXP = '^(do)\h+(\D[^;]*);$'
RET_EXP = '^(return)(?:\h*([^;]+))?;$'

KWD_LIST = ['class', 'constructor', 'function', 'method', 'field', 'static',
            'var', 'int', 'char', 'boolean', 'void', 'true', 'false',
            'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']

SYMBOL_LIST = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*',
               '/', '&', '|', '<', '>', '=', '~']

INT_MIN = 0
INT_MAX = 32767


class JackTockenizer:
    def __init__(self):
        self.re_cond = re.compile(IF_EXP)
        self.re_let = re.compile(LET_EXP)
        self.re_do = re.compile(DO_EXP)
        self.re_ret = re.compile(RET_EXP)
        return

    def hasMoreTokens(self):
        return

    def advance(self):
        return

    def tokenType(self):
        return

    def keyWord(self):
        return

    def symbol(self):
        return

    def identifier(self):
        return

    def intVal(self):
        return

    def stringVal(self):
        return
