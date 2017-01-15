import xml.etree.ElementTree as ET
from xml.dom import minidom
import JackTockenizer as JT


class CompilationEngine:
    def __init__(self, in_file, out_file):
        self._out_file = out_file
        self._tokenizer = JT.JackTockenizer(in_file)
        self._root = ET.Element("class")
        self.spacer = lambda x: ' ' + x + ' '

    def CompileClass(self):
        ET.SubElement(self._root, JT.KEYWORD).text = self.spacer(
                self._tokenizer.keyWord())
        self._tokenizer.advance()
        ET.SubElement(self._root, JT.IDENTIFIER).text = self.spacer(self._tokenizer.identifier())
        self._tokenizer.advance()
        ET.SubElement(self._root, JT.SYMBOL).text = self.spacer(
                self._tokenizer.symbol())
        self._tokenizer.advance()

        while self._tokenizer.symbol() != '}':
            if self._tokenizer.tokenType() == JT.KEYWORD:
                if self._tokenizer.keyWord() in JT.CLASS_VARS:
                    self._root.append(self.CompileClassVarDec())
                elif self._tokenizer.keyWord() in JT.SUBROUTINE_TYPES:
                    self._root.append(self.CompileSubroutineDec())
            self._tokenizer.advance()

        ET.SubElement(self._root, JT.SYMBOL).text = self.spacer(
                self._tokenizer.symbol())

        self._out_file.write(self.prettify(self._root))

    def prettify(self, element):
        rough = ET.tostring(element, short_empty_elements=False)
        reparsed = minidom.parseString(rough)
        return reparsed.toprettyxml(indent='  ')

    def CompileClassVarDec(self):
        t = self._tokenizer
        varDecRoot = ET.Element("classVarDec")
        while self._tokenizer.symbol() != ';':
            if self._tokenizer.tokenType() == JT.KEYWORD:
                ET.SubElement(varDecRoot, JT.KEYWORD).text = \
                    self.spacer(t.keyWord())
            elif self._tokenizer.tokenType() == JT.IDENTIFIER:
                ET.SubElement(varDecRoot, JT.IDENTIFIER).text = \
                    self.spacer(t.identifier())
            elif self._tokenizer.tokenType() == JT.SYMBOL:
                ET.SubElement(varDecRoot, JT.SYMBOL).text = \
                    self.spacer(t.symbol())
            else:
                return "Error"
            self._tokenizer.advance()
        ET.SubElement(varDecRoot, JT.SYMBOL).text = \
            self.spacer(t.symbol())

        print(self.prettify(varDecRoot))
        return varDecRoot

    def CompileSubroutineDec(self):
        t = self._tokenizer
        subroutineDec = ET.Element("subroutineDec")
        ET.SubElement(subroutineDec, JT.KEYWORD).text = \
            self.spacer(t.keyWord())
        t.advance()
        ET.SubElement(subroutineDec, t.tokenType()).text = \
            self.spacer(t.keyWord())
        t.advance()
        ET.SubElement(subroutineDec, JT.IDENTIFIER).text = \
            self.spacer(t.identifier())
        t.advance()
        
        ET.SubElement(subroutineDec, JT.SYMBOL).text = self.spacer(t.symbol())
        t.advance()
        subroutineDec.append(self.CompileParameterList())
        ET.SubElement(subroutineDec, JT.SYMBOL).text = self.spacer(t.symbol())
        t.advance()
        
        subroutineDec.append(self.CompileSubRoutineBody())
        
        print(self.prettify(subroutineDec))
        return subroutineDec

    def CompileSubRoutineBody(self):
        t = self._tokenizer
        subRoutineBody = ET.Element("subroutineBody")
        while t.symbol() != '}':
            if t.tokenType() == JT.KEYWORD and t.keyWord() == \
                    JT.VAR_DEC:
                subRoutineBody.append(self.CompileVarDec())
            elif t.tokenType() == JT.KEYWORD and \
                            t.keyWord() in JT.STATEMENTS:
                subRoutineBody.append(self.CompileStatements())
            elif t.tokenType() == JT.SYMBOL:
                ET.SubElement(subRoutineBody, JT.SYMBOL).text = \
                    self.spacer(t.symbol())
                t.advance()

        ET.SubElement(subRoutineBody, JT.SYMBOL).text = self.spacer(t.symbol())
        print(self.prettify(subRoutineBody))
        return subRoutineBody

    def CompileParameterList(self):
        t = self._tokenizer
        parameterList = ET.Element("parameterList")
        while t.symbol() != ')':
            if t.tokenType() == JT.IDENTIFIER:
                ET.SubElement(parameterList, JT.IDENTIFIER).text = self.spacer(t.identifier())
            elif t.tokenType() == JT.KEYWORD:
                ET.SubElement(parameterList, JT.KEYWORD).text = self.spacer(t.keyWord())
            elif t.tokenType() == JT.SYMBOL:
                ET.SubElement(parameterList, JT.SYMBOL).text = \
                    self.spacer(t.symbol())
            t.advance()

        print(self.prettify(parameterList))
        return parameterList

    def CompileVarDec(self):
        t = self._tokenizer
        varDec = ET.Element("varDec")
        while t.symbol() != ';':
            if t.tokenType() == JT.IDENTIFIER:
                ET.SubElement(varDec, JT.IDENTIFIER).text = self.spacer(t.identifier())
            elif t.tokenType() == JT.KEYWORD:
                ET.SubElement(varDec, JT.KEYWORD).text = self.spacer(t.keyWord())
            elif t.tokenType() == JT.SYMBOL:
                ET.SubElement(varDec, JT.SYMBOL).text = self.spacer(t.symbol())
            t.advance()
        ET.SubElement(varDec, JT.SYMBOL).text = self.spacer(t.symbol())
        t.advance()

        print(self.prettify(varDec))
        return varDec

    def CompileStatements(self):
        t = self._tokenizer
        statements = ET.Element("statements")
        while t.symbol() != '}':
            if t.keyWord() == 'let':
                statements.append(self.CompileLet())
            elif t.keyWord() == 'if':
                statements.append(self.CompileIf())
            elif t.keyWord() == 'while':
                statements.append(self.CompileWhile())
            elif t.keyWord() == 'do':
                statements.append(self.CompileDo())
            elif t.keyWord() == 'return':
                statements.append(self.CompileReturn())

        print(self.prettify(statements))
        return statements

    def CompileDo(self):
        t = self._tokenizer
        doStatement = ET.Element("doStatement")
        ET.SubElement(doStatement, JT.KEYWORD).text = self.spacer(t.keyWord())
        t.advance()
        ET.SubElement(doStatement, JT.IDENTIFIER).text = self.spacer(t.identifier())
        t.advance()
        if t.symbol() == '.':
            ET.SubElement(doStatement, JT.SYMBOL).text = self.spacer(t.symbol())
            t.advance()
            ET.SubElement(doStatement, JT.IDENTIFIER).text = self.spacer(
                t.identifier())
            t.advance()
        ET.SubElement(doStatement, JT.SYMBOL).text = self.spacer(t.symbol())
        t.advance()
        doStatement.append(self.CompileExpressionList())
        ET.SubElement(doStatement, JT.SYMBOL).text = self.spacer(t.symbol())
        t.advance()
        ET.SubElement(doStatement, JT.SYMBOL).text = self.spacer(t.symbol())
        t.advance()
        print(self.prettify(doStatement))
        return doStatement

    def CompileLet(self):
        t = self._tokenizer
        letStatement = ET.Element("letStatement")

        ET.SubElement(letStatement, JT.KEYWORD).text = self.spacer(t.keyWord())
        t.advance()
        ET.SubElement(letStatement, JT.IDENTIFIER).text = self.spacer(t.identifier())
        t.advance()
        if t.tokenType() == JT.SYMBOL and t.symbol() == '[':
            ET.SubElement(letStatement, JT.SYMBOL).text = self.spacer(t.symbol())
            t.advance()
            letStatement.append(self.CompileExpression())
            t.advance()
            ET.SubElement(letStatement, JT.SYMBOL).text = self.spacer(t.symbol())
            t.advance()
        ET.SubElement(letStatement,
                      JT.SYMBOL).text = self.spacer(t.symbol())
        t.advance()
        letStatement.append(self.CompileExpression())
        if t.symbol() != ';':
            t.advance()
        ET.SubElement(letStatement, JT.SYMBOL).text = self.spacer(t.symbol())
        t.advance()

        print(self.prettify(letStatement))
        return letStatement

    def CompileWhile(self):
        t = self._tokenizer
        whileStatement = ET.Element("whileStatement")
        ET.SubElement(whileStatement, JT.KEYWORD).text = self.spacer(t.keyWord())
        t.advance()
        ET.SubElement(whileStatement, JT.SYMBOL).text = self.spacer(t.symbol())
        t.advance()
        whileStatement.append(self.CompileExpression())
        while t.tokenType() is JT.SYMBOL:
            ET.SubElement(whileStatement, JT.SYMBOL).text = self.spacer(t.symbol())
            t.advance()
        whileStatement.append(self.CompileStatements())
        ET.SubElement(whileStatement, JT.SYMBOL).text = self.spacer(t.symbol())
        t.advance()

        print(self.prettify(whileStatement))
        return whileStatement

    def CompileReturn(self):
        t = self._tokenizer
        returnStatement = ET.Element("returnStatement")
        ET.SubElement(returnStatement, JT.KEYWORD).text = self.spacer(t.keyWord())
        t.advance()
        if t.symbol() != ';':
            returnStatement.append(self.CompileExpression())
            if t.symbol() == ';':
                ET.SubElement(returnStatement, JT.SYMBOL).text = self.spacer(
                    t.symbol())
                t.advance()
                return returnStatement
            t.advance()
        ET.SubElement(returnStatement, JT.SYMBOL).text = self.spacer(t.symbol())
        t.advance()

        print(self.prettify(returnStatement))
        return returnStatement

    def CompileIf(self):
        t = self._tokenizer
        ifStatement = ET.Element("ifStatement")
        ET.SubElement(ifStatement, JT.KEYWORD).text = self.spacer(t.keyWord())
        t.advance()
        ET.SubElement(ifStatement, JT.SYMBOL).text = self.spacer(t.symbol())
        t.advance()
        ifStatement.append(self.CompileExpression())
        if t.symbol() != ')':
            t.advance()
        ET.SubElement(ifStatement, JT.SYMBOL).text = self.spacer(t.symbol())
        t.advance()
        ET.SubElement(ifStatement, JT.SYMBOL).text = self.spacer(t.symbol())
        t.advance()
        ifStatement.append(self.CompileStatements())
        ET.SubElement(ifStatement, JT.SYMBOL).text = self.spacer(t.symbol())
        t.advance()
        if t.keyWord() == 'else':
            ET.SubElement(ifStatement, JT.KEYWORD).text = self.spacer(t.keyWord())
            t.advance()
            ET.SubElement(ifStatement, JT.SYMBOL).text = self.spacer(t.symbol())
            t.advance()
            ifStatement.append(self.CompileStatements())
            ET.SubElement(ifStatement, JT.SYMBOL).text = self.spacer(t.symbol())
        t.advance()

        print(self.prettify(ifStatement))
        return ifStatement

    def CompileExpression(self):
        t = self._tokenizer
        expression = ET.Element("expression")
        expression.append(self.CompileTerm())
        while t.symbol() in JT.OP_LIST:
            ET.SubElement(expression, JT.SYMBOL).text = self.spacer(t.symbol())
            t.advance()
            expression.append(self.CompileTerm())

        print(self.prettify(expression))
        return expression

    def CompileTerm(self):
        t = self._tokenizer
        term = ET.Element("term")
        if t.tokenType() is JT.INT_CONST:
            ET.SubElement(term, JT.INT_CONST).text = self.spacer(t.intVal())
        elif t.tokenType() is JT.STRING_CONST:
            ET.SubElement(term, JT.STRING_CONST).text = self.spacer(t.stringVal())
        elif t.keyWord() in JT.KEYWORD_CONSTS:
            ET.SubElement(term, JT.KEYWORD).text = self.spacer(t.keyWord())
            t.advance()
        elif t.tokenType() is JT.IDENTIFIER:
            ET.SubElement(term, JT.IDENTIFIER).text = self.spacer(t.identifier())
            t.advance()

            if t.symbol() == '[':
                ET.SubElement(term, JT.SYMBOL).text = self.spacer(t.symbol())
                t.advance()
                term.append(self.CompileExpression())
                t.advance()
                ET.SubElement(term, JT.SYMBOL).text = self.spacer(t.symbol())
            elif t.symbol() == '(':
                ET.SubElement(term, JT.SYMBOL).text = self.spacer(t.symbol())
                t.advance()
                term.append(self.CompileExpressionList())
                ET.SubElement(term, JT.SYMBOL).text = self.spacer(t.symbol())
            elif t.symbol() == '.':
                ET.SubElement(term, JT.SYMBOL).text = self.spacer(t.symbol())
                t.advance()
                ET.SubElement(term, JT.IDENTIFIER).text = self.spacer(t.identifier())
                t.advance()
                ET.SubElement(term, JT.SYMBOL).text = self.spacer(t.symbol())
                t.advance()
                term.append(self.CompileExpressionList())
                ET.SubElement(term, JT.SYMBOL).text = self.spacer(t.symbol())
                t.advance()
        elif t.tokenType() is JT.SYMBOL:
            if t.symbol() in JT.UOP_LIST:
                ET.SubElement(term, JT.SYMBOL).text = self.spacer(t.symbol())
                t.advance()
                term.append(self.CompileTerm())
            elif t.symbol() == '(':
                ET.SubElement(term, JT.SYMBOL).text = self.spacer(t.symbol())
                t.advance()
                term.append(self.CompileExpression())
                if t.symbol() != ')':
                    t.advance()
                ET.SubElement(term, JT.SYMBOL).text = self.spacer(t.symbol())
                t.advance()

            else:
                ET.SubElement(term, JT.SYMBOL).text = self.spacer(t.symbol())
                t.advance()

        print(self.prettify(term))
        return term

    def CompileExpressionList(self):
        t = self._tokenizer
        expressionList = ET.Element("expressionList")
        while t.symbol() != ')' and t.symbol() != ';':
            if t.symbol() == ',':
                ET.SubElement(expressionList, JT.SYMBOL).text = self.spacer(t.symbol())
                t.advance()
            expressionList.append(self.CompileExpression())
            if t.symbol() != ')':
                t.advance()

        print(self.prettify(expressionList))
        return expressionList