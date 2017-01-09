import re

SINGLE_COMMENT = '//'
KEYWORD = 'keyword'
SYMBOL = 'symbol'
IDENTIFIER = 'identifier'
INT_CONST = 'intConstant'
STRING_CONST = 'stringConstant'

CLASS = 'class'
VARDEC = 'varDec'
SUBROUTINE = 'subRoutine'

classVarList = ['static', 'field']
varTypeList = ['int', 'char', 'boolean']
subroutineTypeList = ['constructor', 'function', 'method']
STATEMENTS = ['if', 'else', 'while', 'return', 'do', 'let']
KEYWORD_CONSTS = ['true', 'false', 'null', 'this']
OP_LIST = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
UOP_LIST = ['-', '~']


KWD_LIST = ['class', 'constructor', 'function', 'method', 'field', 'static',
            'var', 'int', 'char', 'boolean', 'void', 'true', 'false',
            'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']

SYMBOL_LIST = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*',
               '/', '&', '|', '<', '>', '=', '~']

symbolConvertion = {'<': '&lt;', '>': '&gt;', '"': '&quot;', '&': '&amp;'}

INT_MIN = 0
INT_MAX = 32767


class JackTockenizer:
    def __init__(self, file):
        self._tokens = [l.split(SINGLE_COMMENT)[0].strip() for l in
                        file.readlines()
                        if not l.strip().startswith(SINGLE_COMMENT)
                        and len(l.strip()) > 0]
        self.removeComments()
        self.splitSymbols()
        self.currentIndex = 0
        self._currentToken = self._tokens[0]

    def removeComments(self):
        newTokens = []
        for i in self._tokens:
            if i.startswith('/**'):
                while not i.endswith('*/'):
                    continue
            elif i.startswith(SINGLE_COMMENT):
                continue
            else:
                newTokens.append(i)

        self._tokens = newTokens

    def splitSymbols(self):
        newTokens = []
        for token in self._tokens:
            for t in token.split():
                for l in token:
                    if not l.isalpha() and l in SYMBOL_LIST:
                        newTokens.append(l)
                        token.remove(l)
                newTokens.append(t)

        self._tokens = newTokens

    def hasMoreTokens(self):
        """
        Checks if there are more tokens in the input.
        :return: true if there are more tokens; false otherwise.
        """
        return self.currentIndex < len(self._tokens)

    def advance(self):
        """
        Get the nest token from the input and makes it the current token.
        """
        self.currentIndex = (self.currentIndex + 1) % len(self._tokens)
        self._currentToken = self._tokens[self.currentIndex]

    def tokenType(self):
        """
        Returns the type of the current token
        :return: Token type constant.
        """
        token = self._currentToken
        if token in SYMBOL_LIST:
            return SYMBOL
        elif token in KWD_LIST:
            return KEYWORD
        elif INT_MIN < int(token) < INT_MAX:
            return INT_CONST

    def keyWord(self):
        """
        Returns the keyword which is the current token.
        :return:
        """
        return

    def symbol(self):
        """
        Returns the character which is the current token.
        :return:
        """
        return

    def identifier(self):
        """
        Returns the identifier which is the current token.
        :return:
        """
        return

    def intVal(self):
        """
        Returns the integer value of the current token
        :return:
        """
        return

    def stringVal(self):
        """
        Returns the string value of the current token, without the double
        quotes.
        :return:
        """
        return
