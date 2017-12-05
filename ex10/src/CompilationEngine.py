import xml.etree.cElementTree as ET


from src.JackTokenizer import JackTokenizer, KEYWORDS, SYMBOLS, OPERATORS, UNARY_OPERATORS, VARIABLES, CLASS_VARIABLES, \
    SUBROUTINE, CONSTANTS

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
        self.create_tree()

    def __check_next_type(self):
        return self._tokenizer.next().getValue()

    def __check_double_next_type(self):
        return self._tokenizer.double_next().getValue()

    def create_tree(self):
        self.compile_class()

    def compile_class(self):
        root = ET.Element('class')
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        root.append(ET.fromstring(str(self._tokenizer.advance())))

        if self.__check_next_type() in CLASS_VARIABLES:
            root.append(self.compile_class_var_dec())
        while self.__check_next_type() in SUBROUTINE:
            root.append(self.compile_subroutine())

        root.append(ET.fromstring(str(self._tokenizer.advance())))
        tree = ET.ElementTree(root)

        tree.write(self._out_f, encoding='unicode', short_empty_elements=False)

    def compile_class_var_dec(self):
        root = ET.Element(CLASS_VAR_DEC)
        while self.__check_next_type() in CLASS_VARIABLES:
            root.append(ET.fromstring(str(self._tokenizer.advance())))
            root.append(ET.fromstring(str(self._tokenizer.advance())))
            root.append(ET.fromstring(str(self._tokenizer.advance())))
            while self.__check_next_type() == ',':
                root.append(ET.fromstring(str(self._tokenizer.advance())))
                root.append(ET.fromstring(str(self._tokenizer.advance())))
            root.append(ET.fromstring(str(self._tokenizer.advance())))
        return root

    def compile_subroutine(self):
        root = ET.Element(SUBROUTINE_DEC)
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        if self.__check_next_type() != ')':
            root.append(self.compile_param_list())
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        root.append(self.compile_subroutine_body())

        return root

    def compile_param_list(self):
        root = ET.Element(PARAMETER_LIST)
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        while self.__check_next_type() == ',':
            root.append(ET.fromstring(str(self._tokenizer.advance())))
            root.append(ET.fromstring(str(self._tokenizer.advance())))
        return root

    def compile_subroutine_body(self):
        root = ET.Element('subroutineBody')
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        while self.__check_next_type() == 'var':
            root.append(self.compile_var_dec())
        root.append(self.compile_statements())
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        return root

    def compile_var_dec(self):
        root = ET.Element('varDec')
        root.append(ET.fromstring(str(self._tokenizer.advance())))  # var
        root.append(ET.fromstring(str(self._tokenizer.advance())))  # type
        root.append(ET.fromstring(str(self._tokenizer.advance())))  # name
        while self.__check_next_type() == ',':
            root.append(ET.fromstring(str(self._tokenizer.advance())))
            root.append(ET.fromstring(str(self._tokenizer.advance())))
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        return root

    def compile_statements(self):
        root = ET.Element('statements')
        while self.__check_next_type() in STATEMENTS:
            print(self.__check_next_type())
            if self.__check_next_type() == 'let':
                root.append(self.compile_let())
            elif self.__check_next_type() == 'do':
                root.append(self.compile_do())
            elif self.__check_next_type() == 'if':
                root.append(self.compile_if())
            elif self.__check_next_type() == 'while':
                root.append(self.compile_while())
            elif self.__check_next_type() == 'return':
                root.append(self.compile_return())

        return root

    def compile_do(self):
        root = ET.Element(DO_STATEMENT)
        root.append(ET.fromstring(str(self._tokenizer.advance())))  # do
        root.append(self.compile_subroutine_call())
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        return root

    def compile_let(self):
        root = ET.Element(LET_STATEMENT)
        root.append(ET.fromstring(str(self._tokenizer.advance())))  # let
        root.append(ET.fromstring(str(self._tokenizer.advance())))  # varname
        if self.__check_next_type() == '[':
            root.append(ET.fromstring(str(self._tokenizer.advance())))  # [
            root.append(self.compile_expression())
            root.append(ET.fromstring(str(self._tokenizer.advance())))  # ]
        root.append(ET.fromstring(str(self._tokenizer.advance())))  # =
        root.append(self.compile_expression())
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        return root

    def compile_while(self):
        root = ET.Element(WHILE_STATEMENT)
        # TODO: Implement.
        return root

    def compile_return(self):
        root = ET.Element(RETURN_STATEMENT)
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        if self.__check_next_type() != ';':
            self.compile_expression()
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        return root

    def compile_if(self):
        root = ET.Element('ifStatement')
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        root.append(self.compile_expression())
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        root.append(self.compile_statements())
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        if self.__check_next_type() == 'else':
            root.append(ET.fromstring(str(self._tokenizer.advance())))
            root.append(ET.fromstring(str(self._tokenizer.advance())))
            root.append(self.compile_statements())
            root.append(ET.fromstring(str(self._tokenizer.advance())))
        return root

    def compile_expression(self):
        root = ET.Element('expression')
        root.append(self.compile_term())
        # TODO: Fix expression/term prints

        return root

    def compile_term(self):
        root = ET.Element('term')

        if self.__check_double_next_type() == '.':
            root.append(self.compile_subroutine_call())

        elif self.__check_next_type() == '(':
            root.append(ET.fromstring(str(self._tokenizer.advance())))
            root.append(self.compile_expression())
            root.append(ET.fromstring(str(self._tokenizer.advance())))

        elif self.__check_next_type() in UNARY_OPERATORS:
            root.append(ET.fromstring(str(self._tokenizer.advance())))
            root.append(self.compile_term())

        else:
            root.append(ET.fromstring(str(self._tokenizer.advance())))
            if self.__check_next_type() == '[':
                root.append(ET.fromstring(str(self._tokenizer.advance())))
                root.append(self.compile_expression())
                root.append(ET.fromstring(str(self._tokenizer.advance())))
            if self.__check_next_type() in UNARY_OPERATORS:
                root.append(ET.fromstring(str(self._tokenizer.advance())))
                root.append(ET.fromstring(str(self._tokenizer.advance())))

        return root

    def compile_expression_list(self):
        root = ET.Element('expressionList')
        root.append(self.compile_expression())
        while self.__check_next_type() == ',':
            root.append(self.compile_expression())
        return root

    def compile_subroutine_call(self):
        root = ET.Element('subroutineCall')
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        while self.__check_next_type() != '(':
            root.append(ET.fromstring(str(self._tokenizer.advance())))
            root.append(ET.fromstring(str(self._tokenizer.advance())))
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        if self.__check_next_type() != ')':
            root.append(self.compile_expression_list())
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        return root
