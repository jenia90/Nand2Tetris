import re

SINGLE_COMMENT = '//'
KEYWORD = 'keyword'
SYMBOL = 'symbol'
IDENTIFIER = 'identifier'
INT_CONST = 'intConstant'
STRING_CONST = 'stringConstant'
TERM = 'term'
OP = 'op'
UOP = 'unaryOp'

CLASS = 'class'
CLASS_VAR_DEC = 'classVarDec'
SUBROUTINE = 'subRoutine'
STATEMENT = 'statement'
VAR_DEC = 'var'


CLASS_VARS = ['static', 'field']
varTypeList = ['int', 'char', 'boolean']
SUBROUTINE_TYPES = ['constructor', 'function', 'method']
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

KEYWORD_REGEX = '(?!\\w)|'.join(KWD_LIST) + '(?!\\w)'
SYMBOL_REGEX = '[' + re.escape('|'.join(SYMBOL_LIST)) + ']'
INT_REGEX = '\\d+'
STR_REGEX = '\"[^\"\\n]*\"'
ID_REGEX = '\\D[\\w]+'
KWD_CONST_REGEX = '(?!\\w)|'.join(KEYWORD_CONSTS) + '(?!\\w)'
OP_REGEX = '[' + re.escape('|'.join(OP_LIST + UOP_LIST)) + ']'
UOP_REGEX = '[-|~]'


class JackTockenizer:
    def __init__(self, file):
        self._lines = [l.split(SINGLE_COMMENT)[0].strip() for l in
                       file.readlines()
                       if not l.strip().startswith(SINGLE_COMMENT)
                       and len(l.strip()) > 0]
        self._removeComments()
        self._splitter = re.compile(KEYWORD_REGEX + '|' + SYMBOL_REGEX + '|' +
                              INT_REGEX + '|' + STR_REGEX + '|' + ID_REGEX)
        self._tokens = [token.strip() for token in
                        self._splitter.findall(''.join(self._lines))]
        print(self._tokens)
        self._currentIndex = 0
        self._currentToken = ''
        self._updateCurrentToken()

    def _removeComments(self):
        newTokens = []
        for i in self._lines:
            if i.startswith('/**'):
                while not i.endswith('*/'):
                    continue
            else:
                newTokens.append(i.strip())

        self._lines = newTokens

    def _updateCurrentToken(self):
        self._currentToken = self._tokens[self._currentIndex]

    def hasMoreTokens(self):
        """
        Checks if there are more tokens in the input.
        :return: true if there are more tokens; false otherwise.
        """
        return self._currentIndex < len(self._tokens)


    def advance(self):
        """
        Get the nest token from the input and makes it the current token.
        """
        if self.hasMoreTokens():
            self._currentIndex += 1
            self._updateCurrentToken()

    def tokenType(self):
        """
        Returns the type of the current token
        :return: Token type constant.
        """
        token = self._currentToken
        print('current token: ' + token)
        if re.match(KEYWORD_REGEX, token) is not None:
            return KEYWORD
        elif re.match(SYMBOL_REGEX, token) is not None:
            return SYMBOL
        elif re.match(INT_REGEX, token) is not None:
            token = int(token)
            if token < INT_MIN or token > INT_MAX:
                return 'ERROR'
            return INT_CONST
        elif re.match(STR_REGEX, token) is not None:
            return STRING_CONST
        elif re.match(ID_REGEX, token) is not None:
            return IDENTIFIER
        elif re.match(INT_REGEX + '|' + STR_REGEX + '|' + KWD_CONST_REGEX +
                              '|' + ID_REGEX, token):
            return TERM
        elif re.match(OP_REGEX, token):
            return OP
        elif re.match(UOP_REGEX, token):
            return UOP
        else:
            return 'ERROR'

    def keyWord(self):
        """
        Returns the keyword which is the current token.
        :return:
        """
        return self._currentToken

    def symbol(self):
        """
        Returns the character which is the current token.
        :return:
        """
        if self._currentToken not in symbolConvertion:
            return self._currentToken

        return symbolConvertion[self._currentToken]

    def identifier(self):
        """
        Returns the identifier which is the current token.
        :return:
        """
        return self._currentToken

    def intVal(self):
        """
        Returns the integer value of the current token
        :return:
        """
        return self._currentToken

    def stringVal(self):
        """
        Returns the string value of the current token, without the double
        quotes.
        :return:
        """
        return self._currentToken[1:-1]
