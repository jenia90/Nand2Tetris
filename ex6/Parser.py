from Code import *

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
SPLITTING = 1
JUMP = 1
RESET_INDEX = 0

class Parser:
    def __init__(self, file):
        self.fileLines = [l.strip() for l in file.readlines()
                          if not l.strip().startswith(COMMENT)
                          and len(l.strip()) > EMPTY_STRING]
        self.currentIndex = RESET_INDEX

    def hasMoreCommands(self):
        return self.currentIndex < len(self.fileLines)

    def advance(self):
        self.currenntIndex += 1

    def commandType(self):
        command = self.fileLines[self.currentIndex]
        if command.startswith(AT) and len(command) > CORRECT_SYNTAX:
            return A_COMMAND
        elif command.startswith(LBRKT) and command.endswith(RBRKT):
            return L_COMMAND
        elif EQU in command and SEMIC in command:
            return C_COMMAND

    def symbol(self):
        if self.commandType() is A_COMMAND:
            return self.fileLines[self.currentIndex][COMMAND_START:]
        elif self.commandType() is L_COMMAND:
            return self.fileLines[self.currentIndex][COMMAND_START:COMMAND_ENDS]

    def dest(self):
        if self.commandType() is C_COMMAND:
            return Code.dest(self.fileLines[self.currentIndex].split(EQU)[DEST])

    def comp(self):
        if self.commandType() is C_COMMAND:
            return Code.comp(self.fileLines[self.currentIndex].split(EQU)[SPLITTING].split(SEMIC)[COMP])

    def jump(self):
        if self.commandType() is C_COMMAND:
            return Code.jump(self.fileLines[self.currentIndex].split(SEMIC)[JUMP])