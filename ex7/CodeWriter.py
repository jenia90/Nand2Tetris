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
from Parser import CALL_KWD, FUNCTION_KWD, GOTO_KWD, IF_GOTO_KWD, LABEL_KWD,\
    POP_KWD, PUSH_KWD, RET_KWD


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

        self._registers = ['local', 'argument', 'this', 'that']

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

    def writeBranching(self, command, label):
        """
        Writes a given branching command
        :param command: command string such as 'label', 'goto', etc.
        :param label: the label string
        """
        cmd_str = ''

        if command == LABEL_KWD:
            cmd_str = '(' + label + ')\n'

        elif command == GOTO_KWD:
            cmd_str = '@' + label + '\n' \
                        'M;JMP\n'

        elif command == IF_GOTO_KWD:
            cmd_str = '@SP\n' \
                        'M=M-1\n' \
                        'D=M\n' \
                        '@SP\n' \
                        'M=M+1\n' \
                        '@' + label + '\n'\
                        'D;JEQ\n'

        self._outfile.write(cmd_str)

    def writeFuncCommand(self, command, arg1, arg2):
        """
        Writes a function related command.
        :param command: Command string such as 'call', etc.
        :param arg1: function label
        :param arg2: number of arguments
        """
        cmd_str = ''

        if command == FUNCTION_KWD:
            # TODO: add implementation here
            return
        elif command == RET_KWD:
            # TODO: add implementation here
            return
        elif command == CALL_KWD:
            # TODO: add implementation here
            return

        self._outfile.write(cmd_str)

    def pushStackOper(self):
        """
        Pushes a values to the stack
        """
        return '@SP\n' \
               'A=M\n' \
               'M=D\n' \
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
                             self.pushStackOper()

            elif segment in self._registers:
                cmd_str = '@' + idx_str + '\n' \
                             'D=A\n' \
                             '@' + self._segments[segment] + '\n' \
                             'A=M+D\n' \
                             'D=M\n' + self.pushStackOper()

            elif segment == 'constant':
                cmd_str = '@' + idx_str + '\n' \
                             'D=A\n' + self.pushStackOper()

            elif segment == 'static':
                cmd_str = static_var + 'D=M\n' + self.pushStackOper()

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
