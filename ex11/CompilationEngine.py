from old import JackTokenizer as JT

import SymbolTable as ST

TOKEN_IDX = 0
VALUE_IDX = 1

SYMBOL = "symbol"
CLASS = 'class'
ELSE = "else"
RET = "return"
WHILE = "while"
IF = "if"
LET = "let"
DO = "do"


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
        return self.nextValueIs('var')

    def advance(self):
        return self.tokenizer.advance()

    def nextValueIn(self, elementList):
        return self.tokenizer.peek()[VALUE_IDX] in elementList

    def nextValueIs(self, value):
        return self.tokenizer.peek()[VALUE_IDX] == value

    def nextTokenIs(self, token):
        return self.tokenizer.peek()[TOKEN_IDX] == token

    def writeParams(self):
        paramType = self.advance()[VALUE_IDX]
        paramName = self.advance()[VALUE_IDX]
        self.symbolTable.define(paramName, paramType, 'arg')
        if self.nextValueIs(','):
            self.advance()

    def CompileClass(self):
        self.advance()  # get 'class' keyword
        self.className = self.advance()[1]  # get class name
        self.advance()  # get '{' symbol
        if self._isClassVarDec():
            self.CompileClassVarDec()
        while self._isSubroutine():
            self.CompileSubroutine()
        self.advance()  # get '}' symbol

    def CompileClassVarDec(self):
        while self._isClassVarDec():
            self.CompileVarDec()

    def CompileSubroutine(self):
        """
        compiles a complete method, function,
        or constructor.
        """
        subRoutType = self.advance()[VALUE_IDX]
        self.advance()
        self.name = self.className + '.' + self.advance()[VALUE_IDX]
        self.symbolTable.startSubroutine(self.name)
        self.symbolTable.setScope(self.name)
        self.advance()
        self.CompileParameterList(subRoutType)
        self.advance()
        self.CompileSubroutineBody(subRoutType)

    def CompileParameterList(self, paramType):
        if paramType == 'method':
            self.symbolTable.define('this', 'self', 'arg')
        while self._isParam():
            self.writeParams()

    def CompileSubroutineBody(self, subRoutineType):
        self.advance()
        while self._isVarDec():
            self.CompileVarDec()
        nArgs = self.symbolTable.varCount('var')
        self.vw.writeFunction(self.name, nArgs)
        self.LoadPointer(subRoutineType)
        self.CompileStatements()
        self.advance()
        self.symbolTable.setScope(ST.GLOBAL_SCOPE)

    def LoadPointer(self, pointerType):
        if pointerType == 'method':
            self.vw.writePush('argument', 0)
            self.vw.writePop('pointer', 0)
        elif pointerType == 'constructor':
            nArgs = self.symbolTable.varCount('field')
            self.vw.writePush('constant', nArgs)
            self.vw.writeCall('Memory.alloc', 1)
            self.vw.writePop('pointer', 0)

    def CompileVarDec(self):
        varKind = self.tokenizer.advance()[VALUE_IDX]
        varType = self.tokenizer.advance()[VALUE_IDX]
        varName = self.tokenizer.advance()[VALUE_IDX]
        self.symbolTable.define(varName, varType, varKind)
        while self.nextValueIs(','):
            self.advance()
            varName = self.advance()[VALUE_IDX]
            self.symbolTable.define(varName, varType, varKind)
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
        self.vw.writePop('temp', 0)
        self.advance()

    def CompileSubroutineCall(self):
        nArgs = 0
        instName = self.advance()[VALUE_IDX]
        if self.nextValueIs('.'):
            self.advance()
            subName = self.advance()[VALUE_IDX]
            if instName in self.symbolTable.currentScopeSymbols or \
                            instName in self.symbolTable.classSymbols:
                self.writePush(instName, subName)
                full = self.symbolTable.typeOf(instName) + '.' + subName
                nArgs += 1
            else:
                full = instName + '.' + subName
        else:
            self.vw.writePush('pointer', 0)
            nArgs += 1
            full = self.className + '.' + instName
        self.advance()
        nArgs += self.CompileExpressionList()
        self.vw.writeCall(full, nArgs)
        self.advance()

    def CompileExpressionList(self):
        count = 0
        if self._isExpression():
            self.CompileExpression()
            count += 1
        while self.nextValueIs(','):
            self.advance()
            self.CompileExpression()
            count += 1
        return count

    def CompileLet(self):
        self.advance()
        arrayFlag = False
        varName = self.advance()[1]
        if self.nextValueIs('['):
            arrayFlag = True
            self.CompileArray(varName)
        self.advance()
        self.CompileExpression()
        if arrayFlag:
            self.vw.writePop('temp', 0)
            self.vw.writePop('pointer', 1)
            self.vw.writePush('temp', 0)
            self.vw.writePop('that', 0)
        else:
            self.writePop(varName)
        self.advance()

    def CompileArray(self, name):
        self.advance()
        self.CompileExpression()
        self.advance()
        if name in self.symbolTable.currentScopeSymbols:
            if self.symbolTable.kindOf(name) == 'var':
                self.vw.writePush('local', self.symbolTable.indexOf(name))
            elif self.symbolTable.kindOf(name) == 'arg':
                self.vw.writePush('argument', self.symbolTable.indexOf(name))
        else:
            if self.symbolTable.kindOf(name) == 'static':
                self.vw.writePush('static', self.symbolTable.indexOf(name))
            else:
                self.vw.writePush('this', self.symbolTable.indexOf(name))
        self.vw.writeArithmetic('add')

    def CompileWhile(self):
        while_count = str(self.symbolTable.countUpdate('while', 0))
        self.symbolTable.countUpdate('while', 1)
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
        noRet = True
        while self._isExpression():
            noRet = False
            self.CompileExpression()
        if noRet:
            self.vw.writePush('constant', 0)
        self.vw.writeReturn()
        self.advance()

    def CompileIf(self):
        self.advance()
        self.advance()
        self.CompileExpression()
        self.advance()
        if_count = str(self.symbolTable.countUpdate('if', 0))
        self.symbolTable.countUpdate('if', 1)
        self.vw.writeIf('IF_TRUE' + if_count)
        self.vw.writeGoto('IF_FALSE' + if_count)
        self.vw.writeLabel('IF_TRUE' + if_count)
        self.advance()
        self.CompileStatements()
        self.advance()
        if self.nextValueIs(ELSE):
            self.vw.writeGoto('IF_END' + if_count)
            self.vw.writeLabel('IF_FALSE' + if_count)
            self.advance()
            self.advance()
            self.CompileStatements()
            self.advance()
            self.vw.writeLabel('IF_END' + if_count)
        else:
            self.vw.writeLabel('IF_FALSE' + if_count)

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
            self.vw.writePush('constant', val)
        elif self.nextTokenIs(JT.STRING_CONSTANT):
            val = self.advance()[VALUE_IDX]
            self.vw.writePush('constant', len(val))
            self.vw.writeCall('String.new', 1)
            for letter in val:
                self.vw.writePush('constant', ord(letter))
                self.vw.writeCall('String.appendChar', 2)
        elif self.nextValueIn(JT.KEYWORD_CONSTS):
            val = self.advance()[1]  # get keywordConstant
            if val == 'this':
                self.vw.writePush('pointer', 0)
            else:
                self.vw.writePush('constant', 0)
                if val == "true":
                    self.vw.writeArithmetic('not')
        elif self.nextTokenIs(JT.IDENTIFIER):
            nArgs = 0
            name = self.advance()[VALUE_IDX]
            if self.nextValueIs("["):
                array = True
                self.CompileArray(name)
            if self.nextValueIs("("):
                nArgs += 1
                self.vw.writePush('pointer', 0)
                self.advance()
                nArgs += self.CompileExpressionList()
                self.advance()
                self.vw.writeCall(self.className + '.' + name, nArgs)
            elif self.nextValueIs("."):
                self.advance()
                last = self.advance()[VALUE_IDX]
                if name in self.symbolTable.currentScopeSymbols or name in \
                        self.symbolTable.classSymbols:
                    self.writePush(name, last)
                    name = self.symbolTable.typeOf(name) + '.' + last
                    nArgs += 1
                else:
                    name = name + '.' + last
                self.advance()
                nArgs += self.CompileExpressionList()
                self.advance()
                self.vw.writeCall(name, nArgs)
            else:
                if array:
                    self.vw.writePop('pointer', 1)
                    self.vw.writePush('that', 0)
                elif name in self.symbolTable.currentScopeSymbols:
                    if self.symbolTable.kindOf(name) == 'var':
                        self.vw.writePush('local', self.symbolTable.indexOf(name))
                    elif self.symbolTable.kindOf(name) == 'arg':
                        self.vw.writePush('argument', self.symbolTable.indexOf(name))
                else:
                    if self.symbolTable.kindOf(name) == 'static':
                        self.vw.writePush('static', self.symbolTable.indexOf(name))
                    else:
                        self.vw.writePush('this', self.symbolTable.indexOf(name))
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

    def writePush(self, name, lastName):
        if name in self.symbolTable.currentScopeSymbols:
            if self.symbolTable.kindOf(name) == 'var':
                self.vw.writePush('local', self.symbolTable.indexOf(name))
            elif self.symbolTable.kindOf(name) == 'arg':
                self.vw.writePush('argument', self.symbolTable.indexOf(name))
        else:
            if self.symbolTable.kindOf(name) == 'static':
                self.vw.writePush('static', self.symbolTable.indexOf(name))
            else:
                self.vw.writePush('this', self.symbolTable.indexOf(name))

    def writePop(self, name):
        if name in self.symbolTable.currentScopeSymbols:
            if self.symbolTable.kindOf(name) == 'var':
                self.vw.writePop('local', self.symbolTable.indexOf(name))
            elif self.symbolTable.kindOf(name) == 'arg':
                self.vw.writePop('argument', self.symbolTable.indexOf(name))
        else:
            if self.symbolTable.kindOf(name) == 'static':
                self.vw.writePop('static', self.symbolTable.indexOf(name))
            else:
                self.vw.writePop('this', self.symbolTable.indexOf(name))