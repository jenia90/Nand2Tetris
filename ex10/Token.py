class Token:
    def __init__(self, value, kind):
        self._symbol_conversion = {'<': '&lt;', '>': '&gt;', '"': '&quot;', '&': '&amp;'}
        self._kind = kind
        self._val = self._symbol_conversion.get(value, value)
        self.__clean_value()

    def __clean_value(self):
        if self._kind == "stringConstant":
            self._val = self._val[1:-1]
            for s in self._symbol_conversion.keys():
                str(self._val).replace(s, self._symbol_conversion[s])

    def getKind(self):
        return self._kind

    def getValue(self):
        return self._val

    def __repr__(self):
        return "<%s> %s </%s>" % (self._kind, self._val, self._kind)
