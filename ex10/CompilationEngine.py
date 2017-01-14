import xml.etree.cElementTree as ET
from xml.dom import minidom
import JackTockenizer as JT


class CompilationEngine:
    def __init__(self, in_file, out_file):
        self._out_file = out_file
        self._tokenizer = JT.JackTockenizer(in_file)
        self._root = ET.Element("class")

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

        while self._tokenizer.hasMoreTokens():
            if self._tokenizer.tokenType() == JT.KEYWORD:
                if self._tokenizer.keyWord() in JT.CLASS_VARS:
                    self._root.append(self.CompileClassVarDec())
                elif self._tokenizer.keyWord() in JT.SUBROUTINE_TYPES:
                    self._root.append(self.CompileSubroutineDec())
            elif self._tokenizer.tokenType() == JT.SYMBOL and \
                    self._tokenizer.symbol() == '}':
                ET.SubElement(self._root, JT.SYMBOL).text = \
                    self._tokenizer.symbol()
                break
            self._tokenizer.advance()

        self._tree = ET.ElementTree(self._root)
        rough = ET.tostring(self._root)
        reparsed = minidom.parseString(rough)

        self._out_file.write(reparsed.toprettyxml())

    def CompileClassVarDec(self):
        varDecRoot = ET.Element("classVarDec")
        while self._tokenizer.symbol() != ';':
            if self._tokenizer.tokenType() == JT.KEYWORD:
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

        print(varDecRoot)
        return varDecRoot

    def CompileSubroutineDec(self):
        token = self._tokenizer
        subroutineDec = ET.Element("subroutineDec")
        while token.symbol() != '(':
            if token.tokenType() == JT.KEYWORD:
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
        subroutineDec.append(self.CompileParameterList())
        if token.symbol() != ')':
            return "Error"
        ET.SubElement(subroutineDec, JT.SYMBOL).text = \
            token.symbol()
        token.advance()
        subroutineDec.append(self.CompileSubRoutineBody())

        print(subroutineDec)
        return subroutineDec

    def CompileSubRoutineBody(self):
        token = self._tokenizer
        subRoutineBody = ET.Element("subroutineBody")
        while token.symbol() != '}':
            if token.tokenType() == JT.KEYWORD and token.keyWord() == \
                    JT.VAR_DEC:
                subRoutineBody.append(self.CompileVarDec())
            elif token.tokenType() == JT.KEYWORD and \
                            token.keyWord() in JT.STATEMENTS:
                subRoutineBody.append(self.CompileStatements())
            elif token.tokenType() == JT.SYMBOL:
                ET.SubElement(subRoutineBody, JT.SYMBOL).text = token.symbol()
            token.advance()
        if token.symbol() != '}':
            return 'Error'

        ET.SubElement(subRoutineBody, JT.SYMBOL).text = token.symbol()
        token.advance()
        return subRoutineBody

    def CompileParameterList(self):
        token = self._tokenizer
        parameterList = ET.Element("parameterList")
        while token.symbol() != ')':
            if token.tokenType() == JT.IDENTIFIER:
                ET.SubElement(parameterList, JT.IDENTIFIER).text = token.identifier()
            elif token.tokenType() == JT.KEYWORD:
                ET.SubElement(parameterList, JT.KEYWORD).text = token.keyWord()
            elif token.tokenType() == JT.SYMBOL:
                ET.SubElement(parameterList, JT.SYMBOL).text = token.symbol()
            token.advance()

        return parameterList

    def CompileVarDec(self):
        token = self._tokenizer
        varDec = ET.Element("varDec")
        while token.symbol() != ';':
            if token.tokenType() == JT.IDENTIFIER:
                ET.SubElement(varDec, JT.IDENTIFIER).text = token.identifier()
            elif token.tokenType() == JT.KEYWORD:
                ET.SubElement(varDec, JT.KEYWORD).text = token.keyWord()
            elif token.tokenType() == JT.SYMBOL:
                ET.SubElement(varDec, JT.SYMBOL).text = token.symbol()
            token.advance()
        ET.SubElement(varDec, JT.SYMBOL).text = token.symbol()
        return varDec

    def CompileStatements(self):
        token = self._tokenizer
        statements = ET.Element("statements")
        if token.keyWord() == 'let':
            statements.append(self.CompileLet())
        elif token.keyWord() == 'if':
            statements.append(self.CompileIf())
        elif token.keyWord() == 'while':
            statements.append(self.CompileWhile())
        elif token.keyWord() == 'do':
            statements.append(self.CompileDo())
        elif token.keyWord() == 'return':
            statements.append(self.CompileReturn())
        return statements

    def CompileDo(self):
        token = self._tokenizer
        doStatement = ET.Element("doStatement")

        if token.tokenType() is not JT.KEYWORD:
            return "Error"

        ET.SubElement(doStatement, JT.KEYWORD).text = token.keyWord()
        token.advance()

        while token.symbol() != ';':
            if token.tokenType() == JT.IDENTIFIER:
                ET.SubElement(doStatement, JT.IDENTIFIER).text = token.identifier()
            elif token.tokenType() == JT.KEYWORD:
                ET.SubElement(doStatement, JT.KEYWORD).text = token.keyWord()
            elif token.tokenType() == JT.SYMBOL:
                ET.SubElement(doStatement, JT.SYMBOL).text = token.symbol()
            token.advance()

        ET.SubElement(doStatement, JT.SYMBOL).text = token.symbol()
        token.advance()
        return doStatement

    def CompileLet(self):
        token = self._tokenizer
        letStatement = ET.Element("letStatement")
        if token.tokenType() is not JT.KEYWORD:
            return "Error"
        ET.SubElement(letStatement, JT.KEYWORD).text = token.keyWord()
        token.advance()
        ET.SubElement(letStatement, JT.IDENTIFIER).text = token.keyWord()
        token.advance()
        if token.tokenType() == JT.SYMBOL and token.symbol() == '[':
            ET.SubElement(letStatement, JT.SYMBOL).text = token.symbol()
            token.advance()
            letStatement.append(self.CompileExpression())
            token.advance()
            ET.SubElement(letStatement, JT.SYMBOL).text = token.symbol()
            token.advance()
        letStatement.append(self.CompileExpression())
        print(ET.tostring(letStatement))
        return letStatement

    def CompileWhile(self):
        token = self._tokenizer
        whileStatement = ET.Element("whileStatement")
        if token.tokenType() is not JT.KEYWORD:
            return "Error"
        ET.SubElement(whileStatement, JT.KEYWORD).text = token.keyWord()
        token.advance()
        ET.SubElement(whileStatement, JT.SYMBOL).text = token.symbol()
        token.advance()
        whileStatement.append(self.CompileExpression())
        token.advance()
        ET.SubElement(whileStatement, JT.SYMBOL).text = token.symbol()
        token.advance()
        ET.SubElement(whileStatement, JT.SYMBOL).text = token.symbol()
        token.advance()
        whileStatement.append(self.CompileStatements())
        token.advance()
        ET.SubElement(whileStatement, JT.SYMBOL).text = token.symbol()
        return whileStatement

    def CompileReturn(self):
        token = self._tokenizer
        returnStatement = ET.Element("returnStatement")
        if token.tokenType() is not JT.KEYWORD:
            return "Error"
        ET.SubElement(returnStatement, JT.KEYWORD).text = token.keyWord()
        token.advance()
        if token.tokenType() == JT.SYMBOL:
            if token.symbol() == ';':
                ET.SubElement(returnStatement, JT.SYMBOL).text = token.symbol()
                return returnStatement
        returnStatement.append(self.CompileExpression())
        ET.SubElement(returnStatement, JT.SYMBOL).text = token.symbol()
        return returnStatement

    def CompileIf(self):
        token = self._tokenizer
        ifStatement = ET.Element("ifStatement")
        if token.tokenType() is not JT.KEYWORD:
            return "Error"
        ET.SubElement(ifStatement, JT.KEYWORD).text = token.keyWord()
        token.advance()
        ET.SubElement(ifStatement, JT.SYMBOL).text = token.symbol()
        token.advance()
        ifStatement.append(self.CompileExpression())
        ET.SubElement(ifStatement, JT.SYMBOL).text = token.symbol()
        token.advance()
        ET.SubElement(ifStatement, JT.SYMBOL).text = token.symbol()
        token.advance()
        ET.SubElement(ifStatement, JT.SYMBOL).text = token.symbol()
        token.advance()
        ifStatement.append(self.CompileStatements())
        token.advance()
        ET.SubElement(ifStatement, JT.SYMBOL).text = token.symbol()
        token.advance()
        if token.tokenType() is JT.KEYWORD and token.keyWord() == 'else':
            ET.SubElement(ifStatement, token.keyWord())
            token.advance()
            ET.SubElement(ifStatement, JT.SYMBOL).text = token.symbol()
            token.advance()
            ifStatement.append(self.CompileStatements())
            token.advance()
            ET.SubElement(ifStatement, JT.SYMBOL).text = token.symbol()
            token.advance()
        return ifStatement

    def CompileExpression(self):
        token = self._tokenizer
        expression = ET.Element("expression")
        expression.append(self.CompileTerm())
        ET.SubElement(expression, JT.SYMBOL).text = token.symbol()
        token.advance()
        while token.tokenType() is JT.OP:
            if token.tokenType() is JT.OP:
                ET.SubElement(expression, JT.SYMBOL).text = token.symbol()
                token.advance()
        return expression

    def CompileTerm(self):
        token = self._tokenizer
        term = ET.Element("term")
        if token.tokenType() is JT.INT_CONST:
            ET.SubElement(term, JT.INT_CONST).text = token.intVal()
        elif token.tokenType() is JT.STRING_CONST:
            ET.SubElement(term, JT.STRING_CONST).text = token.stringVal()
        elif token.tokenType() in JT.KEYWORD_CONSTS:
            ET.SubElement(term, JT.KEYWORD_CONSTS).text = token.keyWord()
        elif token.tokenType() is JT.IDENTIFIER:
            ET.SubElement(term, JT.IDENTIFIER).text = token.identifier()
            token.advance()
            # varName
            if token.tokenType() is JT.SYMBOL:
                if token.symbol() == '[':
                    ET.SubElement(term, JT.SYMBOL).text = token.symbol()
                    token.advance()
                    term.append(self.CompileExpression())
                    token.advance()
                    ET.SubElement(term, JT.SYMBOL).text = token.symbol()
                    token.advance()
                elif token.symbol() == '.':
                    while token.symbol() != '(':
                        ET.SubElement(term, JT.SYMBOL).text = token.symbol()
                        token.advance()
                        ET.SubElement(term, JT.IDENTIFIER).text = token.identifier()
                        token.advance()
                    ET.SubElement(term, JT.SYMBOL).text = token.symbol()
                    token.advance()
                    term.append(self.CompileExpressionList())
                    ET.SubElement(term, JT.SYMBOL).text = token.symbol()
                    token.advance()
        return term

    def CompileExpressionList(self):
        token = self._tokenizer
        expressionList = ET.Element("expressionList")
        while token.symbol() != ')' and token.symbol() != ';':
            expressionList.append(self.CompileExpression())
            token.advance()
        return expressionList
