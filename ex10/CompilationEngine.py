import xml.etree.ElementTree as ET

from JackTokenizer import JackTokenizer, OPERATORS, \
    UNARY_OPERATORS, CLASS_VARIABLES, \
    SUBROUTINE, CONSTANTS, CONSTANT_TYPES

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

    def __get_next_token(self):
        return ET.fromstring(str(self._tokenizer.advance()))

    def __check_next_value(self):
        return self._tokenizer.next().getValue()

    def __check_next_type(self):
        return self._tokenizer.next().getKind()

    def __check_double_next_value(self):
        return self._tokenizer.double_next().getValue()

    def create_tree(self):
        root = self.compile_class()
        self.indent(root)
        tree = ET.ElementTree(root)
        tree.write(self._out_f, encoding='unicode', short_empty_elements=False)

    def compile_class(self):
        root = ET.Element('class')
        root.append(self.__get_next_token())
        root.append(self.__get_next_token())
        root.append(self.__get_next_token())

        while self.__check_next_value() in CLASS_VARIABLES:
            root.append(self.compile_class_var_dec())
        while self.__check_next_value() in SUBROUTINE:
            root.append(self.compile_subroutine())

        root.append(self.__get_next_token())
        return root

    def indent(self, elem, level=0):
        """
        Prettiefies the output tree structure of the xml
        :param elem: current processed subtree root element
        :param level: recursion and indentation level
        """
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def compile_class_var_dec(self):
        root = ET.Element(CLASS_VAR_DEC)
        root.append(self.__get_next_token())
        root.append(self.__get_next_token())
        root.append(self.__get_next_token())
        while self.__check_next_value() == ',':
            root.append(self.__get_next_token())
            root.append(self.__get_next_token())
        root.append(self.__get_next_token())
        return root

    def compile_subroutine(self):
        root = ET.Element(SUBROUTINE_DEC)
        root.append(self.__get_next_token())
        root.append(self.__get_next_token())
        root.append(self.__get_next_token())
        root.append(self.__get_next_token())
        root.append(self.compile_param_list())
        root.append(self.__get_next_token())
        root.append(self.compile_subroutine_body())

        return root

    def compile_param_list(self):
        root = ET.Element(PARAMETER_LIST)
        if self.__check_next_value() != ')':
            while self.__check_next_type() != 'symbol':
                root.append(self.__get_next_token())
                root.append(self.__get_next_token())
                if self.__check_next_value() == ',':
                    root.append(self.__get_next_token())
        else:
            root.text = '\n'

        return root

    def compile_subroutine_body(self):
        root = ET.Element('subroutineBody')
        root.append(self.__get_next_token())
        while self.__check_next_value() == 'var':
            root.append(self.compile_var_dec())
        root.append(self.compile_statements())
        root.append(self.__get_next_token())
        return root

    def compile_var_dec(self):
        root = ET.Element('varDec')
        root.append(self.__get_next_token())  # var
        root.append(self.__get_next_token())  # type
        root.append(self.__get_next_token())  # name
        while self.__check_next_value() == ',':
            root.append(self.__get_next_token())
            root.append(self.__get_next_token())
        root.append(self.__get_next_token())
        return root

    def compile_statements(self):
        root = ET.Element('statements')
        while self.__check_next_value() in STATEMENTS:
            if self.__check_next_value() == 'let':
                root.append(self.compile_let())
            elif self.__check_next_value() == 'do':
                root.append(self.compile_do())
            elif self.__check_next_value() == 'if':
                root.append(self.compile_if())
            elif self.__check_next_value() == 'while':
                root.append(self.compile_while())
            elif self.__check_next_value() == 'return':
                root.append(self.compile_return())
        return root

    def compile_do(self):
        root = ET.Element(DO_STATEMENT)
        root.append(self.__get_next_token())  # do
        root.extend(self.compile_subroutine_call())
        root.append(self.__get_next_token())
        return root

    def compile_let(self):
        root = ET.Element(LET_STATEMENT)
        root.append(self.__get_next_token())  # let
        root.append(self.__get_next_token())  # varname
        if self.__check_next_value() == '[':
            root.append(self.__get_next_token())  # [
            root.append(self.compile_expression())
            root.append(self.__get_next_token())  # ]
        root.append(self.__get_next_token())  # =
        root.append(self.compile_expression())
        root.append(self.__get_next_token())
        return root

    def compile_while(self):
        root = ET.Element(WHILE_STATEMENT)
        root.append(self.__get_next_token())  # while
        root.append(self.__get_next_token())  # (
        root.append(self.compile_expression())
        root.append(self.__get_next_token())  # )
        root.append(self.__get_next_token())  # {
        root.append(self.compile_statements())
        root.append(self.__get_next_token())  # }
        return root

    def compile_return(self):
        root = ET.Element(RETURN_STATEMENT)
        root.append(self.__get_next_token())
        if self.__check_next_value() != ';':
            root.append(self.compile_expression())
        root.append(self.__get_next_token())
        return root

    def compile_if(self):
        root = ET.Element('ifStatement')
        root.append(self.__get_next_token())  # if
        root.append(self.__get_next_token())  # (
        root.append(self.compile_expression())
        root.append(self.__get_next_token())  # )
        root.append(self.__get_next_token())  # {
        root.append(self.compile_statements())
        root.append(self.__get_next_token())  # }
        if self.__check_next_value() == 'else':
            root.append(self.__get_next_token())  # else
            root.append(self.__get_next_token())  # {
            root.append(self.compile_statements())
            root.append(self.__get_next_token())  # }
        return root

    def compile_expression(self):
        root = ET.Element('expression')
        root.append(self.compile_term())  # (
        while self.__check_next_value() in OPERATORS:
            root.append(self.__get_next_token())  # op
            root.append(self.compile_term())

        return root

    def compile_term(self):
        root = ET.Element('term')
        if self.__check_next_type() in CONSTANT_TYPES or \
                self.__check_next_value() in CONSTANTS:
            root.append(self.__get_next_token())
        elif self.__check_next_type() == 'identifier':
            root.append(self.__get_next_token())
            if self.__check_next_value() == '[':
                root.append(self.__get_next_token())  # [
                root.append(self.compile_expression())
                root.append(self.__get_next_token())  # ]
            if self.__check_next_value() == '(':
                root.append(self.__get_next_token())  # (
                root.append(self.compile_expression_list())
                root.append(self.__get_next_token())  # )
            if self.__check_next_value() == '.':
                root.append(self.__get_next_token())  # .
                root.append(self.__get_next_token())  # subname
                root.append(self.__get_next_token())  # (
                root.append(self.compile_expression_list())
                root.append(self.__get_next_token())  # )
        elif self.__check_next_value() in UNARY_OPERATORS:
            root.append(self.__get_next_token())
            root.append(self.compile_term())
        elif self.__check_next_value() == '(':
            root.append(self.__get_next_token())  # (
            root.append(self.compile_expression())
            root.append(self.__get_next_token())  # )

        return root

    def compile_expression_list(self):
        root = ET.Element('expressionList')
        if self.__check_next_value() != ')':
            root.append(self.compile_expression())
            while self.__check_next_value() == ',':
                root.append(self.__get_next_token())
                root.append(self.compile_expression())
        else:
            root.text = '\n'
        return root

    def compile_subroutine_call(self):
        root = ET.Element('subroutineCall')
        root.append(self.__get_next_token())
        while self.__check_next_value() == '.':
            root.append(self.__get_next_token())
            root.append(self.__get_next_token())
        root.append(self.__get_next_token())
        root.append(self.compile_expression_list())
        root.append(self.__get_next_token())
        return root
