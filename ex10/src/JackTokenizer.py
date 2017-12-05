import re

from src.Token import Token

KEYWORDS = ['class', 'constructor', 'function', 'method', 'field', 'static',
                          'var', 'int', 'char', 'boolean', 'void', 'true', 'false',
                          'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
SYMBOLS = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*',
                         '/', '&', '|', '<', '>', '=', '~']
OPERATORS = ['+', '-', '*', '/', '|', '=', '&lt;', '&gt;', '&amp;']
UNARY_OPERATORS = ['-', '~']
CONSTANTS = ['true', 'false', 'null', 'this']
CLASS_VARIABLES = ['static', 'field']
VARIABLES = ['int', 'char', 'boolean']
SUBROUTINE = ['constructor', 'function', 'method']
CONSTANT_TYPES = ['integerConstant', 'stringConstant', 'keyword']


class JackTokenizer:
    def __init__(self, file):
        self.keyword_re = '(?!\\w)|'.join(KEYWORDS) + '(?!\\w)'
        self.symbol_re = '[' + re.escape('|'.join(SYMBOLS)) + ']'
        self.int_re = '\\d+'
        self.string_re = '\"[^\"\\n]*\"'
        self.id_re = '[\\w]+'

        self._lines = self.cleanup(file.read())
        self._tokens = self.tokenize()
        self._current_token = ''
        self._current_index = -1

    def cleanup(self, text):

        def replace(m):
            if m.group(1):
                return m.group(1)
            if m.group(2) is not None:
                return ''

        com_reg = re.compile(r'("[^\n]*"(?!\\))|(//[^\n]*$|/(?!\\)\*[\s\S]*?\*(?!\\)/)', re.MULTILINE)
        text = re.sub(com_reg, replace, text)
        return text

    def tokenize(self):

        def get_kind(token):
            if re.match(self.keyword_re, token): return 'keyword'
            elif re.match(self.symbol_re, token): return 'symbol'
            elif re.match(self.int_re, token): return 'integerConstant'
            elif re.match(self.string_re, token): return 'stringConstant'
            elif re.match(self.id_re, token): return 'identifier'
            else: return None

        split_re = re.compile('|'.join([self.keyword_re, self.symbol_re, self.int_re, self.string_re, self.id_re]))
        return [Token(token, get_kind(token)) for token in
                        split_re.findall(self._lines)]

    def has_more_tokens(self):
        return self._current_index < len(self._tokens)

    def advance(self):
        self._current_index += 1
        self._current_token = self._tokens[self._current_index]
        return self._current_token

    def double_next(self):
        return self._tokens[self._current_index + 2]

    def next(self):
        return self._tokens[self._current_index + 1]
