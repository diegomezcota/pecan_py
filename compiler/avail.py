# Mariana Martinez Celis Gonzalez
# Diego Gomez Cota
# avail.py
# Estructura parar manejar las direcciones virtuales de memoria en compilacion
class Avail:
    def __init__(self):

        # Tabla con bloques para direcciones globales, locales, temporales y constantes
        # Cada bloque contiene sus respectivos bloques para int, float, bool, string
        # Cada uno de estos bloques se conforma por un arreglo con la siguiente estructura
        # [direccion actual por asignar, direccion inicial, direccion final]
        self.table = {
            'globals': {'int': [0, 0, 1999], 'float': [2000, 2000, 3999], 'bool': [4000, 4000, 5999], 'string': [6000, 6000, 7999]},
            'locals': {'int': [8000, 8000, 9999], 'float': [10000, 10000, 11999], 'bool': [12000, 12000, 13999], 'string': [14000, 14000, 15999]},
            'temps': {'int': [16000, 16000, 17999], 'float': [18000, 18000, 19999], 'bool': [20000, 20000, 21999], 'string': [22000, 22000, 23999]},
            'constants': {'int': [24000, 24000, 25999], 'float': [26000, 26000, 27999], 'bool': [28000, 28000, 29999], 'string': [30000, 30000, 31999]}
        }

    # funcion para pedir una nueva direccion
    # entradas: tipo de dato (int, float, bool, string) y bloque al que pertenece (globals, locals, temps, constants)
    # salida: la direccion asignada de acuerdo a los parametros anteriores
    def get_new_address(self, type, block):
        if self.table[block][type][0] > self.table[block][type][2]:
            raise Exception("Too many variables for type " + type)
        else:
            current_address = self.table[block][type][0]
            self.table[block][type][0] += 1
            return current_address

    # funcion para pedir cierta cantidad de direcciones
    # entradas: tipo de dato (int, float, bool, string), bloque al que pertenece (globals, locals, temps, constants) y cantidad de direcciones a pedir
    # salida: la primera direccion de este grupo de direcciones
    def get_group_addresses(self, type, block, size):
        if self.table[block][type][0] + size - 1 > self.table[block][type][2]:
            raise Exception("Too many variables for type " + type)
        else:
            current_address = self.table[block][type][0]
            self.table[block][type][0] += size
            return current_address

    # funcion para pedir una nueva direccion temporal
    # entradas: tipo de dato (int, float, bool, string)
    # salida: tupla con la direccion asignada y su tipo
    def get_new_temp(self, type):
        if self.table['temps'][type][0] == self.table['temps'][type][2]:
            raise Exception("Too many variables for type " + type)
        else:
            temp_tuple = (self.table['temps'][type][0], type)
            self.table['temps'][type][0] += 1
            return temp_tuple

    # funcion para pedir una nueva direccion global
    # entradas: tipo de dato (int, float, bool, string)
    # salida: tupla con la direccion asignada y su tipo
    def get_new_global(self, type):
        if self.table['globals'][type][0] == self.table['globals'][type][2]:
            raise Exception("Too many variables for type " + type)
        else:
            global_address = self.table['globals'][type][0]
            self.table['globals'][type][0] += 1
            return global_address

    # funcion para resetear contadores de direcciones locales y temporales
    # para poder reutilizarlas en scopes difererntes
    def reset_local_counters(self):
        # Reset local counters
        self.table['locals']['int'][0] = self.table['locals']['int'][1]
        self.table['locals']['float'][0] = self.table['locals']['float'][1]
        self.table['locals']['bool'][0] = self.table['locals']['bool'][1]
        self.table['locals']['string'][0] = self.table['locals']['string'][1]
        # Reset temporal local counters
        self.table['temps']['int'][0] = self.table['temps']['int'][1]
        self.table['temps']['float'][0] = self.table['temps']['float'][1]
        self.table['temps']['bool'][0] = self.table['temps']['bool'][1]
        self.table['temps']['string'][0] = self.table['temps']['string'][1]

    # funcion para obtener un resumen de la cantidad de direcciones virtuales asignadas por tipo en cierto bloque
    # bloque (globals, locals, temps, constants)
    # resumeen de contadores
    def get_counter_summary(self, block):
        type_counters = self.table[block]
        counter_summary = {data_type: dt_array[0] - dt_array[1]
                           for data_type, dt_array in type_counters.items()}
        return counter_summary
