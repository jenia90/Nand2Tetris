NOT_OPER = '!'
OR_OPER = '|'
AND_OPER = '&'
NEG_OPER = '-'
SUB_OPER = '-'
ADD_OPER = '+'
WRITE_ACCESS = 'w'
OUTFILE_EXT = '.asm'

from os import sep
from Parser import POP_COMM, PUSH_COMM
from Parser import ADD_COMM, SUB_COMM, NEG_COMM, EQ_COMM, GT_COMM, LT_COMM, \
    AND_COMM, OR_COMM, NOT_COMM


class CodeWriter:
    """
    Writes a piece of code as a hack machine language
    """

    def __init__(self, outfile):
        '''
        Opens the output file/stream and gets ready to write into it.
        :param outfile: output file
        '''
        self._outfile = open(outfile + OUTFILE_EXT, WRITE_ACCESS)
        self._currFileName = ''
        self._count = 0
        self._segments = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS',
                         'that'  : 'THAT', 'pointer': '3', 'temp': '5'}
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
                'M=' + oper +'M\n' \
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
                'M=M+1'

    def compareOper(self, oper):
        self._count += 1
        varString = '.' + self._currFileName + '.' + str(self._count)

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
                'D=D - M\n' \
                '@CHECK' + varString + '\n' \
                '0;JMP\n' \
                '(yNeg' + varString + ')\n' \
                '@SP\n' \
                'M=M-1\n' \
                'A=M\n' \
                'D=M\n' \
                '@yNegXPos'+ varString + '\n' \
                'D;JGT\n' \
                '@R13\n' \
                'D=D - M\n' \
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
        :param command:
        :return:
        """
        c_str = ''
        if command is ADD_COMM:
            c_str = self.binaryOper(ADD_OPER)
        elif command is SUB_COMM:
            c_str = self.binaryOper(SUB_OPER)
        elif command is NEG_COMM:
            c_str = self.unaryOper(NEG_OPER)
        elif command is AND_COMM:
            c_str = self.binaryOper(AND_OPER)
        elif command is OR_COMM:
            c_str = self.binaryOper(OR_OPER)
        elif command is NOT_COMM:
            c_str = self.unaryOper(NOT_OPER)
        elif command in [EQ_COMM, LT_COMM, GT_COMM]:
            c_str = self.compareOper(command)

        self._outfile.write(c_str)

    def pushStackOper(self):
        return '@SP\n' \
                'A=M\n' \
                'M=D\n' \
                '@SP\n' \
                'M=M+1\n'

    def popFromStack(self, segment, index):
        commandStr = '@' + index + '\n' + \
                     'D=A\n' + \
                     '@' + self._segments[segment] + '\n'

        if segment in self._registers:
            commandStr += 'D=A+D\n' \
                            '@R13\n' \
                            'M=D\n' \
                            '@SP\n' \
                            'M=M-1\n' \
                            'A=M\n' \
                            'D=M\n' \
                            '@R13\n' \
                            'A=M\n' \
                            'M=D\n'

        return commandStr

    def writePushPop(self, command, segment, index):
        """
        Writes the assembly code that is the translation of the given
        command ,
        where command is either C_PUSH or C_POP
        :param command: command type
        :param segment:
        :param index:
        """
        commandStr = ''
        staticVar = '@' + self._outfile.name.split('.')[0].replace(sep,'.') + \
                    '.' + index + '\n'
        if command is PUSH_COMM:
            if segment == 'temp' or segment == 'pointer':
                commandStr = '@' + index + '\n' + \
                             'D=A\n' + \
                             '@' + self._segments[segment] + '\n' + \
                             'A = A + D\n' + \
                             'D = M\n' + \
                             self.pushStackOper()
            elif segment in self._registers:
                commandStr = '@' + index + '\n' \
                             'D=A\n' \
                             '@' + self._segments[segment] + '\n' \
                             'A=M+D\n' \
                             'D=M\n' + self.pushStackOper()
            elif segment == 'constant':
                commandStr = '@' + index + '\n' \
                            'D=A\n' + self.pushStackOper()

            elif segment == 'static':
                commandStr = staticVar + 'D=M\n' + self.pushStackOper()

        elif command is POP_COMM:
            if segment == 'static':
                commandStr = '@SP\n' \
                                'M=M-1\n' \
                                'A=M\n' \
                                'D=M\n' +\
                                staticVar + 'M=D\n'
            else:
                commandStr = self.popFromStack(segment, index)

        self._outfile.write(commandStr)

    def close(self):
        """
        Closes the output file
        :return:
        """
        self._outfile.close()
