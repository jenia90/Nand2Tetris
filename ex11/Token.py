class Token:
    def __init__(self, value, kind):
        self._kind = kind
        self._val = value
        self.__clean_value()

    def __clean_value(self):
        if self._kind == "stringConstant":
            self._val = self._val[1:-1]

    def get_kind(self):
        return self._kind

    def get_value(self):
        return self._val

    def __repr__(self):
        return self._val
