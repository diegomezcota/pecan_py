class FunctionDirectory:
    def __init__(self):
        self.table = {}
        
    # TODO: Change global to 0global, this doesn't solve that a function can be named global, but it's okay since it is not
    # TODO: Add to control de cambios parameter addition to vars table of each declared function
#    class_name	-> #global 		    -> vars_table
        # 		-> function_name 	-> vars_table
        # 		-> constructor	    -> vars_table

#   '#global'	-> #global		    -> vars_table
        # 		-> function_name 	-> vars_table
        # 		-> main		        -> vars_table
    # a reserved word
    def init_global_scope(self):
        self.table = {}
        self.table["global"] = {
            "function_type": "void", "vars_table": {}}

    def add_global_variable(self, declaration):
        _, var_type, var_data_type, var_name = declaration
        # TODO: Check that global variable is not already declared
        self.table['global']['vars_table'][var_name] = {
            'var_data_type': var_data_type, 'var_type': var_type}

    def add_function_with_variables(self, function_variables, function_name, function_type,  function_parameters=[]):
        # add to function directory
        self.table[function_name] = {
            "function_type": function_type, "vars_table": {}
        }
        # add params to function directory
        for param in function_parameters:
            var_type, var_data_type, var_name = param
            # TODO: Check that parameter is not already declared
            self.table[function_name]['vars_table'][var_name] = {
                'var_data_type' : var_data_type, 'var_type': var_type
            }
        # add vars to function directory
        for variable in function_variables:
            _, var_type, var_data_type, var_name = variable
            # TODO: Check that function variable is not already declared
            self.table[function_name]['vars_table'][var_name] = {
                'var_data_type': var_data_type, 'var_type': var_type
            }
