class FunctionDirectory:
    def __init__(self):
        self.table = {}
        
    def init_global_scope(self):
        self.table = {}
        self.table["global"] = {
            "function_type": "void", "vars_table": {}}

    def add_global_variable(self, declaration):
        _, var_type, var_data_type, var_name = declaration
        self.table['global']['vars_table'][var_name] = {
            'var_data_type': var_data_type, 'var_type': var_type}

    def add_function_with_variables(self, function_variables, function_name, function_type):
        # add to function directory
        self.table[function_name] = {
            "function_type": function_type, "vars_table": {}}
        # add vars to function directory
        for variable in function_variables:
            _, var_type, var_data_type, var_name = variable
            self.table[function_name]['vars_table'][var_name] = {
                'var_data_type': var_data_type, 'var_type': var_type}
