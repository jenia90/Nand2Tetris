import re

from src.Token import Token


class JackTokenizer:
    def __init__(self, file):
        self._keywords = ['class', 'constructor', 'function', 'method', 'field', 'static',
                          'var', 'int', 'char', 'boolean', 'void', 'true', 'false',
                          'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
        self._symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*',
                         '/', '&', '|', '<', '>', '=', '~']
        self._operators = ['+', '-', '*', '/', '|', '=', '&lt;', '&gt;', '&amp;']
        self._un_operators = ['-', '~']
        self._constants = ['true', 'false', 'null', 'this']
        self._class_variables = ['static', 'field']
        self._variables = ['int', 'char', 'boolean']
        self._subroutine = ['constructor', 'function', 'method']

        self.keyword_re = '(?!\\w)|'.join(self._keywords) + '(?!\\w)'
        self.symbol_re = '[' + re.escape('|'.join(self._symbols)) + ']'
        self.int_re = '\\d+'
        self.string_re = '\"[^\"\\n]*\"'
        self.id_re = '[\\w]+'

        self._lines = self.cleanup(file.read())
        self._tokens = self.tokenize()

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


    def double_next(self):
        pass

    def next(self):
        pass
