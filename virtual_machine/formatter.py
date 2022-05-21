class Formatter:
    def __init__(self):
        ...

    def cast(self, value, type):
        if type == 'int':
            return int(value)
        if type == 'float':
            return float(value)
        if type == 'bool':
            return value
        if type == 'string':
            return value
