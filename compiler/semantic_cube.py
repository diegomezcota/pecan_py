# Mariana Martinez Celis Gonzalez
# Diego Gomez Cota
# semantic_cube.py
# Estructura para guardar y manejar cubo semantico
class SemanticCube:
    def __init__(self):

        # tabla con valores de cuadro semantico con la siguiente estructura:
        # (tipo de dato operando izquierdo, tipo de dato de operando derecho, operador): tipo de dato resultante
        self.table = {
            ('int', 'int', '*'): 'int',
            ('int', 'int', '/'): 'float',
            ('int', 'int', '+'): 'int',
            ('int', 'int', '-'): 'int',
            ('int', 'int', '>'): 'bool',
            ('int', 'int', '<'): 'bool',
            ('int', 'int', '=='): 'bool',
            ('int', 'int', '!='): 'bool',
            ('int', 'int', '&&'): 'bool',
            ('int', 'int', '||'): 'bool',
            ('int', 'float', '*'): 'float',
            ('int', 'float', '/'): 'float',
            ('int', 'float', '+'): 'float',
            ('int', 'float', '-'): 'float',
            ('int', 'float', '>'): 'bool',
            ('int', 'float', '<'): 'bool',
            ('int', 'float', '=='): 'bool',
            ('int', 'float', '!='): 'bool',
            ('int', 'float', '&&'): 'bool',
            ('int', 'float', '||'): 'bool',
            ('int', 'bool', '&&'): 'bool',
            ('int', 'bool', '||'): 'bool',
            ('float', 'int', '*'): 'float',
            ('float', 'int', '/'): 'float',
            ('float', 'int', '+'): 'float',
            ('float', 'int', '-'): 'float',
            ('float', 'int', '>'): 'bool',
            ('float', 'int', '<'): 'bool',
            ('float', 'int', '=='): 'bool',
            ('float', 'int', '!='): 'bool',
            ('float', 'int', '&&'): 'bool',
            ('float', 'int', '||'): 'bool',
            ('float', 'float', '*'): 'float',
            ('float', 'float', '/'): 'float',
            ('float', 'float', '+'): 'float',
            ('float', 'float', '-'): 'float',
            ('float', 'float', '>'): 'bool',
            ('float', 'float', '<'): 'bool',
            ('float', 'float', '=='): 'bool',
            ('float', 'float', '!='): 'bool',
            ('float', 'float', '&&'): 'bool',
            ('float', 'float', '||'): 'bool',
            ('float', 'bool', '&&'): 'bool',
            ('float', 'bool', '||'): 'bool',
            ('bool', 'int', '&&'): 'bool',
            ('bool', 'int', '||'): 'bool',
            ('bool', 'float', '&&'): 'bool',
            ('bool', 'float', '||'): 'bool',
            ('bool', 'bool', '=='): 'bool',
            ('bool', 'bool', '!='): 'bool',
            ('bool', 'bool', '&&'): 'bool',
            ('bool', 'bool', '||'): 'bool',
            ('int', 'int', '='): 'int',
            ('float', 'float', '='): 'float',
            ('string', 'string', '='): 'string',
            ('bool', 'bool', '='): 'bool'
        }

    # funcion para verificar si los operandos con cierto operador son validos en el lenguaje
    # en otras palabras 'si baila mi hija con el señor'
    # entradas: tipo de dato del operando izquierdo, tipo de dato del operando derecho y operador
    # salida: el tipo de dato del valor resultante en caso de ser una combinacion valida y None en caso de que no
    def is_type_match(self, lo_type, ro_type, operator):
        if (lo_type, ro_type, operator) in self.table:
            return self.table[(lo_type, ro_type, operator)]
        return None
