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

NOT_COMM = 'not'
OR_COMM = 'or'
AND_COMM = 'and'
LT_COMM = 'lt'
GT_COMM = 'gt'
EQ_COMM = 'eq'
NEG_COMM = 'neg'
SUB_COMM = 'sub'
ADD_COMM = 'add'


class Parser:
    """
    Parses a .vm file
    """

    def __init__(self, file):
        self.fileLines = [l.split(COMMENT)[0].strip() for l in file.readlines()
                       if not l.strip().startswith(COMMENT)
                       and len(l.strip()) > 0]
        self.cArithmeticCommands = [ADD_COMM, SUB_COMM, NEG_COMM, EQ_COMM,
                                GT_COMM, LT_COMM, AND_COMM, OR_COMM, NOT_COMM]
        self._currCommandArray = []
        self._currentIndex = 0
        self._currentLine = ''
        self._currCommType = ''
        self._updateCurrentCommand()

    def hasMoreCommands(self):
        """
        Checks if there are more commands to process.
        :return: true if there are more commands; false otherwise.
        """
        return self._currentIndex < len(self.fileLines)

    def advance(self):
        """
        Advances the current command pointer to the next command
        """
        self._currentIndex += 1
        self._updateCurrentCommand()

    def _updateCurrentCommand(self):
        """
        Updates variables associated with the current command, such as its type
        and the string itself.
        """
        if not self.hasMoreCommands():
            return
        self._currentLine = self.fileLines[self._currentIndex % len(self.fileLines)]
        self._currCommandArray = self._currentLine.split()
        self._currCommType = self.commandType()

    def getCurrentType(self):
        """
        Returns current command type.
        """
        return self._currCommType

    def resetCount(self):
        """
        Resets the current command pointer
        """
        self._currentIndex = 0
        self._updateCurrentCommand()

    def commandType(self):
        """
        Gets the type of the current command
        :return: Command type string
        """
        if self._currCommandArray[0] in self.cArithmeticCommands:
            return ARITHMETIC_COMM
        elif self._currCommandArray[0] == 'pop':
            return POP_COMM
        elif self._currCommandArray[0] == 'push':
            return PUSH_COMM
        elif self._currCommandArray[0] == 'label':
            return LABEL_COMM
        elif self._currCommandArray[0] == 'goto':
            return GOTO_COMM
        elif self._currCommandArray[0] == 'if-goto':
            return IF_COMM
        elif self._currCommandArray[0] == 'function':
            return FUNCTION_COMM
        elif self._currCommandArray[0] == 'call':
            return FUNCTION_COMM
        elif self._currCommandArray[0] == 'return':
            return FUNCTION_COMM

    def getCommandString(self):
        return self._currCommandArray[0].strip()

    def arg1(self):
        """
        First command argument
        :return: first command argument string
        """
        if len(self._currCommandArray) > 1:
            return self._currCommandArray[1].strip()

    def arg2(self):
        """
        Second command argument
        :return: second command argument string
        """
        if len(self._currCommandArray) > 2:
            return self._currCommandArray[2].strip()
