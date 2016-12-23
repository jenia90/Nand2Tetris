class CodeWriter:
    """
    Writes a piece of code as a hack machine language
    """

    def __init__(self, outfile):
        """
        Opens the output file/stream and gets ready to write into it.
        :param outfile: output file
        """
        self._outfile = outfile

    def setFileName(self, filename):
        """
        Informs the code writer that the translation of a new VM file started.
        :param filename: filename of the new file
        """
        return

    def writeArithmetic(self, command):
        """
        Writes the assemble code that is the translation of the given arithemetic command.
        :param command:
        :return:
        """
        return

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
