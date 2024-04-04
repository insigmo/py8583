class ParseError(Exception):
    def __init__(self, value):
        self.str = value

    def __str__(self):
        return repr(self.str)


class SpecError(Exception):
    def __init__(self, value):
        self.str = value

    def __str__(self):
        return repr(self.str)


class BuildError(Exception):
    def __init__(self, value):
        self.str = value

    def __str__(self):
        return repr(self.str)
