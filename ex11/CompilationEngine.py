import JackTokenizer as JT
import SymbolTable as ST

TOKEN_IDX = 0
VALUE_IDX = 1

ARG = 'arg'
METHOD = 'method'
THIS = 'this'
SELF = 'self'
LCL = 'local'
POINTER = 'pointer'
C_TOR = 'constructor'
MALLOC = 'Memory.alloc'
CONST = 'constant'
FIELD = 'field'
STATIC = 'static'
TEMP = 'temp'
THAT = "that"
ARGUMENT = 'argument'

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
    def __init__(self, in_f, vmw):
        self.tokenizer = JT.JackTokenizer(in_f)
        self.vw = vmw
        self.symbolTable = ST.SymbolTable()
        self.className = ''
        self.name = ''

    def _isParam(self):
        return not self.nextTokenIs(SYMBOL)

    def _isClassVarDec(self):
        return self.nextValueIn(JT.CLASS_VARS)

    def _isSubroutine(self):
        return self.nextValueIn(JT.SUBROUTINE_TYPES)

    def _isStatement(self):
        return self.nextValueIs(DO) or\
               self.nextValueIs(LET) or\
               self.nextValueIs(IF) or\
               self.nextValueIs(WHILE) or\
               self.nextValueIs(RET)

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
        return self.nextValueIs(VAR)

    def advance(self):
        return self.tokenizer.advance()

    def nextValueIn(self, list):
        return self.tokenizer.peek()[VALUE_IDX] in list

    def nextValueIs(self, val):
        return self.tokenizer.peek()[VALUE_IDX] == val

    def nextTokenIs(self, tok):
        return self.tokenizer.peek()[TOKEN_IDX] == tok

    def writeParameter(self):
        currType = self.advance()[VALUE_IDX]
        currName = self.advance()[VALUE_IDX]
        self.symbolTable.define(currName, currType, ARG)
        if self.nextValueIs(','):
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

    def CompileClassVarDec(self):
        while self._isClassVarDec():
            self.CompileVarDec()

    def CompileSubroutine(self):
        """
        compiles a complete method, function,
        or constructor.
        """
        currType = self.advance()
        self.advance()
        self.name = self.className + '.' + self.advance()[VALUE_IDX]
        self.symbolTable.startSubroutine()
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
        nArgs = self.symbolTable.varCount(VAR)
        self.vw.writeFunction(self.name, nArgs)
        self.LoadPointer(currType)
        self.CompileStatements()
        self.advance()

    def LoadPointer(self, currType):
        if currType[VALUE_IDX] == METHOD:
            self.vw.writePush(ARG, 0)
            self.vw.writePop(POINTER, 0)
        elif currType[VALUE_IDX] == C_TOR:
            nArgs = self.symbolTable.varCount(FIELD)
            self.vw.writePush(CONST, nArgs)
            self.vw.writeCall(MALLOC, 1)
            self.vw.writePop(POINTER, 0)

    def CompileVarDec(self):
        currKind = self.tokenizer.advance()[VALUE_IDX]
        currType = self.tokenizer.advance()[VALUE_IDX]
        currName = self.tokenizer.advance()[VALUE_IDX]
        self.symbolTable.define(currName, currType, currKind)
        while self.nextValueIs(','):
            self.advance()
            currName = self.advance()[VALUE_IDX]
            self.symbolTable.define(currName, currType, currKind)
        self.advance()

    def CompileStatements(self):
        while self._isStatement():
            if self.nextValueIs(DO):
                self.CompileDo()
            elif self.nextValueIs(LET):
                self.CompileLet()
            elif self.nextValueIs(IF):
                self.CompileIf()
            elif self.nextValueIs(WHILE):
                self.CompileWhile()
            elif self.nextValueIs(RET):
                self.CompileReturn()

    def CompileDo(self):
        self.advance()
        self.CompileSubroutineCall()
        self.vw.writePop(TEMP, 0)
        self.advance()

    def CompileSubroutineCall(self):
        lcls = 0
        start = self.advance()[VALUE_IDX]
        if self.nextValueIs('.'):
            self.advance()
            end = self.advance()[VALUE_IDX]
            if self.symbolTable.contains(start):
                self.WritePush(start, end)
                full = self.symbolTable.typeOf(start) + '.' + end
                lcls += 1
            else:
                full = start + '.' + end
        else:
            self.vw.writePush(POINTER, 0)
            lcls += 1
            full = self.className + '.' + start
        self.advance()
        lcls += self.CompileExpressionList()
        self.vw.writeCall(full, lcls)
        self.advance()

    def CompileExpressionList(self):
        counter = 0
        if self._isExpression():
            self.CompileExpression()
            counter += 1
        while self.nextValueIs(','):
            self.advance()
            self.CompileExpression()
            counter += 1
        return counter

    def CompileLet(self):
        self.advance()
        arrayFlag = False
        currName = self.advance()[1]
        if self.nextValueIs('['):
            arrayFlag = True
            self.CompileArray(currName)
        self.advance()
        self.CompileExpression()
        if arrayFlag:
            self.vw.writePop(TEMP, 0)
            self.vw.writePop(POINTER, 1)
            self.vw.writePush(TEMP, 0)
            self.vw.writePop(THAT, 0)
        else:
            self.WritePop(currName)
        self.advance()

    def CompileArray(self, name):
        self.advance()
        self.CompileExpression()
        self.advance()
        if self.symbolTable.contains(name):
            if self.symbolTable.kindOf(name) == VAR:
                self.vw.writePush(LCL, self.symbolTable.indexOf(name))
            elif self.symbolTable.kindOf(name) == ARG:
                self.vw.writePush(ARGUMENT, self.symbolTable.indexOf(name))
        else:
            if self.symbolTable.kindOf(name) == STATIC:
                self.vw.writePush(STATIC, self.symbolTable.indexOf(name))
            elif self.symbolTable.kindOf(name) == THIS:
                self.vw.writePush(THIS, self.symbolTable.indexOf(name))
        self.vw.writeArithmetic('add')

    def CompileWhile(self):
        while_count = str(self.symbolTable.countUpdate(WHILE))
        self.symbolTable.countUpdate(WHILE, 1)
        self.vw.writeLabel('WHILE_EXP' + while_count)
        self.advance()
        self.advance()
        self.CompileExpression()
        self.vw.writeArithmetic('not')
        self.vw.writeIf('WHILE_END' + while_count)
        self.advance()
        self.advance()
        self.CompileStatements()
        self.vw.writeGoto('WHILE_EXP' + while_count)
        self.vw.writeLabel('WHILE_END' + while_count)
        self.advance()

    def CompileReturn(self):
        self.advance()
        returnEmpty = True
        while self._isExpression():
            returnEmpty = False
            self.CompileExpression()
        if (returnEmpty):
            self.vw.writePush(CONST, 0)
        self.vw.writeReturn()
        self.advance()

    def CompileIf(self):
        self.advance()
        self.advance()
        self.CompileExpression()
        self.advance()
        if_count = self.symbolTable.countUpdate('if')
        self.symbolTable.countUpdate('if', 1)
        self.vw.writeIf('IF_TRUE' + str(if_count))
        self.vw.writeGoto('IF_FALSE' + str(if_count))
        self.vw.writeLabel('IF_TRUE' + str(if_count))
        self.advance()
        self.CompileStatements()
        self.advance()
        if self.nextValueIs(ELSE):
            self.vw.writeGoto('IF_END' + str(if_count))
            self.vw.writeLabel('IF_FALSE' + str(if_count))
            self.advance()
            self.advance()
            self.CompileStatements()
            self.advance()
            self.vw.writeLabel('IF_END' + str(if_count))
        else:
            self.vw.writeLabel('IF_FALSE' + str(if_count))

    def CompileExpression(self):
        self.CompileTerm()
        while self.nextValueIn(JT.OP_LIST):
            op = self.advance()[VALUE_IDX]
            self.CompileTerm()
            if op == '+':
                self.vw.writeArithmetic('add')
            elif op == '-':
                self.vw.writeArithmetic('sub')
            elif op == '*':
                self.vw.writeCall('Math.multiply', 2)
            elif op == '/':
                self.vw.writeCall('Math.divide', 2)
            elif op == '|':
                self.vw.writeArithmetic('or')
            elif op == '&':
                self.vw.writeArithmetic('and')
            elif op == '=':
                self.vw.writeArithmetic('eq')
            elif op == '<':
                self.vw.writeArithmetic('lt')
            elif op == '>':
                self.vw.writeArithmetic('gt')

    def CompileTerm(self):
        array = False
        if self.nextTokenIs(JT.INTEGER_CONSTANT):
            val = self.advance()[VALUE_IDX]
            self.vw.writePush(CONST, val)
        elif self.nextTokenIs(JT.STRING_CONSTANT):
            val = self.advance()[VALUE_IDX]
            self.vw.writePush(CONST, len(val))
            self.vw.writeCall('String.new', 1)
            for letter in val:
                self.vw.writePush(CONST, ord(letter))
                self.vw.writeCall('String.appendChar', 2)
        elif self.nextValueIn(JT.KEYWORD_CONSTS):
            val = self.advance()[1]  # get keywordConstant
            if val == THIS:
                self.vw.writePush(POINTER, 0)
            else:
                self.vw.writePush(CONST, 0)
                if val == "true":
                    self.vw.writeArithmetic('not')
        elif self.nextTokenIs(JT.IDENTIFIER):
            locals = 0
            name = self.advance()[VALUE_IDX]
            if self.nextValueIs("["):
                array = True
                self.CompileArray(name)
            if self.nextValueIs("("):
                locals += 1
                self.vw.writePush(POINTER, 0)
                self.advance()
                locals += self.CompileExpressionList()
                self.advance()
                self.vw.writeCall(self.className + '.' + name, locals)
            elif self.nextValueIs("."):
                self.advance()
                last = self.advance()[VALUE_IDX]
                if self.symbolTable.contains(name):
                    self.WritePush(name, last)
                    name = self.symbolTable.typeOf(name) + '.' + last
                    locals += 1
                else:
                    name = name + '.' + last
                self.advance()
                locals += self.CompileExpressionList()
                self.advance()
                self.vw.writeCall(name, locals)
            else:
                if array:
                    self.vw.writePop(POINTER, 1)
                    self.vw.writePush(THAT, 0)
                elif self.symbolTable.contains(name):
                    if self.symbolTable.kindOf(name) == VAR:
                        self.vw.writePush(LCL, self.symbolTable.indexOf(name))
                    elif self.symbolTable.kindOf(name) == ARG:
                        self.vw.writePush(ARGUMENT, self.symbolTable.indexOf(name))
                else:
                    if self.symbolTable.kindOf(name) == STATIC:
                        self.vw.writePush(STATIC, self.symbolTable.indexOf(name))
                    else:
                        self.vw.writePush(THIS, self.symbolTable.indexOf(name))
        elif self.nextValueIn(JT.UOP_LIST):
            oper = self.advance()[VALUE_IDX]
            self.CompileTerm()
            if oper == '-':
                self.vw.writeArithmetic('neg')
            elif oper == '~':
                self.vw.writeArithmetic('not')
        elif self.nextValueIs("("):
            self.advance()
            self.CompileExpression()
            self.advance()

    def WritePush(self, currName, last):
        if self.symbolTable.contains(currName):
            if self.symbolTable.kindOf(currName) == VAR:
                self.vw.writePush(LCL, self.symbolTable.indexOf(currName))
            elif self.symbolTable.kindOf(currName) == ARG:
                self.vw.writePush(ARGUMENT, self.symbolTable.indexOf(currName))
        else:
            if self.symbolTable.kindOf(currName) == STATIC:
                self.vw.writePush(STATIC, self.symbolTable.indexOf(currName))
            else:
                self.vw.writePush(THIS, self.symbolTable.indexOf(currName))

    def WritePop(self, currName):
        if self.symbolTable.contains(currName):
            if self.symbolTable.kindOf(currName) == VAR:
                self.vw.writePop(LCL, self.symbolTable.indexOf(currName))
            elif self.symbolTable.kindOf(currName) == ARG:
                self.vw.writePop(ARGUMENT, self.symbolTable.indexOf(currName))
        else:
            if self.symbolTable.kindOf(currName) == STATIC:
                self.vw.writePop(STATIC, self.symbolTable.indexOf(currName))
            else:
                self.vw.writePop(THIS, self.symbolTable.indexOf(currName))