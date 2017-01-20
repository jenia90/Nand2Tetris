import JackTokenizer as JT


TOKEN_IDX = 0
VALUE_IDX = 1
INDENT_LEN = 2

IDENTIFIER = "identifier"
TERM = 'term'
EXPRESSION = 'expression'
IF_STATEMENT = 'ifStatement'
STATEMENTS = 'statements'
VAR_DEC = 'varDec'
VAR = "var"
SUBROUTINE_BODY = 'subroutineBody'
SYMBOL = "symbol"
PARAMETER_LIST = 'parameterList'
SUBROUTINE_DEC = 'subroutineDec'
CLASS_VAR_DEC = 'classVarDec'
STATIC = "static"
CLASS = 'class'
ELSE = "else"
RET = "return"
WHILE = "while"
IF = "if"
LET = "let"
DO = "do"
RETURN_STATEMENT = 'returnStatement'
WHILE_STATEMENT = 'whileStatement'
LET_STATEMENT = 'letStatement'
EXPRESSION_LIST = 'expressionList'
DO_STATEMENT = 'doStatement'


class CompilationEngine:
    def __init__(self, in_f, out_f):
        self.tokenizer = JT.JackTokenizer(in_f)
        self.elementStack = []
        self._outFile = out_f
        self._indent = ""

    def _addIndent(self):
        self._indent += " " * INDENT_LEN

    def _removeIndent(self):
        self._indent = self._indent[:-INDENT_LEN]

    def _writeNonTerminalStart(self, element):
        self._outFile.write(self._indent + "<" + element + ">\n")
        self.elementStack.append(element)
        self._addIndent()

    def _writeNonTerminalEnd(self):
        self._removeIndent()
        element = self.elementStack.pop()
        self._outFile.write(self._indent + "</" + element + ">\n")

    def _writeTerminal(self, token, value):
        self._outFile.write(self._indent + "<" + token + "> " +
                            value + " </" + token + ">\n")

    def _writeClassVarDec(self):
        self.advance()
        self.advance()
        self.advance()
        while self._nextValueIs(","):
            self.advance()
            self.advance()
        self.advance()

    def _writeParam(self):
        self.advance()
        self.advance()
        if self._nextValueIs(","):
            self.advance()

    def _isParam(self):
        return not self._nextTokenIs(SYMBOL)

    def _isClassVarDec(self):
        return self._nextValueIn(JT.CLASS_VARS)

    def _isSubroutine(self):
        return self._nextValueIn(JT.SUBROUTINE_TYPES)

    def _isStatement(self):
        return self._nextValueIs(DO) or \
               self._nextValueIs(LET) or \
               self._nextValueIs(IF) or \
               self._nextValueIs(WHILE) or \
               self._nextValueIs(RET)

    def _isExpression(self):
        return self._isTerm()

    def _isTerm(self):
        return self._nextTokenIs(JT.INTEGER_CONSTANT) or \
               self._nextTokenIs(JT.STRING_CONSTANT) or \
               self._nextTokenIs(JT.IDENTIFIER) or \
               self._nextValueIn(JT.UOP_LIST) or \
               self._nextValueIn(JT.KWD_CONSTS) or \
               self._nextValueIs('(')

    def _isVarDec(self):
        return self._nextValueIs(VAR)

    def advance(self):
        token, value = self.tokenizer.advance()
        self._writeTerminal(token, value)

    def _nextValueIn(self, elementList):
        return self.tokenizer.peek()[VALUE_IDX] in elementList

    def _nextValueIs(self, value):
        return self.tokenizer.peek()[VALUE_IDX] == value

    def _nextTokenIs(self, token):
        return self.tokenizer.peek()[TOKEN_IDX] == token

    def CompileClass(self):
        self._writeNonTerminalStart(CLASS)
        self.advance()
        self.advance()
        self.advance()
        if self._isClassVarDec():
            self.CompileClassVarDec()
        while self._isSubroutine():
            self.CompileSubroutine()
        self.advance()
        self._writeNonTerminalEnd()
        self._outFile.close()

    def CompileClassVarDec(self):
        while self._isClassVarDec():
            self._writeNonTerminalStart(CLASS_VAR_DEC)
            self._writeClassVarDec()
            self._writeNonTerminalEnd()

    def CompileSubroutine(self):
        """
        compiles a complete method, function,
        or constructor.
        """
        self._writeNonTerminalStart(SUBROUTINE_DEC)
        self.advance()
        self.advance()
        self.advance()
        self.advance()
        self.CompileParameterList()
        self.advance()
        self.CompileSubroutineBody()
        self._writeNonTerminalEnd()

    def CompileParameterList(self):
        self._writeNonTerminalStart(PARAMETER_LIST)
        while self._isParam():
            self._writeParam()
        self._writeNonTerminalEnd()

    def CompileSubroutineBody(self):
        self._writeNonTerminalStart(SUBROUTINE_BODY)
        self.advance()

        while self._isVarDec():
            self.CompileVarDec()

        self.CompileStatements()
        self.advance()
        self._writeNonTerminalEnd()

    def CompileVarDec(self):
        self._writeNonTerminalStart(VAR_DEC)
        self.advance()
        self.advance()
        self.advance()
        while self._nextValueIs(","):
            self.advance()
            self.advance()
        self.advance()
        self._writeNonTerminalEnd()

    def CompileStatements(self):
        self._writeNonTerminalStart(STATEMENTS)
        while self._isStatement():
            if self._nextValueIs(DO):
                self.CompileDo()
            elif self._nextValueIs(LET):
                self.CompileLet()
            elif self._nextValueIs(IF):
                self.CompileIf()
            elif self._nextValueIs(WHILE):
                self.CompileWhile()
            elif self._nextValueIs(RET):
                self.CompileReturn()
        self._writeNonTerminalEnd()

    def CompileDo(self):
        self._writeNonTerminalStart(DO_STATEMENT)
        self.advance()
        self.CompileSubroutineCall()
        self.advance()
        self._writeNonTerminalEnd()

    def CompileSubroutineCall(self):
        self.advance()
        if self._nextValueIs("."):
            self.advance()
            self.advance()
        self.advance()
        self.CompileExpressionList()
        self.advance()

    def CompileExpressionList(self):
        self._writeNonTerminalStart(EXPRESSION_LIST)
        if self._isExpression():
            self.CompileExpression()
        while self._nextValueIs(","):
            self.advance()
            self.CompileExpression()
        self._writeNonTerminalEnd()

    def CompileLet(self):
        self._writeNonTerminalStart(LET_STATEMENT)
        self.advance()
        self.advance()

        if self._nextValueIs("["):
            self.advance()
            self.CompileExpression()
            self.advance()

        self.advance()
        self.CompileExpression()
        self.advance()
        self._writeNonTerminalEnd()

    def CompileWhile(self):
        self._writeNonTerminalStart(WHILE_STATEMENT)
        self.advance()
        self.advance()
        self.CompileExpression()
        self.advance()
        self.advance()
        self.CompileStatements()
        self.advance()
        self._writeNonTerminalEnd()

    def CompileReturn(self):
        self._writeNonTerminalStart(RETURN_STATEMENT)
        self.advance()
        while self._isExpression():
            self.CompileExpression()
        self.advance()
        self._writeNonTerminalEnd()

    def CompileIf(self):
        self._writeNonTerminalStart(IF_STATEMENT)
        self.advance()
        self.advance()
        self.CompileExpression()
        self.advance()
        self.advance()
        self.CompileStatements()
        self.advance()
        if self._nextValueIs(ELSE):
            self.advance()
            self.advance()
            self.CompileStatements()
            self.advance()
        self._writeNonTerminalEnd()

    def CompileExpression(self):
        self._writeNonTerminalStart(EXPRESSION)
        self.CompileTerm()
        while self._nextValueIn(JT.OP_LIST):
            self.advance()
            self.CompileTerm()
        self._writeNonTerminalEnd()

    def CompileTerm(self):
        self._writeNonTerminalStart(TERM)
        if self._nextTokenIs(JT.INTEGER_CONSTANT) or \
                self._nextTokenIs(JT.STRING_CONSTANT) or\
                self._nextValueIn(JT.KWD_CONSTS):
            self.advance()
        elif self._nextTokenIs(IDENTIFIER):
            self.advance()
            if self._nextValueIs("["):
                self.advance()
                self.CompileExpression()
                self.advance()
            if self._nextValueIs("("):
                self.advance()
                self.CompileExpressionList()
                self.advance()
            if self._nextValueIs("."):
                self.advance()
                self.advance()
                self.advance()
                self.CompileExpressionList()
                self.advance()
        elif self._nextValueIn(JT.UOP_LIST):
            self.advance()
            self.CompileTerm()
        elif self._nextValueIs("("):
            self.advance()
            self.CompileExpression()
            self.advance()
        self._writeNonTerminalEnd()
