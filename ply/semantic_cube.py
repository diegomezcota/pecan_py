class SemanticCube:
    # TODO: Add a get_result_type() function that handles tuples that don't exist and returns None
    def __init__(self):
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
        }

    def is_type_match(self, lo_type, ro_type, operator):
        if (lo_type, ro_type, operator) in self.table:
            return self.table[(lo_type, ro_type, operator)]
        return None
