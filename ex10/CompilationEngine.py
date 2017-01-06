import xml.etree.cElementTree as ET
import JackTockenizer as JT

class CompilationEngine:
    def __init__(self, in_file, out_file):
        self._tokenizer = JT.JackTockenizer(in_file)
        self._root = ET.Element("class")
        self._tree = ET.ElementTree(self._root)

    def CompileClass(self):
        while self._tokenizer.tokenType != '{':
            currToken = self._tokenizer.tokenType()
            if currToken == JT.KEYWORD:
                ET.SubElement(self._root, JT.KEYWORD).text = \
                    self._tokenizer.keyWord()
            elif currToken == JT.SYMBOL:
                ET.SubElement(self._root, JT.SYMBOL).text = \
                    self._tokenizer.symbol()
            elif currToken == JT.IDENTIFIER:
                ET.SubElement(self._root, JT.IDENTIFIER).text = \
                    self._tokenizer.identifier()
            elif currToken == JT.INT_CONST:
                ET.SubElement(self._root, JT.INT_CONST).text = \
                    self._tokenizer.intVal()
            elif currToken == JT.STRING_CONST:
                ET.SubElement(self._root, JT.STRING_CONST).text = \
                    self._tokenizer.stringVal()
            else:
                return "ERROR"
            self._tokenizer.advance()
        if self._tokenizer.tokenType == '{':
                ET.SubElement(self._root, JT.SYMBOL).text = \
                self._tokenizer.symbol()

            #until here its the class

        self._tokenizer.advance()

        #from here its compileClassVarDec

        while self._tokenizer != 'constructor':
            self.CompileClassVarDec()
            self._tokenizer.advance()

    def CompileClassVarDec(self):
        currToken = self._tokenizer.tokenType()
        classVarDecLeaf = ET.SubElement(self._root, "classVarDec")
        while currToken != ';':
            if currToken == JT.KEYWORD:
                ET.SubElement(classVarDecLeaf, JT.KEYWORD).text = \
                        self._tokenizer.keyWord()
            elif currToken == JT.IDENTIFIER:
                ET.SubElement(classVarDecLeaf, JT.IDENTIFIER).text = \
                        self._tokenizer.identifier()
            elif currToken == JT.SYMBOL:
                ET.SubElement(classVarDecLeaf, JT.SYMBOL).text = \
                self._tokenizer.symbol()
            else:
                return "ERROR"
            self._tokenizer.advance()
        if currToken == ';':
            ET.SubElement(classVarDecLeaf, JT.SYMBOL).text = \
                self._tokenizer.symbol()


    def CompilesubroutineDec(self):
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
