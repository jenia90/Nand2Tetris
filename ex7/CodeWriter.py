FNAME_SEP = '.'
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
        return '\n'.join(['@SP',
                          'M=M-1',
                          'A=M',
                          'M=' + oper + 'M',
                          '@SP',
                          'M=M+1',
                          ''])

    def binaryOper(self, oper):
        return '\n'.join(['@SP',
                          'M=M-1',
                          'A=M',
                          'D=M',
                          '@SP',
                          'M=M-1',
                          'A=M',
                          'M=M' + oper + 'D',
                          '@SP',
                          'M=M+1',
                          ''])

    def compareOper(self, oper):
        self._count += 1
        varString = FNAME_SEP + self._currFileName + FNAME_SEP + \
                    str(self._count)

        return '\n'.join(['@SP',
                          'M=M-1',
                          'A=M',
                          'D=M',
                          '@SP',
                          'M=M-1',
                          'A=M',
                          'D=M-D',
                          '@cor' + varString,
                          'D;J' + oper.upper(),
                          'D=0',
                          '@after' + varString,
                          '0;JMP',
                          '(cor' + varString + ')',
                          'D=-1',
                          '@after' + varString,
                          '0;JMP',
                          '(after' + varString + ')',
                          '@SP',
                          'A=M',
                          'M=D',
                          '@SP',
                          'M=M+1',
                          ''])

    def writeArithmetic(self, command):
        """
        Writes the assemble code that is the translation of the given
        arithmetic command.
        :param command:
        :return:
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

    def pushStackOper(self):
        """
        Pushes a values to the stack
        """
        return '\n'.join(['@SP',
                          'A=M',
                          'M=D',
                          '@SP',
                          'M=M+1',
                          ''])

    def popFromStack(self, segment, index):
        """
        Pops a value from the stack
        """
        cmd_str = '\n'.join(['@' + index,
                             'D=A',
                             '@' + self._segments[segment],
                             ''])

        if segment in self._registers:
            cmd_str += 'A=M\n'

        cmd_str += '\n'.join(['D=A+D',
                              '@R13',
                              'M=D',
                              '@SP',
                              'M=M-1',
                              'A=M',
                              'D=M',
                              '@R13',
                              'A=M',
                              'M=D',
                              ''])

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
        static_var = '@' + self._outfile.name.split(FNAME_SEP)[-2]. \
            split(sep)[-1] + FNAME_SEP + idx_str

        if command == PUSH_COMM:
            if segment == 'temp' or segment == 'pointer':
                cmd_str = '\n'.join(['@' + idx_str,
                                     'D=A',
                                     '@' + self._segments[segment],
                                     'A=A+D',
                                     'D=M',
                                     self.pushStackOper()])

            elif segment in self._registers:
                cmd_str = '\n'.join(['@' + idx_str,
                                     'D=A',
                                     '@' + self._segments[segment],
                                     'A=M+D',
                                     'D=M',
                                     self.pushStackOper()])

            elif segment == 'constant':
                cmd_str = '\n'.join(['@' + idx_str,
                                     'D=A',
                                     self.pushStackOper()])

            elif segment == 'static':
                cmd_str = '\n'.join([static_var,
                                     'D=M',
                                     self.pushStackOper()])

        elif command == POP_COMM:
            if segment == 'static':
                cmd_str = '\n'.join(['@SP',
                                     'M=M-1',
                                     'A=M',
                                     'D=M',
                                     static_var,
                                     'M=D',
                                     ''])
            else:
                cmd_str = self.popFromStack(segment, index)

        self._outfile.write(cmd_str)

    def close(self):
        """
        Closes the output file
        """
        self._outfile.close()
