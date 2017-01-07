import xml.etree.cElementTree as ET
import JackTockenizer as JT

class CompilationEngine:
    def __init__(self, in_file, out_file):
        self._tokenizer = JT.JackTockenizer(in_file)
        self._root = ET.Element("class")
        self._tree = ET.ElementTree(self._root)

    def CompileClass(self):
        if not (self._tokenizer.tokenType() == JT.KEYWORD):
            return "ERROR"
        else:
            ET.SubElement(self._root, JT.KEYWORD).text = \
                self._tokenizer.keyWord()
        self._tokenizer.advance()
        if not (self._tokenizer.tokenType() == JT.IDENTIFIER):
            return "ERROR"
        else:
            ET.SubElement(self._root, JT.IDENTIFIER).text = \
                self._tokenizer.identifier()
        self._tokenizer.advance()
        if not (self._tokenizer.tokenType() == JT.SYMBOL):
            return "ERROR"
        else:
            ET.SubElement(self._root, JT.SYMBOL).text = \
                self._tokenizer.symbol()
        self._tokenizer.advance()
        while self._tokenizer.tokenType != '}':
            if self._tokenizer.tokenType() == JT.KEYWORD:
                if self._tokenizer.keyWord() == JT.VARDEC:
                    ET.SubElement(self._root, self.CompileClassVarDec())
                elif self._tokenizer.keyWord() == JT.SUBROUTINE:
                    ET.SubElement(self._root, self.CompileSubroutineDec())
            self._tokenizer.advance()

    def CompileClassVarDec(self):
        varDecRoot = ET.Element("classVarDec")
        while self._tokenizer.symbol() is not ';':
            if self._tokenizer.tokenType == JT.KEYWORD:
                ET.SubElement(varDecRoot, JT.KEYWORD).text = \
                    self._tokenizer.keyWord()
            elif self._tokenizer.tokenType() == JT.IDENTIFIER:
                ET.SubElement(varDecRoot, JT.IDENTIFIER).text = \
                    self._tokenizer.identifier()
            elif self._tokenizer.tokenType() == JT.SYMBOL:
                ET.SubElement(varDecRoot, JT.SYMBOL).text = \
                    self._tokenizer.symbol()
            else:
                return "Error"
            self._tokenizer.advance()
        ET.SubElement(varDecRoot, JT.SYMBOL).text = \
            self._tokenizer.symbol()
        return varDecRoot

    def CompileSubroutineDec(self):
        token = self._tokenizer
        subroutineDec = ET.Element("subroutineDec")
        while token.symbol() is not '(':
            if token.tokenType == JT.KEYWORD:
                ET.SubElement(subroutineDec, JT.KEYWORD).text = \
                    token.keyWord()
            elif token.tokenType() == JT.IDENTIFIER:
                ET.SubElement(subroutineDec, JT.IDENTIFIER).text = \
                    token.identifier()
            else:
                return "Error"
            token.advance()
        ET.SubElement(subroutineDec, JT.SYMBOL).text = \
            token.symbol()
        token.advance()
        ET.SubElement(subroutineDec,self.CompileParameterList())
        if (token.symbol() is not ')'):
            return "Error"
        ET.SubElement(subroutineDec, JT.SYMBOL).text = \
            token.symbol()
        token.advance()
        ET.SubElement(subroutineDec,self.CompileSubRoutineBody)
        return subroutineDec

    def CompileSubRoutineBody(self):
        token = self._tokenizer
        subRoutineBody = ET.Element("subroutineBody")
        while token.tokenType() is not '}':
            if token.tokenType() == JT.KEYWORD and token.keyWord() == 'var':
                ET.SubElement(subRoutineBody,self.CompileVarDec)
            elif token.tokenType() == JT.KEYWORD and token.keyWord() in JT.STATEMENTS:
                ET.SubElement(subRoutineBody, self.CompileStatements())
            token.advance()
        if token.symbol() is not '}':
            return 'Error'
        else:
            ET.SubElement(subRoutineBody,token.symbol())
        return subRoutineBody

    def CompileParameterList(self):
        token = self._tokenizer
        parameterList = ET.Element("parameterList")
        while token.symbol() is not ')':
            if token.tokenType() == JT.IDENTIFIER:
                ET.SubElement(parameterList,token.identifier())
            elif token.tokenType() == JT.KEYWORD:
                ET.SubElement(parameterList,token.keyWord())
            elif ET.SubElement() == JT.SYMBOL:
                ET.SubElement(parameterList,token.symbol())
        return parameterList

    def CompileVarDec(self):
        token = self._tokenizer
        varDec = ET.Element("varDec")
        while token.symbol() is not ';':
            if token.tokenType() == JT.IDENTIFIER:
                ET.SubElement(varDec,token.identifier())
            elif token.tokenType() == JT.KEYWORD:
                ET.SubElement(varDec,token.keyWord())
            elif ET.SubElement() == JT.SYMBOL:
                ET.SubElement(varDec,token.symbol())
        return varDec

    def CompileStatements(self):
        token = self._tokenizer
        statements = ET.SubElement("statements")
        if token.keyWord() == 'let':
            ET.SubElement(statements,self.CompileLet())
        elif token.keyWord() == 'if':
            ET.SubElement(statements,self.CompileIf())
        elif token.keyWord() == 'while':
            ET.SubElement(statements,self.CompileWhile())
        elif token.keyWord() == 'do':
            ET.SubElement(statements,self.CompileDo())
        elif token.keyWord() == 'return':
            ET.SubElement(statements,self.CompileReturn())
        return statements

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
