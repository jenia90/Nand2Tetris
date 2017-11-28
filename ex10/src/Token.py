class Token:
    def __init__(self, value, kind):
        self._val = value
        self._kind = kind
        self._symbol_conversion = {'<': '&lt;', '>': '&gt;', '"': '&quot;', '&': '&amp;'}

    def __repr__(self):
        if self._kind == 'symbol' and self._val in self._symbol_conversion:
            return self._symbol_conversion[self._val], self._kind
        return "{},{}"
