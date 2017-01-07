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
                        if not l.startswith(SINGLE_COMMENT)
                        and len(l) > 0]
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
        for i in self._tokens:
            for l in i:
                if l in SYMBOL_LIST:
                    newTokens.append(l)
            newTokens.append(i)

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
        while self.hasMoreTokens()
            if
        self.currentIndex += 1

    def validate(self, str):
        if self.re_cond.match(str):
            return

    def tokenType(self):
        """
        Returns the type of the current token
        :return: Token type constant.
        """
        return

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
