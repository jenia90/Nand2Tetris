import JackTokenizer as JT
import VMWriter as VMR
import SymbolTable as ST

TOKEN_IDX = 0
VALUE_IDX = 1

ARG = 'arg'
METHOD = 'method'
THIS = 'this'
SELF = 'self'
EMPTY = ''
IDENTIFIER = "identifier"
TERM = 'term'
EXPRESSION = 'expression'
IF_STATEMENT = 'ifStatement'
STATEMENTS = 'statements'
VAR_DEC = 'varDec'
VAL = "var"
SUBROUTINE_BODY = 'subroutineBody'
SYMBOL = "symbol"
PARAMETER_LIST = 'parameterList'
SUBROUTINE_DEC = 'subroutineDec'
CLASS_VAR_DEC = 'classVarDec'
STATIC = "static"
CLASS = 'class'
RETURN_STATEMENT = 'returnStatement'
WHILE_STATEMENT = 'whileStatement'
LET_STATEMENT = 'letStatement'
EXPRESSION_LIST = 'expressionList'
DO_STATEMENT = 'doStatement'


class CompilationEngine:
    def __init__(self, in_f, out_f):
        self.tokenizer = JT.JackTokenizer(in_f)
        self.vmWriter = VMR.VMWriter(out_f)
        self.symbolTable = ST.SymbolTable()
        self.className = EMPTY
        self.name = EMPTY

    def _isParam(self):
        return not self.nextTokenIs(SYMBOL)

    def _isClassVarDec(self):
        return self.nextValueIn(JT.CLASS_VARS)

    def _isSubroutine(self):
        return self.nextValueIn(JT.SUBROUTINE_TYPES)

    def _isStatement(self):
        return self.nextValueIs("do") or\
               self.nextValueIs("let") or\
               self.nextValueIs("if") or\
               self.nextValueIs("while") or\
               self.nextValueIs("return")

    def _isExpression(self):
        return self._isTerm()

    def _isTerm(self):
        return self.nextTokenIs(JT.INTEGER_CONSTANT) or \
               self.nextTokenIs(JT.STRING_CONSTANT) or\
               self.nextTokenIs(JT.IDENTIFIER) or\
               self.nextValueIn(JT.UOP_LIST) or\
               self.nextValueIn(JT.KWD_CONSTS) or\
               self.nextValueIs('(')

    def _isVarDec(self):
        return self.nextValueIs(VAL)

    def advance(self):
        return self.tokenizer.advance()

    def nextValueIn(self, list):
        return self.tokenizer.peek()[VALUE_IDX] in list

    def nextValueIs(self, val):
        return self.tokenizer.peek()[VALUE_IDX] == val

    def nextTokenIs(self, tok):
        return self.tokenizer.peek()[TOKEN_IDX] == tok

    def WriteClassVarDec(self):
        self.advance()
        currKind = self.tokenizer.advance()[VALUE_IDX]
        self.advance()
        currType = self.tokenizer.advance()[VALUE_IDX]
        self.advance()
        currName = self.tokenizer.advance()[VALUE_IDX]
        self.symbolTable.define(currName, currType, currKind)
        while self.nextValueIs(","):
            self.advance()
            currName = self.advance()[VALUE_IDX]
            self.symbolTable.define(currName, currType, currKind)
        self.advance()

    def writeParameter(self):
        currType = self.advance()[VALUE_IDX]
        currName = self.advance()[VALUE_IDX]
        self.symbolTable.define(currName, currType, ARG)
        if self.nextValueIs(","):
            self.advance()

    def CompileClass(self):
        self.advance()
        self.className = self.advance()[VALUE_IDX]
        self.advance()
        if self._isClassVarDec():
            self.CompileClassVarDec()
        while self._isSubroutine():
            self.CompileSubroutine()
        self.advance()
        self.vmWriter.close()

    def CompileClassVarDec(self):
        while self._isClassVarDec():
            self.WriteClassVarDec()

    def CompileSubroutine(self):
        """
        compiles a complete method, function,
        or constructor.
        """
        currType = self.advance()
        self.advance()
        self.name = self.className + '.' + self.advance()[VALUE_IDX]
        self.symbolTable.startSubroutine(self.name)
        self.symbolTable.setScope(self.name)
        self.advance()
        self.CompileParameterList(currType)
        self.advance()
        self.CompileSubroutineBody(currType)

    def CompileParameterList(self, currType):
        if currType[1] == METHOD:
            self.symbolTable.define(THIS, SELF, ARG)
        while self._isParam():
            self.writeParameter()

    def CompileSubroutineBody(self, currType):
        self.advance()
        while self._isVarDec():
            self.CompileVarDec()
        vars = self.symbolTable.varCount('var')

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
        while self.nextValueIs(","):
            self.advance()
            self.advance()
        self.advance()
        self._writeNonTerminalEnd()

    def CompileStatements(self):
        self._writeNonTerminalStart(STATEMENTS)
        while self._isStatement():
            if self.nextValueIs("do"):
                self.CompileDo()
            elif self.nextValueIs("let"):
                self.CompileLet()
            elif self.nextValueIs("if"):
                self.CompileIf()
            elif self.nextValueIs("while"):
                self.CompileWhile()
            elif self.nextValueIs("return"):
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
        if self.nextValueIs("."):
            self.advance()
            self.advance()
        self.advance()
        self.CompileExpressionList()
        self.advance()

    def CompileExpressionList(self):
        self._writeNonTerminalStart(EXPRESSION_LIST)
        if self._isExpression():
            self.CompileExpression()
        while self.nextValueIs(","):
            self.advance()
            self.CompileExpression()
        self._writeNonTerminalEnd()

    def CompileLet(self):
        self._writeNonTerminalStart(LET_STATEMENT)
        self.advance()
        self.advance()

        if self.nextValueIs("["):
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
        if self.nextValueIs("else"):
            self.advance()
            self.advance()
            self.CompileStatements()
            self.advance()
        self._writeNonTerminalEnd()

    def CompileExpression(self):
        self._writeNonTerminalStart(EXPRESSION)
        self.CompileTerm()
        while self.nextValueIn(JT.OP_LIST):
            self.advance()
            self.CompileTerm()
        self._writeNonTerminalEnd()

    def CompileTerm(self):
        self._writeNonTerminalStart(TERM)
        if self.nextTokenIs(JT.INTEGER_CONSTANT) or \
                self.nextTokenIs(JT.STRING_CONSTANT) or\
                self.nextValueIn(JT.KWD_CONSTS):
            self.advance()
        elif self.nextTokenIs(IDENTIFIER):
            self.advance()
            if self.nextValueIs("["):
                self.advance()
                self.CompileExpression()
                self.advance()
            if self.nextValueIs("("):
                self.advance()
                self.CompileExpressionList()
                self.advance()
            if self.nextValueIs("."):
                self.advance()
                self.advance()
                self.advance()
                self.CompileExpressionList()
                self.advance()
        elif self.nextValueIn(JT.UOP_LIST):
            self.advance()
            self.CompileTerm()
        elif self.nextValueIs("("):
            self.advance()
            self.CompileExpression()
            self.advance()
        self._writeNonTerminalEnd()
