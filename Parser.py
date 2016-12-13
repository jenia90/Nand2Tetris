class Parser:
    def __init__(self, file):
        self.file = file
        self.numOfCommands = len(file)
        self.cmdTypeList = ['A_COMMAND', 'C_COMMAND', 'L_COMMAND']

    def hasMoreCommand(self):
        return

    def advance(self):
        return

    def commandType(self):
        return

    def symbol(self):
        return

    def dest(self):
        return

    def comp(self):
        return

    def jump(self):
        return