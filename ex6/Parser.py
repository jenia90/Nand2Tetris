import Code
class Parser:

    A_COMMAND = 'A_COMMAND'
    C_COMMAND = 'C_COMMAND'
    L_COMMAND = 'L_COMMAND'

    def __init__(self, file):
        self.fileLines = [l.strip() for l in file.readlines()
                          if not l.strip().startswith('//')
                          and len(l.strip()) > 0]
        self.currentIndex = 0

    def hasMoreCommands(self):
        return self.currentIndex < len(self.fileLines)

    def advance(self):
        self.currenntIndex += 1

    def commandType(self):
        command = self.fileLines[self.currentIndex]
        if command.startswith('@') and len(command) > 1:
            return self.A_COMMAND
        elif command.startswith('(') and command.endswith(')'):
            return self.L_COMMAND
        elif command.contains('=',';'):
            return self.C_COMMAND

    def symbol(self):
        if self.commandType() is self.A_COMMAND:
            return self.fileLines[self.currentIndex][1:]
        elif self.commandType() is self.L_COMMAND:
            return self.fileLines[self.currentIndex][1:-1]

    def dest(self):
        if self.commandType() is self.C_COMMAND:
            return Code.Code.dest(self.fileLines[self.currentIndex].split('=')[0])

    def comp(self):
        if self.commandType() is self.C_COMMAND:
            return Code.Code.comp(self.fileLines[self.currentIndex].split('=')[1].split(';')[0])

    def jump(self):
        if self.commandType() is self.C_COMMAND:
            return Code.Code.jump(self.fileLines[self.currentIndex].split(';')[1])