# Mariana Martinez Celis Gonzalez
# Diego Gomez Cota
# Memory.py
# Estructura para el manejo de memorias en ejecucion de manera local y global

from formatter import Formatter

# Estructura para memorias locales


class LocalMemory:

    # se inicializa con el tamaño de variables de cada tipo y sus temporales necesarias
    def __init__(self, vars_sizes, temps_sizes):

        vars_int, vars_float, vars_bool, vars_string = vars_sizes

        temps_int, temps_float, temps_bool, temps_string = temps_sizes

        # tabla que guarda los valores en cada tipo de dato correspondiente
        self.table = {
            'vars': {'int': [0] * vars_int, 'float': [0.0] * vars_float, 'bool': [False] * vars_bool, 'string': [''] * vars_string},
            'temps': {'int': [0] * temps_int, 'float': [0.0] * temps_float, 'bool': [False] * temps_bool, 'string': [''] * temps_string}
        }
        
        # Para distinguir si es un metodo de una clase
        self.object = None

    # funcion para obtener la llave del tipo de dato dada una direccion virtual
    # entrada: direccion virtual
    # salidas: la llave correspondiente sea locals, temps o None
    def get_scope_key(self, address):
        if (address >= 8000 and address < 16000):
            return 'locals'
        elif (address >= 16000 and address < 24000):
            return 'temps'
        return None

    # funcion para obtener el tipo de dato de una variable dada una direccion virtual
    # entrada: direccion
    # salidas: tupla de tipo de dato y su limite inferior correspondiente
    def get_data_type(self, address):
        if (address >= 0 and address < 2000):
            return ('int', 0)
        elif (address >= 2000 and address < 4000):
            return ('float', 2000)
        elif (address >= 4000 and address < 6000):
            return ('bool', 4000)
        else:
            return ('string', 6000)

    # funcion para obtener las llaves del diccionario dada una direccion virtual
    # entrada: direccion virtual
    # salidas: tupla con scope de la tabla, tipo de dato y la direccion de la memoria donde se encuentra el valor
    def get_table_keys(self, address):

        scope_key = self.get_scope_key(address)
        if not scope_key:
            return (None, None, None)
        table_scope = None
        data_type = None

        if scope_key == 'temps':
            table_scope = 'temps'
            address -= 16000
        else:
            table_scope = 'vars'
            address -= 8000

        data_type, type_offset = self.get_data_type(address)

        return (table_scope, data_type, address-type_offset)
    
    #TODO: Documentar
    def set_object_characteristics(self, object_scope, object_base_addresses):
        self.object = {
            'object_scope' : object_scope,
            'object_base_addresses' : object_base_addresses  
        }

    # funcion para agregar un valor dentro de una direccion virtual
    # entradas: direccion virtual y valor a agregar
    # salida: None si la direccion virtual se encuentra fuera del scope
    def set_value_in_address(self, address, value):

        table_scope, data_type, index = self.get_table_keys(address)

        if not table_scope:
            return None

        self.table[table_scope][data_type][index] = value

    # funcion para obtener el valor dentro de una direccion virtual
    # entrada: direccion virtual
    # salida tupla de tipo de dato y valor o None en caso de que se encuentre fuera del scope
    def get_value_from_address(self, address):

        table_scope, data_type, index = self.get_table_keys(address)

        if not table_scope:
            return (None, None)

        return (data_type, self.table[table_scope][data_type][index])


# gm = LocalMemory()
# gm.set_value_in_address(8004, 'tripsi')
# print(gm.table)


# Estructura para memorias globales
class GlobalMemory:

    # se inicializa con el tamaño de variables de cada tipo y sus constantes necesarias
    def __init__(self, vars_sizes, consts_sizes, consts_table):

        vars_int, vars_float, vars_bool, vars_string = vars_sizes

        consts_int, consts_float, consts_bool, consts_string = consts_sizes

        self.fm = Formatter()

        # tabla que guarda los valores en cada tipo de dato correspondiente
        self.table = {
            'vars': {'int': [0] * vars_int, 'float': [0.0] * vars_float, 'bool': [False] * vars_bool, 'string': [''] * vars_string},
            'constants': {'int': [0] * consts_int, 'float': [0.0] * consts_float, 'bool': [False] * consts_bool, 'string': [''] * consts_string}
        }

        for data_type, value_dict in consts_table.items():
            for value, address in value_dict.items():
                self.set_const_in_address(address, value)

    # funcion para obtener la llave del tipo de dato dada una direccion virtual
    # entrada: direccion virtual
    # salidas: la llave correspondiente sea vars, constants o None
    def get_scope_key(self, address):
        if (address >= 0 and address < 8000):
            return 'vars'
        return 'constants'

    # funcion para obtener el tipo de dato de una variable dada una direccion virtual
    # entrada: direccion
    # salidas: tupla de tipo de dato y su limite inferior correspondiente
    def get_data_type(self, address):
        data_type = None

        if address >= 0 and address < 2000:
            data_type = 'int'
            address -= 0
        elif address >= 2000 and address < 4000:
            data_type = 'float'
            address -= 2000
        elif address >= 4000 and address < 6000:
            data_type = 'bool'
            address -= 4000
        else:
            data_type = 'string'
            address -= 6000
        return (data_type, address)

    # funcion para obtener las llaves del diccionario dada una direccion virtual
    # entrada: direccion virtual
    # salidas: tupla con scope de la tabla, tipo de dato y la direccion de la memoria donde se encuentra el valor
    def get_table_keys(self, address):

        scope_key = self.get_scope_key(address)
        if scope_key == 'vars':
            address -= 0
        else:
            address -= 24000
        data_type, index = self.get_data_type(address)
        return (scope_key, data_type, index)

    # funcion para agregar una constante en cierta direccion
    # entradas: direccion virtual y valor de la constante a agregar
    def set_const_in_address(self, address, value):
        # We're using our own Formatter here due to constants loading are not defined in quads
        table_scope, data_type, index = self.get_table_keys(address)
        value = self.fm.cast(value, data_type)
        self.table[table_scope][data_type][index] = value

    # funcion para agregar un valor dentro de una direccion virtual
    # entradas: direccion virtual y valor a agregar
    # salida: None si la direccion virtual se encuentra fuera del scope
    def set_value_in_address(self, address, value):

        table_scope, data_type, index = self.get_table_keys(address)
        self.table[table_scope][data_type][index] = value

    # funcion para obtener el valor dentro de una direccion virtual
    # entrada: direccion virtual
    # salida tupla de tipo de dato y valor o None en caso de que se encuentre fuera del scope
    def get_value_from_address(self, address):

        table_scope, data_type, index = self.get_table_keys(address)

        value = self.table[table_scope][data_type][index]

        return (data_type, value)
