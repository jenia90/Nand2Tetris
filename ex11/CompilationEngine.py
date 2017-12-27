from JackTokenizer import CLASS_VARIABLES, CONSTANTS, CONSTANT_TYPES, \
    JackTokenizer, OPERATORS, SUBROUTINE, UNARY_OPERATORS
from VMWriter import VMWriter

PARAMETER_LIST = 'parameterList'
SUBROUTINE_DEC = 'subroutineDec'
CLASS_VAR_DEC = 'classVarDec'

RETURN_STATEMENT = 'returnStatement'
WHILE_STATEMENT = 'whileStatement'
LET_STATEMENT = 'letStatement'
EXPRESSION_LIST = 'expressionList'
DO_STATEMENT = 'doStatement'

STATEMENTS = ['let', 'do', 'while', 'return', 'if']


class CompilationEngine:
    def __init__(self, in_f, out_f):
        self._in_f, self._out_f = in_f, out_f
        self._tokenizer = JackTokenizer(self._in_f)
        self.vw = VMWriter(out_f)

    def __get_next_token(self):
        self._tokenizer.advance()

    def __check_next_value(self):
        return self._tokenizer.next().getValue()

    def __check_next_type(self):
        return self._tokenizer.next().getKind()

    def __check_double_next_value(self):
        return self._tokenizer.double_next().getValue()

    def compile_class(self):
        self.__get_next_token()
        self.__get_next_token()
        self.__get_next_token()

        while self.__check_next_value() in CLASS_VARIABLES:
            self.compile_class_var_dec()
        while self.__check_next_value() in SUBROUTINE:
            self.compile_subroutine()

        self.__get_next_token()

    def compile_class_var_dec(self):
        self.__get_next_token()
        self.__get_next_token()
        self.__get_next_token()
        while self.__check_next_value() == ',':
            self.__get_next_token()
            self.__get_next_token()
        self.__get_next_token()

    def compile_subroutine(self):
        self.__get_next_token()
        self.__get_next_token()
        self.__get_next_token()
        self.__get_next_token()
        self.compile_param_list()
        self.__get_next_token()
        self.compile_subroutine_body()

    def compile_param_list(self):
        if self.__check_next_value() != ')':
            while self.__check_next_type() != 'symbol':
                self.__get_next_token()
                self.__get_next_token()
                if self.__check_next_value() == ',':
                    self.__get_next_token()

    def compile_subroutine_body(self):
        self.__get_next_token()
        while self.__check_next_value() == 'var':
            self.compile_var_dec()
        self.compile_statements()
        self.__get_next_token()

    def compile_var_dec(self):
        self.__get_next_token()  # var
        self.__get_next_token()  # type
        self.__get_next_token()  # name
        while self.__check_next_value() == ',':
            self.__get_next_token()
            self.__get_next_token()
        self.__get_next_token()

    def compile_statements(self):
        if self.__check_next_value() != '}':
            while self.__check_next_value() in STATEMENTS:
                if self.__check_next_value() == 'let':
                    self.compile_let()
                elif self.__check_next_value() == 'do':
                    self.compile_do()
                elif self.__check_next_value() == 'if':
                    self.compile_if()
                elif self.__check_next_value() == 'while':
                    self.compile_while()
                elif self.__check_next_value() == 'return':
                    self.compile_return()

    def compile_do(self):
        self.__get_next_token()  # do
        self.compile_subroutine_call()
        self.__get_next_token()

    def compile_let(self):
        self.__get_next_token()  # let
        self.__get_next_token()  # varname
        if self.__check_next_value() == '[':
            self.__get_next_token()  # [
            self.compile_expression()
            self.__get_next_token()  # ]
        self.__get_next_token()  # =
        self.compile_expression()
        self.__get_next_token()

    def compile_while(self):
        self.__get_next_token()  # while
        self.__get_next_token()  # (
        self.compile_expression()
        self.__get_next_token()  # )
        self.__get_next_token()  # {
        self.compile_statements()
        self.__get_next_token()  # }

    def compile_return(self):
        self.__get_next_token()
        if self.__check_next_value() != ';':
            self.compile_expression()
        self.__get_next_token()

    def compile_if(self):
        self.__get_next_token()  # if
        self.__get_next_token()  # (
        self.compile_expression()
        self.__get_next_token()  # )
        self.__get_next_token()  # {
        self.compile_statements()
        self.__get_next_token()  # }
        if self.__check_next_value() == 'else':
            self.__get_next_token()  # else
            self.__get_next_token()  # {
            self.compile_statements()
            self.__get_next_token()  # }

    def compile_expression(self):
        self.compile_term()  # (
        while self.__check_next_value() in OPERATORS:
            self.__get_next_token()  # op
            self.compile_term()

    def compile_term(self):
        if self.__check_next_type() in CONSTANT_TYPES or \
                self.__check_next_value() in CONSTANTS:
            self.__get_next_token()
        elif self.__check_next_type() == 'identifier':
            self.__get_next_token()
            if self.__check_next_value() == '[':
                self.__get_next_token()  # [
                self.compile_expression()
                self.__get_next_token()  # ]
            if self.__check_next_value() == '(':
                self.__get_next_token()  # (
                self.compile_expression_list()
                self.__get_next_token()  # )
            if self.__check_next_value() == '.':
                self.__get_next_token()  # .
                self.__get_next_token()  # subname
                self.__get_next_token()  # (
                self.compile_expression_list()
                self.__get_next_token()  # )
        elif self.__check_next_value() in UNARY_OPERATORS:
            self.__get_next_token()
            self.compile_term()
        elif self.__check_next_value() == '(':
            self.__get_next_token()  # (
            self.compile_expression()
            self.__get_next_token()  # )

    def compile_expression_list(self):
        if self.__check_next_value() != ')':
            self.compile_expression()
            while self.__check_next_value() == ',':
                self.__get_next_token()
                self.compile_expression()

    def compile_subroutine_call(self):
        self.__get_next_token()
        while self.__check_next_value() == '.':
            self.__get_next_token()
            self.__get_next_token()
        self.__get_next_token()
        self.compile_expression_list()
        self.__get_next_token()
