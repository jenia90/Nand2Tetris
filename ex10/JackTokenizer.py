import re

SINGLE_COMMENT = '//'

IDENTIFIER = "identifier"
STRING_CONSTANT = "stringConstant"
INTEGER_CONSTANT = "integerConstant"
SYMBOL = "symbol"
KEYWORD = "keyword"

KWD_LIST = ['class', 'constructor', 'function', 'method', 'field', 'static',
            'var', 'int', 'char', 'boolean', 'void', 'true', 'false',
            'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']

SYMBOL_LIST = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*',
                '/', '&', '|', '<', '>', '=', '~']
symbolConvertion = {'<': '&lt;', '>': '&gt;', '"': '&quot;', '&': '&amp;'}

OP_LIST = ['+', '-', '*', '/', '|', '=', '&lt;', '&gt;', '&amp;']
UOP_LIST = ['-', '~']
KWD_CONSTS = ['true', 'false', 'null', 'this']
CLASS_VARS = ['static', 'field']
VAR_TYPES = ['int', 'char', 'boolean']
SUBROUTINE_TYPES = ['constructor', 'function', 'method']
KEYWORD_CONSTS = ['true', 'false', 'null', 'this']

KEYWORD_REGEX = '(?!\\w)|'.join(KWD_LIST) + '(?!\\w)'
SYMBOL_REGEX = '[' + re.escape('|'.join(SYMBOL_LIST)) + ']'
INT_REGEX = '\\d+'
STR_REGEX = '\"[^\"\\n]*\"'
ID_REGEX = '[\\w]+'


str_commnent_regex = '(\"(?:\\[\S\s]|[^"\\])*\"|\'(?:\\[\S\s]|[^"\\])\'|[' \
                     '\S\s][^/\"\'\\]*)'

class JackTokenizer:
    def __init__(self, file):
        """
        Opens the input file/stream and gets ready
        to tokenize it
        """
        self._file = file
        self._lines = [l.strip() for l in
                       file.readlines()
                       if not l.strip().startswith(SINGLE_COMMENT)
                       and len(l.strip()) > 0]
        self._lines = self._removeComments()
        self._splitter = re.compile(KEYWORD_REGEX + '|' + SYMBOL_REGEX + '|' +
                                    INT_REGEX + '|' + STR_REGEX + '|' + ID_REGEX)
        self._tokens = [self.procToken(token.strip()) for token in
                        self._splitter.findall(''.join(self._lines))]
        self._currToken = ""

    def _removeComments(self):
        """ Removes comments from the file string """
        newTokens = []
        for i in self._lines:
            m = re.match(r'([^\"].*\"[^/]*(//.*))', i)
            comment = False
            if i.startswith('/**') or i.startswith('*'):
                comment = True
            if i.endswith('*/'):
                comment = False
                continue
            if not comment:
                if m is not None:
                    newTokens.append(i[:i.index(m.group(2))].strip())
                else:
                    newTokens.append(i.split(SINGLE_COMMENT)[0].strip())

        return newTokens

    def procToken(self, token):
        if re.match(KEYWORD_REGEX, token) is not None:
            return KEYWORD, token
        elif re.match(SYMBOL_REGEX, token) is not None:
            return SYMBOL, self.replace(token)
        elif re.match(INT_REGEX, token) is not None:
            return INTEGER_CONSTANT, token
        elif re.match(STR_REGEX, token) is not None:
            return STRING_CONSTANT, token[1:-1]
        else:
            return IDENTIFIER, token

    def replace(self, token):
        if token not in symbolConvertion:
            return token
        return symbolConvertion[token]

    def hasMoreTokens(self):
        return self._tokens != []

    def advance(self):
        self._currToken = self._tokens.pop(0)
        return self._currToken

    def peek(self):
        if self.hasMoreTokens():
            return self._tokens[0]
        else:
            return ("ERROR", 0)

    def getToken(self):
        """
        returns the type of the current token
        """
        return self._currToken[0]

    def getValue(self):
        """
        returns the current value
        """
        return self._currToken[1]
