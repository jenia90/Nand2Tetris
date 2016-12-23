COMMENT = '//'

ARITHMETIC_COMM = 'C_ARITHMETIC'
PUSH_COMM = 'C_PUSH'
POP_COMM = 'C_POP'
LABEL_COMM = 'C_LABEL'
GOTO_COMM = 'C_GOTO'
IF_COMM = 'C_IF'
FUNCTION_COMM = 'C_FUNCTION'
RETURN_COMM = 'C_RETURN'
CALL_COMM = 'C_CALL'


class Parser:
    """
    Parses a .vm file
    """

    def __init__(self, file):
        self._lines = [l.split(COMMENT)[0].strip() for l in file.readlines()
                       if not l.strip().startswith(COMMENT)
                       and len(l.strip()) > 0]
        self._currentIndex = 0
        self._currentCommand = ''
        self._currCommType = ''
        self._updateCurrentCommand()

    def hasMoreCommands(self):
        """
        Checks if there are more commands to process.
        :return: true if there are more commands; false otherwise.
        """
        return self.currentIndex < len(self.fileLines)

    def advance(self):
        """
        Advances the current command pointer to the next command
        """
        self.currentIndex += 1
        self.updateCurrentCommand()

    def _updateCurrentCommand(self):
        """
        Updates variables associated with the current command, such as its type
        and the string itself.
        """
        if not self.hasMoreCommands():
            return
        self.currentCommand = \
            self.fileLines[self.currentIndex % len(self.fileLines)]
        self.currCommType = self.commandType()

    def getCurrentType(self):
        """
        Returns current command type.
        """
        return self.currCommType

    def resetCount(self):
        """
        Resets the current command pointer
        """
        self.currentIndex = 0
        self.updateCurrentCommand()

    def commandType(self):
        """
        Gets the type of the current command
        :return: Command type string
        """
        return

    def arg1(self):
        """
        First command argument
        :return: first command argument string
        """
        return

    def arg2(self):
        """
        Second command argument
        :return: second command argument string
        """
        return
