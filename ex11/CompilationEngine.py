from JackTokenizer import CLASS_VARIABLES, CONSTANTS, CONSTANT_TYPES, \
    JackTokenizer, OPERATORS, SUBROUTINE, UNARY_OPERATORS
from SymbolTable import INC, SymbolTable
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
        self._tokenizer = JackTokenizer(in_f)
        self.vw = VMWriter(out_f)
        self.st = SymbolTable()
        self.class_name = ''

    def __get_next_token(self):
        return self._tokenizer.advance()

    def __check_next_value(self):
        return self._tokenizer.next().get_value()

    def __check_next_type(self):
        return self._tokenizer.next().get_kind()

    def __check_double_next_value(self):
        return self._tokenizer.double_next().get_value()

    def __push_var(self, name):
        kind = self.st.get_kind(name)
        index = self.st.get_index(name)

        if kind == 'var':
            self.vw.write_push('local', index)
        elif kind == 'arg':
            self.vw.write_push('argument', index)
        elif kind == 'static':
            self.vw.write_push('static', index)
        else:
            self.vw.write_push('this', index)

    def __pop_var(self, name):
        kind = self.st.get_kind(name)
        index = self.st.get_index(name)

        if kind == 'var':
            self.vw.write_pop('local', index)
        elif kind == 'arg':
            self.vw.write_pop('argument', index)
        elif kind == 'static':
            self.vw.write_pop('static', index)
        else:
            self.vw.write_pop('this', index)

    def compile_class(self):
        self.__get_next_token()
        self.class_name = str(self.__get_next_token())
        self.st.set_scope('global')
        self.__get_next_token()

        while self.__check_next_value() in CLASS_VARIABLES:
            self.compile_class_var_dec()
        while self.__check_next_value() in SUBROUTINE:
            self.compile_subroutine()

        self.__get_next_token()

    def compile_class_var_dec(self):
        var_kind = str(self.__get_next_token())
        var_type = str(self.__get_next_token())
        var_name = str(self.__get_next_token())
        self.st.new_id(var_kind, var_type, var_name)
        while self.__check_next_value() == ',':
            self.__get_next_token()
            var_name = str(self.__get_next_token())
            self.st.new_id(var_kind, var_type, var_name)
        self.__get_next_token()

    def compile_subroutine(self):
        sub_type = str(self.__get_next_token())
        self.__get_next_token()
        sub_name = self.class_name + '.' + str(self.__get_next_token())
        self.st.new_sub(sub_name)
        self.st.set_scope(sub_name)
        self.__get_next_token()
        self.compile_param_list(sub_type)
        self.__get_next_token()
        self.compile_subroutine_body(sub_name, sub_type)

    def compile_param_list(self, type):
        if type == 'method':
            self.st.new_id('arg', 'self', 'this')
        while self.__check_next_type() != 'symbol':
            p_type = str(self.__get_next_token())
            p_name = str(self.__get_next_token())
            self.st.new_id('arg', p_type, p_name)
            if self.__check_next_value() == ',':
                self.__get_next_token()

    def compile_subroutine_body(self, name, type):
        self.__get_next_token()
        while self.__check_next_value() == 'var':
            self.compile_var_dec()
        n_args = self.st.var_count('var')
        self.vw.write_func(name, n_args)
        self.load_pointer(type)
        self.compile_statements()
        self.__get_next_token()
        self.st.set_scope('global')

    def load_pointer(self, type):
        if type == 'constructor':
            n_args = self.st.var_count('field')
            self.vw.write_push('constant', n_args)
            self.vw.write_func_call('Memory.alloc', 1)
            self.vw.write_pop('pointer', 0)
        elif type == 'method':
            self.vw.write_push('argument', 0)
            self.vw.write_pop('pointer', 0)

    def compile_var_dec(self):
        var_kind = str(self.__get_next_token())
        var_type = str(self.__get_next_token())
        var_name = str(self.__get_next_token())
        self.st.new_id(var_kind, var_type, var_name)
        while self.__check_next_value() == ',':
            self.__get_next_token()
            var_name = str(self.__get_next_token())
            self.st.new_id(var_kind, var_type, var_name)
        self.__get_next_token()

    def compile_statements(self):
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
        self.vw.write_pop('temp', 0)
        self.__get_next_token()

    def compile_let(self):
        self.__get_next_token()  # let
        is_array = False
        var_name = str(self.__get_next_token())  # varname
        if self.__check_next_value() == '[':
            is_array = True
            self.compile_array(var_name)
        self.__get_next_token()  # =
        self.compile_expression()
        self.__get_next_token()
        if is_array:
            self.vw.write_pop('temp', 0)
            self.vw.write_pop('pointer', 1)
            self.vw.write_push('temp', 0)
            self.vw.write_pop('that', 0)
        else:
            if self.st.is_defined(var_name):
                self.__pop_var(var_name)

    def compile_while(self):
        n_while = str(self.st.update_count('while', INC))
        self.vw.write_label('WHILE_EXP' + n_while)
        self.__get_next_token()  # while
        self.__get_next_token()  # (
        self.compile_expression()
        self.vw.write_arithmetic('not')
        self.vw.write_if('WHILE_END' + n_while)
        self.__get_next_token()  # )
        self.__get_next_token()  # {
        self.compile_statements()
        self.vw.write_goto('WHILE_EXP' + n_while)
        self.vw.write_label('WHILE_END' + n_while)
        self.__get_next_token()  # }

    def compile_return(self):
        self.__get_next_token()
        if self.__check_next_value() != ';':
            self.compile_expression()
        else:
            self.vw.write_push('constant', 0)
        self.vw.write_return()
        self.__get_next_token()

    def compile_if(self):
        self.__get_next_token()  # if
        self.__get_next_token()  # (
        self.compile_expression()
        self.__get_next_token()  # )
        n_if = str(self.st.update_count('if', INC))
        self.vw.write_if('IF_TRUE' + n_if)
        self.vw.write_goto('IF_FALSE' + n_if)
        self.vw.write_label('IF_TRUE' + n_if)
        self.__get_next_token()  # {
        self.compile_statements()
        self.__get_next_token()  # }
        if self.__check_next_value() == 'else':
            self.__get_next_token()  # else
            self.vw.write_goto('IF_END' + n_if)
            self.vw.write_label('IF_FALSE' + n_if)
            self.__get_next_token()  # {
            self.compile_statements()
            self.__get_next_token()  # }
            self.vw.write_label('IF_END' + n_if)
        else:
            self.vw.write_label('IF_FALSE' + n_if)

    def compile_expression(self):
        self.compile_term()  # (
        while self.__check_next_value() in OPERATORS:
            _op = str(self.__get_next_token())  # op
            self.compile_term()
            if _op == '+':
                self.vw.write_arithmetic('add')
            elif _op == '-':
                self.vw.write_arithmetic('sub')
            elif _op == '|':
                self.vw.write_arithmetic('or')
            elif _op == '&':
                self.vw.write_arithmetic('and')
            elif _op == '=':
                self.vw.write_arithmetic('eq')
            elif _op == '<':
                self.vw.write_arithmetic('lt')
            elif _op == '>':
                self.vw.write_arithmetic('gt')
            elif _op == '*':
                self.vw.write_func_call('Math.multiply', 2)
            elif _op == '/':
                self.vw.write_func_call('Math.divide', 2)

    def compile_term(self):
        is_array = False
        _type = self.__check_next_type()
        if _type in CONSTANT_TYPES:
            if _type in CONSTANT_TYPES:
                value = str(self.__get_next_token())
                if value in CONSTANTS:
                    if value == 'this':
                        self.vw.write_push('pointer', 0)
                    else:
                        self.vw.write_push('constant', 0)
                        if value == 'true':
                            self.vw.write_arithmetic('not')
            if _type == 'stringConstant':
                self.vw.write_push('constant', len(value))
                self.vw.write_func_call('String.new', 1)
                for l in value:
                    self.vw.write_push('constant', ord(l))
                    self.vw.write_func_call('String.appendChar', 2)
            elif _type == 'integerConstant':
                self.vw.write_push('constant', value)
        elif self.__check_next_value() in CONSTANTS:
            value = str(self.__get_next_token())
            if value == 'this':
                self.vw.write_push('pointer', 0)
            else:
                self.vw.write_push('constant', 0)
                if value == 'true':
                    self.vw.write_arithmetic('not')
        elif _type == 'identifier':
            n_args = 0
            var_name = str(self.__get_next_token())
            if self.__check_next_value() == '[':
                is_array = True
                self.compile_array(var_name)
            if self.__check_next_value() == '(':
                n_args += 1
                self.vw.write_push('pointer', 0)
                self.__get_next_token()  # (
                n_args += self.compile_expression_list()
                self.__get_next_token()  # )
                self.vw.write_func_call(self.class_name + '.' + var_name,
                                        n_args)
            elif self.__check_next_value() == '.':
                self.__get_next_token()  # .
                sub_name = str(self.__get_next_token())  # subname
                if self.st.is_defined(var_name):
                    self.__push_var(var_name)
                    var_name = self.st.get_type(var_name) + '.' + sub_name
                    n_args += 1
                else:
                    var_name = var_name + '.' + sub_name
                self.__get_next_token()  # (
                n_args += self.compile_expression_list()
                self.__get_next_token()  # )
                self.vw.write_func_call(var_name, n_args)
            else:
                if is_array:
                    self.vw.write_pop('pointer', 1)
                    self.vw.write_push('that', 0)
                elif self.st.is_in_current_scope(var_name):
                    kind = self.st.get_kind(var_name, True)
                    index = self.st.get_index(var_name, True)
                    if kind == 'var':
                        self.vw.write_push('local', index)
                    elif kind == 'arg':
                        self.vw.write_push('argument', index)
                else:
                    self.__push_var(var_name)
        elif self.__check_next_value() in UNARY_OPERATORS:
            _op = str(self.__get_next_token())
            self.compile_term()
            if _op == '~':
                self.vw.write_arithmetic('not')
            elif _op == '-':
                self.vw.write_arithmetic('neg')
        elif self.__check_next_value() == '(':
            self.__get_next_token()  # (
            self.compile_expression()
            self.__get_next_token()  # )

    def compile_expression_list(self):
        arg_count = 0
        if self.__check_next_value() != ')':
            self.compile_expression()
            arg_count += 1
            while self.__check_next_value() == ',':
                self.__get_next_token()
                self.compile_expression()
                arg_count += 1
        return arg_count

    def compile_subroutine_call(self):
        n_args = 0
        instance_name = str(self.__get_next_token())
        if self.__check_next_value() == '.':
            self.__get_next_token()
            sub_name = str(self.__get_next_token())
            if self.st.is_defined(instance_name):
                self.__push_var(instance_name)
                full_name = '.'.join(
                        [self.st.get_type(instance_name), sub_name])
                n_args += 1
            else:
                full_name = '.'.join([instance_name, sub_name])
        else:
            self.vw.write_push('pointer', 0)
            n_args += 1
            full_name = '.'.join([self.class_name, instance_name])
        self.__get_next_token()
        n_args += self.compile_expression_list()
        self.vw.write_func_call(full_name, n_args)
        self.__get_next_token()

    def compile_array(self, name):
        self.__get_next_token()
        self.compile_expression()
        self.__get_next_token()
        if self.st.is_defined(name):
            self.__push_var(name)
        self.vw.write_arithmetic('add')
