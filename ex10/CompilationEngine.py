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
        ET.SubElement(subroutineDec, self.CompileParameterList())
        if token.symbol() is not ')':
            return "Error"
        ET.SubElement(subroutineDec, JT.SYMBOL).text = \
            token.symbol()
        token.advance()
        ET.SubElement(subroutineDec, self.CompileSubRoutineBody)
        return subroutineDec

    def CompileSubRoutineBody(self):
        token = self._tokenizer
        subRoutineBody = ET.Element("subroutineBody")
        while token.tokenType() is not '}':
            if token.tokenType() == JT.KEYWORD and token.keyWord() == 'var':
                ET.SubElement(subRoutineBody, self.CompileVarDec)
            elif token.tokenType() == JT.KEYWORD and \
                            token.keyWord() in JT.STATEMENTS:
                ET.SubElement(subRoutineBody, self.CompileStatements())
            token.advance()
        if token.symbol() is not '}':
            return 'Error'
        else:
            ET.SubElement(subRoutineBody, token.symbol())
        return subRoutineBody

    def CompileParameterList(self):
        token = self._tokenizer
        parameterList = ET.Element("parameterList")
        while token.symbol() is not ')':
            if token.tokenType() == JT.IDENTIFIER:
                ET.SubElement(parameterList, token.identifier())
            elif token.tokenType() == JT.KEYWORD:
                ET.SubElement(parameterList, token.keyWord())
            elif token.tokenType() == JT.SYMBOL:
                ET.SubElement(parameterList, token.symbol())
        return parameterList

    def CompileVarDec(self):
        token = self._tokenizer
        varDec = ET.Element("varDec")
        while token.symbol() is not ';':
            if token.tokenType() == JT.IDENTIFIER:
                ET.SubElement(varDec, token.identifier())
            elif token.tokenType() == JT.KEYWORD:
                ET.SubElement(varDec, token.keyWord())
            elif token.tokenType() == JT.SYMBOL:
                ET.SubElement(varDec, token.symbol())
        return varDec

    def CompileStatements(self):
        token = self._tokenizer
        statements = ET.Element("statements")
        if token.keyWord() == 'let':
            ET.SubElement(statements, self.CompileLet())
        elif token.keyWord() == 'if':
            ET.SubElement(statements, self.CompileIf())
        elif token.keyWord() == 'while':
            ET.SubElement(statements, self.CompileWhile())
        elif token.keyWord() == 'do':
            ET.SubElement(statements, self.CompileDo())
        elif token.keyWord() == 'return':
            ET.SubElement(statements, self.CompileReturn())
        return statements

    def CompileDo(self):
        token = self._tokenizer
        doStatement = ET.Element("doStatement")
        if token.tokenType is not JT.KEYWORD:
            return "Error"
        ET.SubElement(doStatement, token.keyWord())
        token.advance()
        # subroutinecall from here
        if token.tokenType is not JT.IDENTIFIER:
            return "Error"
        ET.SubElement(doStatement, token.identifier())
        token.advance()
        if token.tokenType is JT.SYMBOL:
            ET.SubElement(doStatement, token.symbol())
            token.advance()
            ET.SubElement(doStatement, self.CompileExpressionList)
            token.advance()
            ET.SubElement(doStatement, token.symbol())
        else:
            ET.SubElement(doStatement, token.identifier())
            token.advance()
            ET.SubElement(doStatement, token.symbol())
            token.advance()
            ET.SubElement(doStatement, token.identifier())
            token.advance()
            ET.SubElement(doStatement, token.symbol())
            token.advance()
            ET.SubElement(doStatement, self.CompileExpressionList())
            token.advance()
            ET.SubElement(doStatement, token.symbol())
        return doStatement

    def CompileLet(self):
        token = self._tokenizer
        letStatement = ET.Element("letStatement")
        if token.tokenType is not JT.KEYWORD:
            return "Error"
        ET.SubElement(letStatement, token.keyWord())
        token.advance()
        ET.SubElement(letStatement, token.identifier())
        token.advance()
        if token.tokenType() == JT.SYMBOL:
            if token.symbol() == '[':
                ET.SubElement(letStatement, token.symbol())
                token.advance()
                ET.SubElement(letStatement, self.CompileExpression())
                token.advance()
        ET.SubElement(letStatement, token.symbol())
        token.advance()
        ET.SubElement(letStatement, self.CompileExpression())
        token.advance()
        ET.SubElement(letStatement, token.symbol())
        return letStatement

    def CompileWhile(self):
        token = self._tokenizer
        whileStatement = ET.Element("whileStatement")
        if token.tokenType is not JT.KEYWORD:
            return "Error"
        ET.SubElement(whileStatement, token.keyWord())
        token.advance()
        ET.SubElement(whileStatement, token.symbol())
        token.advance()
        ET.SubElement(whileStatement, self.CompileExpression())
        token.advance()
        ET.SubElement(whileStatement, token.symbol())
        token.advance()
        ET.SubElement(whileStatement, token.symbol())
        token.advance()
        ET.SubElement(whileStatement, self.CompileStatements())
        token.advance()
        ET.SubElement(whileStatement, token.symbol())
        return whileStatement

    def CompileReturn(self):
        token = self._tokenizer
        returnStatement = ET.Element("returnStatement")
        if token.tokenType is not JT.KEYWORD:
            return "Error"
        ET.SubElement(returnStatement, token.keyWord())
        token.advance()
        if token.tokenType == JT.SYMBOL:
            if token.symbol() == ';':
                ET.SubElement(returnStatement, token.symbol())
                return returnStatement
        ET.SubElement(returnStatement, self.CompileExpression())
        return returnStatement

    def CompileIf(self):
        token = self._tokenizer
        ifStatement = ET.Element("ifStatement")
        if token.tokenType() is not JT.KEYWORD:
            return "Error"
        ET.SubElement(ifStatement, token.keyWord())
        token.advance()
        ET.SubElement(ifStatement, token.symbol())
        token.advance()
        ET.SubElement(ifStatement, self.CompileExpression())
        token.advance()
        ET.SubElement(ifStatement, token.symbol())
        token.advance()
        ET.SubElement(ifStatement, token.symbol())
        token.advance()
        ET.SubElement(ifStatement, self.CompileStatements())
        token.advance()
        ET.SubElement(ifStatement, token.symbol())
        token.advance()
        if token.tokenType == JT.KEYWORD:
            if token.keyWord() == 'else':
                ET.SubElement(ifStatement, token.keyWord())
                token.advance()
                ET.SubElement(ifStatement, token.symbol())
                token.advance()
                ET.SubElement(ifStatement, self.CompileStatements())
                token.advance()
                ET.SubElement(ifStatement, token.symbol())
        return ifStatement

    def CompileExpression(self):
        token = self._tokenizer
        expression = ET.Element("expression")
        ET.SubElement(expression, self.CompileTerm())
        token.advance()
        while token.tokenType() == JT.TERM or token.tokenType == JT.OP:
            if token.tokenType() == JT.OP:
                ET.SubElement(expression, token.op())
            elif token.tokenType() == JT.TERM:
                ET.SubElement(expression, self.CompileTerm())
            token.advance()
        return expression

    def CompileTerm(self):
        token = self._tokenizer
        term = ET.Element("term")
        if token.tokenType == JT.INT_CONST:
            ET.SubElement(term, token.intVal())
        elif token.tokenType == JT.STRING_CONST:
            ET.SubElement(term, token.stringVal())
        elif token.tokenType in JT.KEYWORD_CONSTS:
            ET.SubElement(term, token.keyWord())
        elif token.tokenType == JT.IDENTIFIER:
            ET.SubElement(term, token.identifier())
            token.advance()
            # varName
            if token.symbol() == '[':
                ET.SubElement(term, token.symbol())
                token.advance()
                ET.SubElement(term, self.CompileExpression())
                token.advance()
                ET.SubElement(term, token.symbol())
            # subroutinecall
            elif token.tokenType == JT.IDENTIFIER or \
                            token.tokenType == JT.SYMBOL:
                if token.tokenType is JT.SYMBOL:
                    ET.SubElement(term, token.symbol())
                    token.advance()
                    ET.SubElement(term, self.CompileExpressionList)
                    token.advance()
                    ET.SubElement(term, token.symbol())
                else:
                    ET.SubElement(term, token.identifier())
                    token.advance()
                    ET.SubElement(term, token.symbol())
                    token.advance()
                    ET.SubElement(term, token.identifier())
                    token.advance()
                    ET.SubElement(term, token.symbol())
                    token.advance()
                    ET.SubElement(term, self.CompileExpressionList())
                    token.advance()
                    ET.SubElement(term, token.symbol())
            elif token.tokenType == JT.UOP:
                ET.SubElement(term, token.symbol())
                token.advance()
                ET.SubElement(term, self.CompileTerm())
        return term

    def CompileExpressionList(self):
        token = self._tokenizer
        expressionList = ET.Element("expressionList")
        if token.symbol() is not ')':
            ET.SubElement(expressionList, self.CompileExpression())
            token.advance()
            while token.symbol() is not ')':
                ET.SubElement(expressionList, token.symbol())
                token.advance()
                ET.SubElement(expressionList, self.CompileExpression())
                token.advance()
        return expressionList
