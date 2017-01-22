class VMWriter:
    def __init__(self, out_file):
        self._out = open(out_file, 'w')

    def writePush(self, segment, index):
        self._out.write('push ' + segment + ' ' + str(index) + '\n')

    def writePop(self, segment, index):
        self._out.write('pop ' + segment + ' ' + str(index) + '\n')

    def writeArithmetic(self, command):
        self._out.write(command + '\n')

    def writeLabel(self, label):
        self._out.write('label ' + label + '\n')

    def writeGoto(self, label):
        self._out.write('goto ' + label + '\n')

    def writeIf(self, label):
        self._out.write('if-goto ' + label + '\n')

    def writeCall(self, name, nArgs):
        self._out.write('call ' + name + ' ' + str(nArgs) + '\n')

    def writeFunction(self, name, nArgs):
        self._out.write('function ' + name + ' ' + str(nArgs) + '\n')

    def writeReturn(self):
        self._out.write('return\n')

    def close(self):
        self._out.close()
