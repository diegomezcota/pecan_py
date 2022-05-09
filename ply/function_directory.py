class FunctionDirectory:
    def __init__(self):
        self.table = {}

    # TODO: Change global to 0global, this doesn't solve that a function can be named global, but it's okay since it is not
    # TODO: Add parameter to vars table of each declared function
    # TODO: Add checking for already declared function and not declared header, using has_been_implented flag
#    class_name	-> #global 		    -> vars_table
        # 		-> function_name 	-> vars_table
        # 		-> constructor	    -> vars_table

#   '#global'	-> #global		    -> vars_table
        # 		-> function_name 	-> vars_table
        # 		-> main		        -> vars_table
    # a reserved word
    def add_general_scope(self, name):
        # TODO: checar chekeo
        self.table[name] = {}

    def add_internal_scope(self, general_name, name):
        # TODO: checar chekeo
        self.table[general_name][name] = {
            "vars_table": {}
        }

    def set_function_type(self, general_name, internal_name, type):
        # TODO: checar chekeo
        self.table[general_name][internal_name]['function_type'] = type

    def add_variable(self, general_name, internal_name, var_name, var_type, var_data_type, var_virtual_address):
        # TODO: checar chekeo
        self.table[general_name][internal_name]['vars_table'][var_name] = {
            'var_type': var_type,
            'var_data_type': var_data_type,
            'var_virtual_address': var_virtual_address
        }
