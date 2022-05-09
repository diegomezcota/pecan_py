
class FunctionDirectory:
    def __init__(self):
        self.table = {}

    # TODO: Add parameter to vars table of each declared function
    # TODO: Add checking for already declared function and not declared header, using has_been_implented flag
#    class_name	-> #global 		    -> vars_table
        # 		-> function_name 	-> vars_table
        # 		-> constructor	    -> vars_table

#   '#global'	-> #global		    -> vars_table
        # 		-> function_name 	-> vars_table
        # 		-> main		        -> vars_table
    def add_general_scope(self, name):
        if name in self.table.keys():
            raise GeneralScopeAlreadyDeclared()
        else:
            self.table[name] = {}

    def add_internal_scope(self, general_name, name):
        if name in self.table[general_name].keys():
            raise FunctionAlreadyDeclared()
        else:
            self.table[general_name][name] = {
                "vars_table": {}
            }

    def set_function_type(self, general_name, internal_name, type):
        self.table[general_name][internal_name]['function_type'] = type

    def add_variable(self, general_name, internal_name, var_name, var_type, var_data_type, var_virtual_address):
        if var_name in self.table[general_name][internal_name]['vars_table'].keys():
            raise VariableAlreadyDeclared()
        else:
            self.table[general_name][internal_name]['vars_table'][var_name] = {
                'var_type': var_type,
                'var_data_type': var_data_type,
                'var_virtual_address': var_virtual_address
            }

    def has_general_scope(self, name):
        return (name in self.table.keys())

    def has_internal_scope(self, general_name, internal_name):
        return (internal_name in self.table[general_name].keys())

    def has_variable(self, general_name, internal_name, var_name):
        return (var_name in self.table[general_name][internal_name]['vars_table'].keys())


class GeneralScopeAlreadyDeclared(Exception):
    pass


class FunctionAlreadyDeclared(Exception):
    pass


class VariableAlreadyDeclared(Exception):
    pass
