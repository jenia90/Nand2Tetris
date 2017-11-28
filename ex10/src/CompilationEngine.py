from JackTokenizer import JackTokenizer
import xml.etree.ElementTree

class CompilationEngine:
    def __init__(self, in_f, out_f):
        self._in_f, self._out_f = in_f, out_f
        self._tokenizer = JackTokenizer(self._in_f)
        for t in self._tokenizer._tokens:
            print(str(t))
        self.create_tree()

    def create_tree(self):
        pass