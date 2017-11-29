from xml.etree.ElementTree import Element

from JackTokenizer import JackTokenizer


class CompilationEngine:
    def __init__(self, in_f, out_f):
        self._in_f, self._out_f = in_f, out_f
        self._tokenizer = JackTokenizer(self._in_f)
        self._tree = self.create_tree()

    def create_tree(self):
        return self.compile_class()

    def compile_class(self):
        root = Element('class')
        self._out_f.write(root)

    def compile_class_var_dec(self):
        pass

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