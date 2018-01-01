GET = 0
INC = 1
RST = 2


class SymbolTable:
    def __init__(self):
        self._class_symbols = {}
        self._subs = {}
        self._counter = {}
        self._current_scope = {}

    def update_count(self, kind, command=0):
        count = 0

        if kind not in self._counter:
            self._counter[kind] = 0

        if command == GET:
            return self._counter[kind]
        elif command == INC:
            count = self._counter[kind]
            self._counter[kind] += 1
        elif command == RST:
            self._counter[kind] = 0

        return count

    def new_sub(self, name):
        self._subs[name] = {}
        for t in ['var', 'if', 'while', 'arg']:
            self.update_count(t, RST)

    def new_id(self, kind, type, name):
        data = (type, kind, self.update_count(kind, INC))

        if kind in ['static', 'field']:
            self._class_symbols[name] = data
        elif kind in ['var', 'arg']:
            self._current_scope[name] = data

    def var_count(self, kind):
        return self._counter.get(kind, 0)

    def get_kind(self, name):
        return self._class_symbols.get(name,
                                       self._current_scope.get(name, None))[1]

    def get_type(self, name):
        return self._class_symbols.get(name,
                                       self._current_scope.get(name, None))[0]

    def get_index(self, name):
        return self._class_symbols.get(name,
                                       self._current_scope.get(name, None))[2]

    def set_scope(self, name):
        if name == 'global':
            self._current_scope = self._class_symbols
        else:
            self._current_scope = self._subs[name]

    def is_in_current_scope(self, name):
        return name in self._current_scope

    def is_defined(self, name):
        return name in self._current_scope or \
               name in self._class_symbols
