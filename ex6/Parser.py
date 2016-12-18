AT = '@'
EQU = '='
SEMIC = ';'
LBRKT = '('
RBRKT = ')'
COMMENT = '//'
A_COMMAND = 'A_COMMAND'
C_COMMAND = 'C_COMMAND'
L_COMMAND = 'L_COMMAND'
EMPTY_STRING = 0
CORRECT_SYNTAX = 1
COMMAND_START = 1
COMMAND_ENDS = -1
DEST = 0
COMP = 0
COMP_JUMP = 1
JUMP = 1
RESET_INDEX = 0

class Parser:
    def __init__(self, file):
        self.fileLines = [l.split(COMMENT)[0].strip() for l in file.readlines()
                          if not l.strip().startswith(COMMENT)
                          and len(l.strip()) > EMPTY_STRING]
        self.currentIndex = 0
        self.currentCommand = ''
        self.currCommType = ''
        self.updateCurrentCommand()

    def hasMoreCommands(self):
        return self.currentIndex < len(self.fileLines)

    def advance(self):
        self.currentIndex += 1
        self.updateCurrentCommand()


    def updateCurrentCommand(self):
        self.currentCommand = \
            self.fileLines[self.currentIndex % len(self.fileLines)]
        self.currCommType = self.commandType()

    def getCurrentType(self):
        return self.currCommType

    def resetCount(self):
        self.currentIndex = 0
        self.currentCommand = self.fileLines[self.currentIndex]

    def commandType(self):
        if self.currentCommand.startswith(AT) and len(self.currentCommand) > 1:
            return A_COMMAND

        elif self.currentCommand.startswith(LBRKT):
            return L_COMMAND

        elif EQU in self.currentCommand or SEMIC in self.currentCommand:
            return C_COMMAND

    def symbol(self):
        if self.currCommType is A_COMMAND:
            return self.currentCommand[COMMAND_START:].strip()

        elif self.currCommType is L_COMMAND:
            return self.currentCommand[COMMAND_START:COMMAND_ENDS].strip()

    def dest(self):
        if EQU in self.currentCommand:
            return self.currentCommand.split(EQU)[DEST].strip()

    def comp(self):
        if self.currCommType is C_COMMAND:
            if EQU in self.currentCommand:
                return self.currentCommand.\
                    split(EQU)[COMP_JUMP].\
                    split(SEMIC)[COMP].strip()

            else:
                return self.currentCommand.split(SEMIC)[0].strip()

    def jump(self):
        if self.commandType() is C_COMMAND and SEMIC in self.currentCommand:
            return self.currentCommand.split(SEMIC)[JUMP].strip()
