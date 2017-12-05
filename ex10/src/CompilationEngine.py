import xml.etree.cElementTree as ET


from src.JackTokenizer import JackTokenizer, KEYWORDS, SYMBOLS, OPERATORS, UNARY_OPERATORS, VARIABLES, CLASS_VARIABLES, \
    SUBROUTINE, CONSTANTS


class CompilationEngine:
    def __init__(self, in_f, out_f):
        self._in_f, self._out_f = in_f, out_f
        self._tokenizer = JackTokenizer(self._in_f)
        self.create_tree()

    def __check_next_type(self):
        return self._tokenizer.next().getValue()

    def create_tree(self):
        self.compile_class()

    def compile_class(self):
        root = ET.Element('class')
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        root.append(ET.fromstring(str(self._tokenizer.advance())))
        root.append(ET.fromstring(str(self._tokenizer.advance())))

        next_type = self.__check_next_type()
        if next_type in CLASS_VARIABLES:
            root.append(self.compile_class_var_dec())
        elif next_type in SUBROUTINE:
            root.append(self.compile_subroutine())

        root.append(ET.fromstring(str(self._tokenizer.advance())))
        tree = ET.ElementTree(root)

        tree.write(self._out_f, encoding='unicode', short_empty_elements=False)

    def compile_class_var_dec(self):
        root = ET.Element('classVarDec')
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
        pass

    def compile_param_list(self):
        pass

    def compile_var_dec(self):
        pass

    def compile_statements(self):
        pass

    def compile_do(self):
        pass

    def compile_let(self):
        pass

    def compile_while(self):
        pass

    def compile_return(self):
        pass

    def compile_if(self):
        pass

    def compile_expression(self):
        pass

    def compile_term(self):
        pass

    def compile_expression_list(self):
        pass
