# Mariana Martinez Celis Gonzalez
# Diego Gomez Cota
# function_directory.py
# Estructura para manejar el directorio de funciones
class FunctionDirectory:
    def __init__(self):

        # tabla que contiene el directorio de funciones con la siguiente estructura
        #       scope general       scope interno       tabla de variables
        #       class_name	        -> #global          -> vars_table
        # 		                    -> function_name 	-> vars_table
        # 		                    -> constructor	    -> vars_table
        #       '#global'	        -> #global          -> vars_table
        # 		                    -> function_name 	-> vars_table
        # 		                    -> main		        -> vars_table
        self.table = {}

    # funcion para agregar un scope general ya sea global o de los objetos creados
    # entradas: nombre del scope
    def add_general_scope(self, name):
        if name in self.table.keys():
            raise GeneralScopeAlreadyDeclared(
                "General scope of " + name + " has already been declared.")
        else:
            self.table[name] = {}

    # funcion para crear un scope interno dentro de uno general ya sea global de ese scope o de funciones
    # entradas: scope general, nombre del scope interno a crear
    def add_internal_scope(self, general_name, name):
        if name in self.table[general_name].keys():
            raise FunctionAlreadyDeclared(
                "Function '" + name + "' has already been declared")
        else:
            self.table[general_name][name] = {
                "vars_table": {},
                "param_signature": [],
                "workspace": {}
            }

    # funcion para obtener el parametro numero n de una funcion
    # entradas: scope general, scope interno, indice del parametro
    # salida: error o el parametro en el indice buscado
    def get_nth_param_type(self, general_name, internal_name, n):
        # Raise error if n is bigger than array size
        param_signature_arr = self.table[general_name][internal_name]['param_signature']
        if n >= len(param_signature_arr):
            error_msg = "Sending too many parameters for function '" + internal_name + \
                "' when " + str(len(param_signature_arr)) + " are expected."
            raise FunctionParamLengthMismatch(error_msg)
        else:
            return param_signature_arr[n]

    # funcion para obtener la cantidad de parametros en una funcion
    # entradas: scope general y scope interno (funcion)
    # salida: numero de parametros en ese scope interno (funcion)
    def get_param_signature_length(self, general_name, internal_name):
        return len(self.table[general_name][internal_name]['param_signature'])

    # function para obtener el indice del cuadruplo inicial para una funcion
    # entradas: scope general y scope interno (funcion)
    # salida: indice del primer cuadruplo de la funcion
    def get_function_start_quad(self, general_name, internal_name):
        return self.table[general_name][internal_name]['start_quad']

    # funcion para obtener el tipo de retorno de una funcion
    # entradas: scope general y scope interno (funcion)
    # salida: el tipo de dato del retorno de la funcion
    def get_function_type(self, general_name, internal_name):
        return self.table[general_name][internal_name]['function_type']

    # funcion para obtener la direccion virtual de una funcion
    # entradas: scope general, scope interno (funcion) y nombre de la funcion
    # salida: la direccion virtual de la funcion
    def get_function_virtual_address(self, general_name, internal_name, function_name):
        return self.table[general_name][internal_name]['vars_table'][function_name]['var_virtual_address']

    # funcion para obtener la direccion virtual de una variable
    # entradas: scope general, scope interno (funcion) y nombre de la variable
    # salida: la direccion virtual de la variable
    def get_variable_virtual_address(self, general_name, internal_name, var_name):
        return self.table[general_name][internal_name]['vars_table'][var_name]['var_virtual_address']

    # funcion para obtener el tipo de dato de una variable
    # entradas: scope general, scope interno (funcion) y nombre de la variable
    # salida: tipo de dato de la variable
    def get_variable_data_type(self, general_name, internal_name, var_name):
        return self.table[general_name][internal_name]['vars_table'][var_name]['var_data_type']

    # funcion para obtener el tamaño de una variable de tipo grupo (variable dimensionada)
    # entradas: scope general, scope interno (funcion) y nombre de la variable
    # salida: tamaño de la variable de tipo grupo
    def get_group_size(self, general_name, internal_name, var_name):
        return self.table[general_name][internal_name]['vars_table'][var_name]['group_size']

    # funcion para obtener el tamaño de una dimension dentro de una variable de tipo grupo
    # entradas: scope general, scope interno (funcion), nombre de la variable y dimension
    # salida: tamaño de la dimension de la variable tipo grupo
    def get_dim_size(self, general_name, internal_name, var_name, dim):
        return self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'][dim-1]['size']

    # funcion para obtener el numero de dimensiones de una variable
    # entradas: scope general, scope interno (funcion) y nombre de la variable
    # salidas: numero de dimensiones de la variable
    def get_group_dimensions(self, general_name, internal_name, var_name):
        if 'dim_list' in self.table[general_name][internal_name]['vars_table'][var_name].keys():
            return len(self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'])
        else:
            return 0

    # funcion para obtener la m de una dimension de una variable de tipo grupo
    # entradas: scope general, scope interno (funcion), nombre de la variable y dimension
    # salida: el valor de la m de la dimension
    def get_m_dim(self, general_name, internal_name, var_name, dim):
        return self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'][dim-1]['m']

    # funcion para agregar el workspace de temporales de un scope interno
    # entradas: scope general, scope interno (funcion) y workspace de temporales
    def set_temps_workspace(self, general_name, internal_name, temps_workspace):
        self.table[general_name][internal_name]['workspace']['temps_workspace'] = temps_workspace

    # fumcion para agregar el tipo de dato de una funcion (scope interno)
    # entradas: scope general, scope interno (funcion) y tipo de dato
    def set_function_type(self, general_name, internal_name, type):
        self.table[general_name][internal_name]['function_type'] = type

    # funcion para agregar el indice del cuadruplo inicial de una funcion
    # entradas: scope general, scope interno (funcion) e indice del cuadruplo inicial de la funcion
    def set_start_quad(self, general_name, internal_name, quad_id):
        self.table[general_name][internal_name]['start_quad'] = quad_id

    # funcion para agregar una variable con sus caracteristicas a la tabla de variables de un scope interno
    # entradas: scope general, scope interno (funcion), nombre de la variable, tipo de variable,
    # tipo de dato de la variable y direccion virtual de la variable
    def add_variable(self, general_name, internal_name, var_name, var_type, var_data_type, var_virtual_address):
        if var_name in self.table[general_name][internal_name]['vars_table'].keys():
            raise VariableAlreadyDeclared(
                "Variable named " + var_name + " has already been declared in the same scope.")
        else:
            self.table[general_name][internal_name]['vars_table'][var_name] = {
                'var_type': var_type,
                'var_data_type': var_data_type,
                'var_virtual_address': var_virtual_address
            }

    # funcion para modificar la firma de parametros de una funcion
    # entradas: scope general, scope interno (funcion) y tipo de dato del parameetro
    def add_to_param_signature(self, general_name, internal_name, parameter_type):
        self.table[general_name][internal_name]['param_signature'].append(
            parameter_type)

    # funcion para agregar caracteristicas de la primera dimension de una variable tipo grupo
    # entradas: scope general, scope interno (funcion) y nombre de la variable
    def add_dim1_list(self, general_name, internal_name, var_name):
        self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'] = [{
            'dim': 1, 'size': None}]
        self.table[general_name][internal_name]['vars_table'][var_name]['r'] = 1

    # funcion para agregar caracteristicas de la segunda dimension de una variable tipo grupo
    # entradas: scope general, scope interno (funcion) y nombre de la variable
    def add_dim2_list(self, general_name, internal_name, var_name):
        self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'].append({
            'dim': 2, 'size': None})

    # funcion para agregar el tamaño de una dimension y calcular la r de una variable de tipo grupo
    # entradas: scope general, scope interno (funcion), nombre de la variable, indice de la dimension y tamaño de la dimension
    def add_dim_size_and_update_r(self, general_name, internal_name, var_name, index, size):
        r = self.table[general_name][internal_name]['vars_table'][var_name]['r']
        self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'][index]['size'] = size
        self.table[general_name][internal_name]['vars_table'][var_name]['r'] = r * size

    # funcion para saber si se tiene un scope general con cierto nombre
    # entrada: nombre del scope general
    def has_general_scope(self, name):
        return (name in self.table.keys())

    # funcion para saber si se tiene un scope interno con cierto nombre en cierto scope general
    # entradas: nombre del scope general y nombre del scope interno
    def has_internal_scope(self, general_name, internal_name):
        return (internal_name in self.table[general_name].keys())

    # funcion para saber si se tiene una variable en cierto scope general e interno
    # entradas: scope general, scope interno (funcion) y nombre de la variable
    def has_variable(self, general_name, internal_name, var_name):
        return (var_name in self.table[general_name][internal_name]['vars_table'].keys())

    # funcion para generar el workspace de variables de un scope interno
    # entradas: nombre del scope general y nombre del scope interno
    def generate_variable_workspace(self, general_name, internal_name):
        variable_workspace = {"int": 0, "float": 0, "string": 0, "bool": 0}
        # ir por todo el var table y sumar cada tipo
        vars_table = self.table[general_name][internal_name]['vars_table']
        for _, var_dict in vars_table.items():
            if var_dict['var_type'] != 'group':
                variable_workspace[var_dict['var_data_type']] += 1
            else:
                variable_workspace[var_dict['var_data_type']
                                   ] += var_dict['group_size']
        self.table[general_name][internal_name]['workspace']['variables_workspace'] = variable_workspace

    # funcion para calcular y guardar la m de una dimension de una variable de tipo grupo
    # entradas: scope general, scope interno, nombre de la variable
    def generate_dim_ms(self, general_name, internal_name, var_name):
        size = self.table[general_name][internal_name]['vars_table'][var_name]['r']

        for dim in self.table[general_name][internal_name]['vars_table'][var_name]['dim_list']:
            r = self.table[general_name][internal_name]['vars_table'][var_name]['r']
            dim_size = dim['size']
            dim['m'] = r / dim_size
            self.table[general_name][internal_name]['vars_table'][var_name]['r'] = dim['m']

        self.table[general_name][internal_name]['vars_table'][var_name]['group_size'] = size

    # funcion para eliminar la tabla de variables de un scope interno
    # entradas: nombre de scope general y nombre de scope interno
    def delete_vars_table(self, general_name, internal_name):
        self.table[general_name][internal_name]['vars_table'] = {}


class GeneralScopeAlreadyDeclared(Exception):
    pass


class FunctionAlreadyDeclared(Exception):
    pass


class VariableAlreadyDeclared(Exception):
    pass


class FunctionParamLengthMismatch(Exception):
    ...
