class Formatter:
    def __init__(self):
        ...

    def cast(self, value, type):
        if type == 'int':
            return int(value)
        if type == 'float':
            return float(value)
        if type == 'bool':
            # custom check for string instance of casting
            if isinstance(value, str):
                return value == 'true'
            return value
        if type == 'string':
            return value
