# Mariana Martinez Celis Gonzalez
# Diego Gomez Cota
# ovejota_manager.py
# Estructura para manejar el archivo ovejota para pasar los valores correspondientes de compilacion a ejecucion
import json


class OvejotaManager:
    def __init__(self):

        # se lee el archivo ovejota, salida de compilacion
        with open('ovejota.json') as json_file:
            self.ovejota = json.load(json_file)

        if 'error' in self.ovejota.keys():
            raise Exception(self.ovejota['error'])

        # se crean los diccionarios pertinentes de cada parte del ovejota
        self.function_directory = self.ovejota['function_directory']

        self.quads = self.ovejota['quads']

        self.constants_summary = self.ovejota['constants_summary']

        self.constants_table = self.ovejota['constants_table']
        
        self.global_objects_constructors_start_quads = self.ovejota['global_objects_constructors_start_quads']

    # funcion para obtener el workspace de variables de un scope interno
    # entradas: scope general, scope interno
    # salida: workspace de variables del scope interior
    def get_variable_workspace(self, general_name, internal_name):
        return self.function_directory[general_name][internal_name]['workspace']['variables_workspace']

    # funcion para obtener el workspace de temporales de un scope interno
    # entradas: scope general, scope interno
    # salida: workspace de temporales del scope interior
    def get_temps_workspace(self, general_name, internal_name):
        return self.function_directory[general_name][internal_name]['workspace']['temps_workspace']

    # funcion para obtener el resumen de constantes
    def get_constants_summary(self):
        return self.constants_summary

    # funcion para obtener la tabla de constantes
    def get_constants_table(self):
        return self.constants_table

    # funcion para obtener los cuádruplos de inicio de los constructores de objetos globales
    def get_global_objects_constructors_start_quads(self):
        return self.global_objects_constructors_start_quads 

#om = OvejotaManager()
#print(json.dumps(om.function_directory, indent=2))
#print(json.dumps(om.quads, indent=2))
