class Parser:
    def __init__(self, file):
        self.fileLines = [l.strip() for l in file.readlines()
                          if not l.strip().startswith('//')
                          and len(l.strip()) > 0]
        self.cmdTypeList = ['A_COMMAND', 'C_COMMAND', 'L_COMMAND']

    def hasMoreCommand(self):
        return len(self.file) > 0

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