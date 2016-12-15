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


class Parser:
    def __init__(self, file):
        self.fileLines = [l.strip() for l in file.readlines()
                          if not l.strip().startswith(COMMENT)
                          and len(l.strip()) > 0]
        self.currentIndex = 0

    def hasMoreCommands(self):
        return self.currentIndex < len(self.fileLines)

    def advance(self):
        self.currenntIndex += 1

    def commandType(self):
        command = self.fileLines[self.currentIndex]
        if command.startswith(AT) and len(command) > 1:
            return A_COMMAND
        elif command.startswith(LBRKT) and command.endswith(RBRKT):
            return L_COMMAND
        elif EQU in command and SEMIC in command:
            return C_COMMAND

    def symbol(self):
        if self.commandType() is A_COMMAND:
            return self.fileLines[self.currentIndex][1:]
        elif self.commandType() is L_COMMAND:
            return self.fileLines[self.currentIndex][1:-1]

    def dest(self):
        if self.commandType() is C_COMMAND:
            return Code.dest(self.fileLines[self.currentIndex].split(EQU)[0])

    def comp(self):
        if self.commandType() is C_COMMAND:
            return Code.comp(self.fileLines[self.currentIndex].split(EQU)[1].split(SEMIC)[0])

    def jump(self):
        if self.commandType() is C_COMMAND:
            return Code.jump(self.fileLines[self.currentIndex].split(SEMIC)[1])