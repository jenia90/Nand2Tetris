NOT_OPER = '!'
OR_OPER = '|'
AND_OPER = '&'
NEG_OPER = '-'
SUB_OPER = '-'
ADD_OPER = '+'
WRITE_ACCESS = 'w'
OUTFILE_EXT = '.asm'


class CodeWriter:
    """
    Writes a piece of code as a hack machine language
    """

    def __init__(self, outfile):
        """
        Opens the output file/stream and gets ready to write into it.
        :param outfile: output file
        """
        self._outfile = open(outfile + OUTFILE_EXT, WRITE_ACCESS)
        self._currFileName = ''
        self._count = 0

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
        return "@SP\n" \
                 "M=M-1\n" \
                 "A=M\n" \
                 "D=M\n" \
                 "@R13\n" \
                 "M=D\n" \
                 "@yNeg" + str(self._count) + "\n" \
                 "D;JLT\n" \
                 "@SP\n" \
                 "M=M-1\n" \
                 "A=M\n" \
                 "D=M\n" \
                 "@yPosXNeg" + str(self._count) + "\n" \
                 "D;JLT\n" \
                 "@R13\n" \
                 "D=D - M\n" \
                 "@CHECK" + str(self._count) + "\n" \
                 "0;JMP\n" \
                 "(yNeg" + str(self._count) + ")\n" \
                 "@SP\n" \
                 "M=M-1\n" \
                 "A=M\n" \
                 "D=M\n" \
                 "@yNegXPos" + str(self._count) + "\n" \
                 "D;JGT\n" \
                 "@R13\n" \
                 "D=D - M\n" \
                 "@CHECK" + str(self._count) + "\n" \
                 "0;JMP\n" \
                 "(yPosXNeg" + str(self._count) + ")\n" \
                 "D=-1\n" \
                 "@CHECK" + str(self._count) + "\n" \
                 "0;JMP\n" \
                 "(yNegXPos" + str(self._count) + ")\n" \
                 "D=1\n" \
                 "@CHECK" + str(self._count) + "\n" \
                 "0;JMP\n" \
                 "(CHECK" + str(self._count) + ")\n" \
                 "@ISTRUE" + str(self._count) + "\n" \
                 "D;J" + oper.upper() + "\n" \
                 "D=0\n" \
                 "@AFTER" + str(self._count) + "\n" \
                 "0;JMP\n" \
                 "(ISTRUE" + str(self._count) + ")\n" \
                 "D=-1\n" \
                 "@AFTER" + str(self._count) + "\n" \
                 "0;JMP\n" \
                 "(AFTER" + str(self._count) + ")\n" \
                 "@SP\n" \
                 "A=M\n" \
                 "M=D\n" \
                 "@SP\n" \
                 "M=M+1\n"

    def writeArithmetic(self, command):
        """
        Writes the assemble code that is the translation of the given
        arithmetic command.
        :param command:
        :return:
        """
        if command is 'add':
            c_str = self.binaryOper(ADD_OPER)
        elif command is 'sub':
            c_str = self.binaryOper(SUB_OPER)
        elif command is 'neg':
            c_str = self.unaryOper(NEG_OPER)
        elif command is 'and':
            c_str = self.binaryOper(AND_OPER)
        elif command is 'or':
            c_str = self.binaryOper(OR_OPER)
        elif command is 'not':
            c_str = self.unaryOper(NOT_OPER)
        else:
            c_str = self.compareOper(command)

        self._outfile.write(c_str)


    def writePushPop(self, command, segment, index):
        """
        Wrties the assembly code that is the translation of the given command ,
        where command is either C_PUSH or C_POP
        :param command: command type
        :param segment:
        :param index:
        """
        return

    def close(self):
        """
        Closes the output file
        :return:
        """
        self._outfile.close()
