import xml.etree.cElementTree as ET
import JackTockenizer

class CompilationEngine:
    def __init__(self, tokenizer):
        self._tokenizer = tokenizer
        self._root = ET.Element("class")
        self._tree = ET.ElementTree(self._root)
        self._output = ''

    def CompileClass(self):
        while self._tokenizer.hasMoreCommands():
            currToken = self._tokenizer.tokenType()
            if currToken == KEYWORD:
                ET.SubElement(self._root,KEYWORD).text = self._tokenizer.keyWord()
            elif currToken == SYMBOL:
                ET.SubElement(self._root,SYMBOL).text = self._tokenizer.symbol()
            elif currToken == IDENTIFIER:
                ET.SubElement(self._root,IDENTIFIER).text = self._tokenizer.identifier()
            elif currToken == INT_CONST:
                ET.SubElement(self._root,INT_CONST).text = self._tokenizer.intVal()
            elif currToken == STRING_CONST:
                ET.SubElement(self._root,STRING_CONST).text = self._tokenizer.stringVal()
            else:
                return "ERROR"
        self._tokenizer.advance()

    def CompileClassVarDec(self):
        return

    def CompileSubroutine(self):
        return

    def CompileParameterList(self):
        return

    def CompileVarDec(self):
        return

    def CompileStatements(self):
        return

    def CompileDo(self):
        return

    def CompileLet(self):
        return

    def CompileWhile(self):
        return

    def CompileReturn(self):
        return

    def CompileIf(self):
        return

    def CompileExpression(self):
        return

    def CompileTerm(self):
        return

    def CompileExpressionList(self):
        return
