
class FunctionDirectory:
    def __init__(self):
        self.table = {}

    # TODO: Add checking for already declared function and not declared header, using has_been_implented flag
#    class_name	-> #global 		    -> vars_table
        # 		-> function_name 	-> vars_table
        # 		-> constructor	    -> vars_table

#   '#global'	-> #global		    -> vars_table
        # 		-> function_name 	-> vars_table
        # 		-> main		        -> vars_table
    def add_general_scope(self, name):
        if name in self.table.keys():
            raise GeneralScopeAlreadyDeclared(
                "General scope of " + name + " has already been declared.")
        else:
            self.table[name] = {}

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

    def get_nth_param_type(self, general_name, internal_name, n):
        # Raise error if n is bigger than array size
        param_signature_arr = self.table[general_name][internal_name]['param_signature']
        if n >= len(param_signature_arr):
            error_msg = "Sending too many parameters for function '" + internal_name + \
                "' when " + str(len(param_signature_arr)) + " are expected."
            raise FunctionParamLengthMismatch(error_msg)
        else:
            return param_signature_arr[n]

    def get_param_signature_length(self, general_name, internal_name):
        return len(self.table[general_name][internal_name]['param_signature'])

    def get_function_start_quad(self, general_name, internal_name):
        return self.table[general_name][internal_name]['start_quad']

    def get_function_type(self, general_name, internal_name):
        return self.table[general_name][internal_name]['function_type']

    def get_function_virtual_address(self, general_name, internal_name, function_name):
        return self.table[general_name][internal_name]['vars_table'][function_name]['var_virtual_address']

    def get_variable_virtual_address(self, general_name, internal_name, var_name):
        return self.table[general_name][internal_name]['vars_table'][var_name]['var_virtual_address']

    def get_variable_data_type(self, general_name, internal_name, var_name):
        return self.table[general_name][internal_name]['vars_table'][var_name]['var_data_type']

    def get_group_size(self, general_name, internal_name, var_name):
        return self.table[general_name][internal_name]['vars_table'][var_name]['group_size']

    def get_group_dimensions(self, general_name, internal_name, var_name):
        if 'dim_list' in self.table[general_name][internal_name]['vars_table'][var_name].keys():
            return len(self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'])
        else:
            return 0

    def get_m_dim(self, general_name, internal_name, var_name, dim):
        return self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'][dim-1]['m']

    def set_temps_workspace(self, general_name, internal_name, temps_workspace):
        self.table[general_name][internal_name]['workspace']['temps_workspace'] = temps_workspace

    def set_function_type(self, general_name, internal_name, type):
        self.table[general_name][internal_name]['function_type'] = type

    def set_start_quad(self, general_name, internal_name, quad_id):
        self.table[general_name][internal_name]['start_quad'] = quad_id

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

    def add_to_param_signature(self, general_name, internal_name, parameter_type):
        self.table[general_name][internal_name]['param_signature'].append(
            parameter_type)

    def add_dim1_list(self, general_name, internal_name, var_name):
        self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'] = [{
            'dim': 1, 'size': None}]
        self.table[general_name][internal_name]['vars_table'][var_name]['r'] = 1

    def add_dim2_list(self, general_name, internal_name, var_name):
        self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'].append({
            'dim': 2, 'size': None})

    def add_dim_size_and_update_r(self, general_name, internal_name, var_name, index, size):
        r = self.table[general_name][internal_name]['vars_table'][var_name]['r']
        self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'][index]['size'] = size
        self.table[general_name][internal_name]['vars_table'][var_name]['r'] = r * size

    def has_general_scope(self, name):
        return (name in self.table.keys())

    def has_internal_scope(self, general_name, internal_name):
        return (internal_name in self.table[general_name].keys())

    def has_variable(self, general_name, internal_name, var_name):
        return (var_name in self.table[general_name][internal_name]['vars_table'].keys())

    def generate_variable_workspace(self, general_name, internal_name):
        variable_workspace = {"int": 0, "float": 0, "string": 0, "bool": 0}
        # ir por todo el var table y sumar cada tipo
        vars_table = self.table[general_name][internal_name]['vars_table']
        for _, var_dict in vars_table.items():
            if var_dict['var_type'] != 'group':
                variable_workspace[var_dict['var_data_type']] += 1
            else:
                variable_workspace[var_dict['var_data_type']] += var_dict['group_size']
        self.table[general_name][internal_name]['workspace']['variables_workspace'] = variable_workspace

    def generate_dim_ms(self, general_name, internal_name, var_name):
        size = self.table[general_name][internal_name]['vars_table'][var_name]['r']

        for dim in self.table[general_name][internal_name]['vars_table'][var_name]['dim_list']:
            r = self.table[general_name][internal_name]['vars_table'][var_name]['r']
            dim_size = dim['size']
            dim['m'] = r / dim_size
            self.table[general_name][internal_name]['vars_table'][var_name]['r'] = dim['m']

        self.table[general_name][internal_name]['vars_table'][var_name]['group_size'] = size

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
