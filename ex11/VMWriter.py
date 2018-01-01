class VMWriter:
    def __init__(self, out_file):
        self._out = out_file

    def write_push(self, segment, index):
        self._out.write('push ' + segment + ' ' + str(index) + '\n')
        self._out.flush()

    def write_pop(self, segment, index):
        self._out.write('pop ' + segment + ' ' + str(index) + '\n')
        self._out.flush()

    def write_arithmetic(self, command):
        self._out.write(command + '\n')
        self._out.flush()

    def write_label(self, label):
        self._out.write('label ' + label + '\n')
        self._out.flush()

    def write_goto(self, label):
        self._out.write('goto ' + label + '\n')
        self._out.flush()

    def write_if(self, label):
        self._out.write('if-goto ' + label + '\n')
        self._out.flush()

    def write_func_call(self, name, nArgs):
        self._out.write('call ' + name + ' ' + str(nArgs) + '\n')
        self._out.flush()

    def write_func(self, name, nArgs):
        self._out.write('function ' + name + ' ' + str(nArgs) + '\n')
        self._out.flush()

    def write_return(self):
        self._out.write('return\n')
        self._out.flush()
