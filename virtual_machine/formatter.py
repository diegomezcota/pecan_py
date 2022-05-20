class Formatter:
    def __init__(self):
        ...
    
    def cast(self, value, type):
        if type == 'int':
            return int(value)
        if type == 'float':
            return float(value)
        if type == 'bool':
            if value == 'true':
                return True
            return False
        if type == 'string':
            return value
        
        
fm = Formatter()
print(fm.cast('true', 'bool'))