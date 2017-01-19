import JackTokenizer as JT
import VMWriter as VMR
import SymbolTable as ST

TOKEN_IDX = 0
VALUE_IDX = 1

ARG = 'arg'
METHOD = 'method'
THIS = 'this'
SELF = 'self'
GLOBAL = 'global'
EMPTY = ''
VAR = 'var'
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
            self.CompileVarDec()

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
        vars = self.symbolTable.varCount(VAR)
        self.vmWriter.writeFunction(self.name,vars)
        self.LoadPointer(currType)
        self.CompileStatements()
        self.advance()
        self.symbolTable.setScope(GLOBAL)

    def LoadPointer(self, currType):
        if currType[VALUE_IDX] == METHOD:
            self.vmWriter.writePush('argument', 0)
            self.vmWriter.writePop('pointer', 0)
        elif currType[VALUE_IDX] == 'constructor':
            globalVars = self.symbolTable.globalsCount('field')
            self.vmWriter.writePush('constant', globalVars)
            self.vmWriter.writeCall('Memory.alloc', 1)
            self.vmWriter.writePop('pointer', 0)

    def CompileVarDec(self):
        currKind = self.tokenizer.advance()[VALUE_IDX]
        currType = self.tokenizer.advance()[VALUE_IDX]
        currName = self.tokenizer.advance()[VALUE_IDX]
        self.symbolTable.define(currName, currType, currKind)
        while self.nextValueIs(","):
            self.advance()
            currName = self.advance()[VALUE_IDX]
            self.symbolTable.define(currName, currType, currKind)
        self.advance()

    def CompileStatements(self):
        while self._isStatement():
            if self.nextValueIs("do"):     self.CompileDo()
            elif self.nextValueIs("let"):    self.CompileLet()
            elif self.nextValueIs("if"):     self.CompileIf()
            elif self.nextValueIs("while"):  self.CompileWhile()
            elif self.nextValueIs("return"): self.CompileReturn()

    def CompileDo(self):
        self.advance()
        self.CompileSubroutineCall()
        self.vmWriter.writePop('temp', 0)
        self.advance()

    def CompileSubroutineCall(self):
        first = EMPTY
        last = EMPTY
        full = EMPTY
        locals = 0
        first = self.advance()[VALUE_IDX]
        if self.nextValueIs("."):
            self.advance()
            last = self.advance()[VALUE_IDX]
            if first in self.symbolTable.currScope or first in self.symbolTable.globalScope:
                self.WritePush(first, last)
                full = self.symbolTable.typeOf(first) + '.' + last
                locals += 1
            else:
                full = first + '.' + last
        else:
            self.vmWriter.writePush('pointer', 0)
            locals += 1
            full = self.className + '.' + first
        self.advance()
        locals += self.CompileExpressionList()
        self.vmWriter.writeCall(full, locals)
        self.advance()

    def CompileExpressionList(self):
        counter = 0
        if self._isExpression():
            self.CompileExpression()
            counter += 1
        while self.nextValueIs(","):
            self.advance()
            self.CompileExpression()
            counter += 1
        return counter

    def CompileLet(self):
        self.advance()
        arrayFlag = False
        currName = self.advance()[1]
        if self.nextValueIs("["):
            arrayFlag = True
            self.CompileArray(currName)
        self.advance()
        self.CompileExpression()
        if arrayFlag:
            self.vmWriter.writePop("temp", 0)
            self.vmWriter.writePop("pointer", 1)
            self.vmWriter.writePush("temp", 0)
            self.vmWriter.writePop("that", 0)
        else:
            self.WritePop(currName)
        self.advance()


    def CompileArray(self, currName):
        self.advance()
        self.CompileExpression()
        self.advance()
        if currName in self.symbolTable.currScope:
            if self.symbolTable.kindOf(currName) == 'var':
                self.vmWriter.writePush('local', self.symbolTable.indexOf(currName))
            elif self.symbolTable.kindOf(currName) == 'arg':
                self.vmWriter.writePush('argument', self.symbolTable.indexOf(currName))
        else:
            if self.symbolTable.kindOf(currName) == 'static':
                self.vmWriter.writePush('static', self.symbolTable.indexOf(currName))
            elif self.symbolTable.kindOf(currName) == 'this':
                self.vmWriter.writePush('this', self.symbolTable.indexOf(currName))
        self.vmWriter.writeArithmetic('add')

    def CompileWhile(self):
        counter = str(self.symbolTable.whileCounter)
        self.symbolTable.whileCounter += 1
        self.vmWriter.writeLabel('WHILE_EXP' + counter)
        self.advance()
        self.advance()
        self.CompileExpression()
        self.vmWriter.writeArithmetic('not')
        self.vmWriter.writeIf('WHILE_END' + counter)
        self.advance()
        self.advance()
        self.CompileStatements()
        self.vmWriter.writeGoto('WHILE_EXP' + counter)
        self.vmWriter.writeLabel('WHILE_END' + counter)
        self.advance()

    def CompileReturn(self):
        self.advance()
        returnEmpty = True
        while self._isExpression():
            returnEmpty = False
            self.CompileExpression()
        if (returnEmpty):
            self.vmWriter.writePush('constant', 0)
        self.vmWriter.writeReturn()
        self.advance()

    def CompileIf(self):
        self.advance()
        self.advance()
        self.CompileExpression()
        self.advance()
        counter = self.symbolTable.ifCounter
        self.symbolTable.ifCounter += 1
        self.vmWriter.writeIf('IF_TRUE' + str(counter))
        self.vmWriter.writeGoto('IF_FALSE' + str(counter))
        self.vmWriter.writeLabel('IF_TRUE' + str(counter))
        self.advance()
        self.CompileStatements()
        self.advance()
        if self.nextValueIs("else"):
            self.vmWriter.writeGoto('IF_END' + str(counter))
            self.vmWriter.writeLabel('IF_FALSE' + str(counter))
            self.advance()
            self.advance()
            self.CompileStatements()
            self.advance()
            self.vmWriter.writeLabel('IF_END' + str(counter))
        else:
            self.vmWriter.writeLabel('IF_FALSE' + str(counter))

    def CompileExpression(self):
        self.CompileTerm()
        while self.nextValueIn(self.binaryOp):
            oper = self.advance()[VALUE_IDX]
            self.CompileTerm()
            if oper == '+':
                self.vmWriter.writeArithmetic('add')
            elif oper == '-':
                self.vmWriter.writeArithmetic('sub')
            elif oper == '*':
                self.vmWriter.writeCall('Math.multiply', 2)
            elif oper == '/':
                self.vmWriter.writeCall('Math.divide', 2)
            elif oper == '|':
                self.vmWriter.writeArithmetic('or')
            elif oper == '&':
                self.vmWriter.writeArithmetic('and')
            elif oper == '=':
                self.vmWriter.writeArithmetic('eq')
            elif oper == '<':
                self.vmWriter.writeArithmetic('lt')
            elif oper == '>':
                self.vmWriter.writeArithmetic('gt')

    def CompileTerm(self):
        array = False
        if self.nextTokenIs("integerConstant"):
            val = self.advance()[VALUE_IDX]
            self.vmWriter.writePush('constant', val)
        elif self.nextTokenIs("stringConstant"):
            val = self.advance()[VALUE_IDX]
            self.vmWriter.writePush('constant', len(val))
            self.vmWriter.writeCall('String.new', 1)
            for letter in val:
                self.vmWriter.writePush('constant', ord(letter))
                self.vmWriter.writeCall('String.appendChar', 2)
        elif self.nextValueIn(self.keywordConstant):
            val = self.advance()[1]  # get keywordConstant
            if val == "this":
                self.vmWriter.writePush('pointer', 0)
            else:
                self.vmWriter.writePush('constant', 0)
                if val == "true":
                    self.vmWriter.writeArithmetic('not')
        elif self.nextTokenIs("identifier"):
            locals = 0
            currName = self.advance()[VALUE_IDX]
            if self.nextValueIs("["):
                array = True
                self.CompileArray(currName)
            if self.nextValueIs("("):
                locals += 1
                self.vmWriter.writePush('pointer', 0)
                self.advance()
                locals += self.CompileExpressionList()
                self.advance()
                self.vmWriter.writeCall(self.className + '.' + currName, locals)
            elif self.nextValueIs("."):
                self.advance()
                last = self.advance()[VALUE_IDX]
                if currName in self.symbolTable.currScope or currName in self.symbolTable.globalScope:
                    self.WritePush(currName, last)
                    currName = self.symbolTable.typeOf(currName) + '.' + last
                    locals += 1
                else:
                    currName = currName + '.' + last
                self.advance()
                locals += self.CompileExpressionList()
                self.advance()
                self.vmWriter.writeCall(currName, locals)
            else:
                if array:
                    self.vmWriter.writePop('pointer', 1)
                    self.vmWriter.writePush('that', 0)
                elif currName in self.symbolTable.currScope:
                    if self.symbolTable.kindOf(currName) == 'var':
                        self.vmWriter.writePush('local', self.symbolTable.indexOf(currName))
                    elif self.symbolTable.kindOf(currName) == 'arg':
                        self.vmWriter.writePush('argument', self.symbolTable.indexOf(currName))
                else:
                    if self.symbolTable.kindOf(currName) == 'static':
                        self.vmWriter.writePush('static', self.symbolTable.indexOf(currName))
                    else:
                        self.vmWriter.writePush('this', self.symbolTable.indexOf(currName))
        elif self.nextValueIn(self.unaryOp):
            oper = self.advance()[VALUE_IDX]
            self.CompileTerm()
            if oper == '-':
                self.vmWriter.writeArithmetic('neg')
            elif oper == '~':
                self.vmWriter.writeArithmetic('not')
        elif self.nextValueIs("("):
            self.advance()
            self.CompileExpression()
            self.advance()

    def WritePush(self, currName, last):
        if currName in self.symbolTable.currScope:
            if self.symbolTable.kindOf(currName) == 'var':
                self.vmWriter.writePush('local', self.symbolTable.indexOf(currName))
            elif self.symbolTable.kindOf(currName) == 'arg':
                self.vmWriter.writePush('argument', self.symbolTable.indexOf(currName))
        else:
            if self.symbolTable.kindOf(currName) == 'static':
                self.vmWriter.writePush('static', self.symbolTable.indexOf(currName))
            else:
                self.vmWriter.writePush('this', self.symbolTable.indexOf(currName))

    def WritePop(self, currName):
        if currName in self.symbolTable.currScope:
            if self.symbolTable.kindOf(currName) == 'var':
                self.vmWriter.writePop('local', self.symbolTable.indexOf(currName))
            elif self.symbolTable.kindOf(currName) == 'arg':
                self.vmWriter.writePop('argument', self.symbolTable.indexOf(currName))
        else:
            if self.symbolTable.kindOf(currName) == 'static':
                self.vmWriter.writePop('static', self.symbolTable.indexOf(currName))
            else:
                self.vmWriter.writePop('this', self.symbolTable.indexOf(currName))