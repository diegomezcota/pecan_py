# Mariana Martinez Celis Gonzalez
# Diego Gomez Cota
# constants.py
# Estructura para manejar la tabla de constantes
class Constants:

    def __init__(self):

        # Tabla seccionada por los tipos de datos int, float, bool, string
        # cada seccion tiene un diccionario con las constantes y su direccion virtual
        self.table = {'int': {}, 'float': {}, 'bool': {}, 'string': {}}

    # funcion para agregar una constante a la tabla de constantes
    # entradas: tipo de dato de la constante, su direccion virtual y su valor
    def add_constant(self, type, virtual_address, constant):
        self.table[type][constant] = virtual_address

    # funcion para verificar si una constante ya se encuentra en la tabla
    # entradas: tipo de dato de la constante y su valor
    # salidas: valor booleano de acuerdo a la existencia de la variable a buscar en la tabla
    def has_constant(self, type, constant):
        return constant in self.table[type].keys()

    # funcion para obtener la direccion virtual de alguna constante
    # entradas: tipo de dato de la constante y su valor
    # salida: su direccion virtual asignada
    def get_constant_address(self, type, constant):
        return self.table[type][constant]
