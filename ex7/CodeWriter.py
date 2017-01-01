FNAME_SEP = '.'
NOT_OPER = '!'
OR_OPER = '|'
AND_OPER = '&'
NEG_OPER = '-'
SUB_OPER = '-'
ADD_OPER = '+'
WRITE_ACCESS = 'w'
OUTFILE_EXT = '.asm'

from os import sep, path
from Parser import POP_COMM, PUSH_COMM
from Parser import ADD_COMM, SUB_COMM, NEG_COMM, EQ_COMM, GT_COMM, LT_COMM, \
    AND_COMM, OR_COMM, NOT_COMM
from Parser import CALL_COMM, FUNCTION_COMM, RETURN_COMM, LABEL_COMM, \
    GOTO_COMM, IF_COMM


class CodeWriter:
    """
    Writes a piece of code as a hack machine language
    """

    def __init__(self, outfile):
        '''
        Opens the output file/stream and gets ready to write into it.
        :param outfile: output file
        '''
        self._outfile = open(outfile, WRITE_ACCESS)
        self._currFileName = ''
        self._count = 0
        self._segments = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS',
                          'that': 'THAT', 'pointer': '3', 'temp': '5'}

        self._indexes = {24576: 'KBD', 1: 'R1', 2: 'R2', 3: 'R3', 4: 'R4',
                         5: 'R5', 16384: 'SCREEN', 7: 'R7', 8: 'R8', 9: 'R9',
                         10: 'R10', 11: 'R11', 12: 'R12', 13: 'R13', 14: 'R14',
                         15: 'R15', 6: 'R6', 0: 'SP'}

        self._funcCallCounts = {}

        self._registers = ['local', 'argument', 'this', 'that']
        self.writeInit()

    def writeInit(self):
        """
        Writes the bootstrap code to the asm file
        :return:
        """
        self._outfile.write('@256\n'
                            'D=A\n'
                            '@SP\n'
                            'M=D\n')
        self.writeCall('Sys.init', 0)

    def setFileName(self, filename):
        """
        Informs the code writer that the translation of a new VM file started.
        :param filename: filename of the new file
        """
        self._currFileName = filename

    def unaryOper(self, oper):
        return '@SP\n' \
               'M=M-1\n' \
               'A=M\n' \
               'M=' + oper + 'M\n' \
               '@SP\n' \
               'M=M+1\n'

    def binaryOper(self, oper):
        return '@SP\n' \
               'M=M-1\n' \
               'A=M\n' \
               'D=M\n' \
               '@SP\n' \
               'M=M-1\n' \
               'A=M\n' \
               'M=M' + oper + 'D\n' \
               '@SP\n' \
               'M=M+1\n'

    def compareOper(self, oper):
        self._count += 1
        varString = FNAME_SEP + self._currFileName + FNAME_SEP + str(self._count)

        return '@SP\n' \
               'M=M-1\n' \
               'A=M\n' \
               'D=M\n' \
               '@R13\n' \
               'M=D\n' \
               '@yNeg' + varString + '\n' +\
               'D;JLT\n' \
               '@SP\n' \
               'M=M-1\n' \
               'A=M\n' \
               'D=M\n' \
               '@yPosXNeg' + varString + '\n' \
               'D;JLT\n' \
               '@R13\n' \
               'D=D-M\n' \
               '@CHECK' + varString + '\n' \
               '0;JMP\n' \
               '(yNeg' + varString + ')\n' \
               '@SP\n' \
               'M=M-1\n' \
               'A=M\n' \
               'D=M\n' \
               '@yNegXPos' + varString + '\n' \
               'D;JGT\n' \
               '@R13\n' \
               'D=D-M\n' \
               '@CHECK' + varString + '\n' \
               '0;JMP\n' \
               '(yPosXNeg' + varString + ')\n' \
               'D=-1\n' \
               '@CHECK' + varString + '\n' \
               '0;JMP\n' \
               '(yNegXPos' + varString + ')\n' \
               'D=1\n' \
               '@CHECK' + varString + '\n' \
               '0;JMP\n' \
               '(CHECK' + varString + ')\n' \
               '@ISTRUE' + varString + '\n' \
               'D;J' + oper.upper() + '\n' \
               'D=0\n' \
               '@AFTER' + varString + '\n' \
               '0;JMP\n' \
               '(ISTRUE' + varString + ')\n' \
               'D=-1\n' \
               '@AFTER' + varString + '\n' \
               '0;JMP\n' \
               '(AFTER' + varString + ')\n' \
               '@SP\n' \
               'A=M\n' \
               'M=D\n' \
               '@SP\n' \
               'M=M+1\n'

    def writeArithmetic(self, command):
        """
        Writes the assemble code that is the translation of the given
        arithmetic command.
        :param command: Arithmetic command string
        """
        cmd_str = ''
        if command == ADD_COMM:
            cmd_str = self.binaryOper(ADD_OPER)
        elif command == SUB_COMM:
            cmd_str = self.binaryOper(SUB_OPER)
        elif command == NEG_COMM:
            cmd_str = self.unaryOper(NEG_OPER)
        elif command == AND_COMM:
            cmd_str = self.binaryOper(AND_OPER)
        elif command == OR_COMM:
            cmd_str = self.binaryOper(OR_OPER)
        elif command == NOT_COMM:
            cmd_str = self.unaryOper(NOT_OPER)
        elif command in [EQ_COMM, LT_COMM, GT_COMM]:
            cmd_str = self.compareOper(command)

        self._outfile.write(cmd_str)

    def writeLabel(self, label):
        return '(' + label + ')\n'

    def writeGoto(self, label):
        return '@' + label + '\n' \
               '0;JMP\n'

    def writeIf(self, label):
        return '@SP\n' \
               'M=M-1\n' \
               'A=M\n'\
               'D=M\n' \
               '@' + label + '\n' \
               'D;JNE\n'

    def writeBranching(self, command, label):
        """
        Writes a given branching command
        :param command: command string such as 'label', 'goto', etc.
        :param label: the label string
        """
        cmd_str = ''

        if command == LABEL_COMM:
            cmd_str = self.writeLabel(label)

        elif command == GOTO_COMM:
            cmd_str = self.writeGoto(label)

        elif command == IF_COMM:
            cmd_str = self.writeIf(label)

        self._outfile.write(cmd_str)

    def backupPointer(self, pointer):
        return '@' + pointer + '\n' \
               'D=M\n' + self.pushStackOper('D')


    def writeFunction(self, name, nArgs):
        cmd_str = self.writeLabel(name)
        for i in range(nArgs):
            self.pushStackOper('0')

        return cmd_str

    def writeCall(self, name, nArgs):
        if name in self._funcCallCounts:
            self._funcCallCounts[name] = 0

        self._funcCallCounts[name] += 1
        count = self._funcCallCounts[name]

        ret_name = name + '$ret.' + count
        cmd_str = '@' + ret_name + '\n'
        cmd_str += 'D=A\n'
        for p in ['LCL', 'ARG', 'THIS', 'THAT']:
            cmd_str += self.backupPointer(p)

        cmd_str += '@SP\n' \
                   'D=M\n' \
                   '@' + str(nArgs + 5) + '\n' \
                   'D=D-A\n' \
                   '@ARG\n' \
                   'M=D\n' \
                   '@SP\n' \
                   'D=M\n' \
                   '@LCL\n' \
                   'M=D\n'

        self._outfile.write(cmd_str)
        self.writeGoto(name)
        self.writeLabel(ret_name)


        return cmd_str

    def writeReturn(self):
        cmd_str = ''

        return cmd_str

    def writeFuncCommand(self, command, arg1, arg2):
        """
        Writes a function related command.
        :param command: Command string such as 'call', etc.
        :param arg1: function label
        :param arg2: number of arguments
        """
        cmd_str = ''

        if command == FUNCTION_COMM:
            cmd_str = self.writeFunction(arg1, arg2)
        elif command == RETURN_COMM:
            cmd_str = self.writeReturn()
        elif command == CALL_COMM:
            cmd_str = self.writeFunction(arg1, arg2)

        self._outfile.write(cmd_str)

    def pushStackOper(self, arg):
        """
        Pushes a values to the stack
        """
        return '@SP\n' \
               'A=M\n' \
               'M=' + arg + '\n' \
               '@SP\n' \
               'M=M+1\n'

    def popFromStack(self, segment, index):
        """
        Pops a value from the stack
        """
        cmd_str = '@' + index + '\n' \
                  'D=A\n' \
                  '@' + self._segments[segment] + '\n'

        if segment in self._registers:
            cmd_str += 'A=M\n'

        cmd_str += 'D=A+D\n' \
                      '@R13\n' \
                      'M=D\n' \
                      '@SP\n' \
                      'M=M-1\n' \
                      'A=M\n' \
                      'D=M\n' \
                      '@R13\n' \
                      'A=M\n' \
                      'M=D\n'

        return cmd_str

    def writePushPop(self, command, segment, index):
        """
        Writes the assembly code that is the translation of the given
        command ,
        where command is either C_PUSH or C_POP
        :param command: command type
        :param segment:
        :param index:
        """
        idx_str = self._indexes.get(int(index), index)
        cmd_str = ''
        static_var = '@' + self._outfile.name.split(FNAME_SEP)[-2].\
                                split(sep)[-1] + FNAME_SEP + idx_str + '\n'

        if command == PUSH_COMM:
            if segment == 'temp' or segment == 'pointer':
                cmd_str = '@' + idx_str + '\n' + \
                             'D=A\n' + \
                             '@' + self._segments[segment] + '\n' + \
                             'A=A+D\n' + \
                             'D=M\n' + \
                             self.pushStackOper('D')

            elif segment in self._registers:
                cmd_str = '@' + idx_str + '\n' \
                             'D=A\n' \
                             '@' + self._segments[segment] + '\n' \
                             'A=M+D\n' \
                             'D=M\n' + self.pushStackOper('D')

            elif segment == 'constant':
                cmd_str = '@' + idx_str + '\n' \
                          'D=A\n' + self.pushStackOper('D')

            elif segment == 'static':
                cmd_str = static_var + 'D=M\n' + self.pushStackOper('D')

        elif command == POP_COMM:
            if segment == 'static':
                cmd_str = '@SP\n' \
                          'M=M-1\n' \
                          'A=M\n' \
                          'D=M\n' +\
                          static_var + 'M=D\n'
            else:
                cmd_str = self.popFromStack(segment, index)

        self._outfile.write(cmd_str)

    def close(self):
        """
        Closes the output file
        """
        self._outfile.close()
