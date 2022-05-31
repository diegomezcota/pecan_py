# Mariana Martinez Celis Gonzalez
# Diego Gomez Cota
# formatter.py
# Estructura para manejar el formateo de tipos de datos entre PecanPy y Python
class Formatter:
    def __init__(self):
        ...

    # funcion para castear tipos de datos entre PecanPy y Python
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
