# TODO: Mandar tabla de constantes thru ovejota
from formatter import Formatter


class LocalMemory:
    def __init__(self, vars_sizes, temps_sizes):

        vars_int, vars_float, vars_bool, vars_string = vars_sizes

        temps_int, temps_float, temps_bool, temps_string = temps_sizes

        self.table = {
            'vars': {'int': [0] * vars_int, 'float': [0.0] * vars_float, 'bool': [False] * vars_bool, 'string': [''] * vars_string},
            'temps': {'int': [0] * temps_int, 'float': [0.0] * temps_float, 'bool': [False] * temps_bool, 'string': [''] * temps_string}
        }

    def get_scope_key(self, address):
        if (address >= 8000 and address < 16000):
            return 'locals'
        elif (address >= 16000 and address < 24000):
            return 'temps'
        return None

    def get_data_type(self, address):
        if (address >= 0 and address < 2000):
            return ('int', 0)
        elif (address >= 2000 and address < 4000):
            return ('float', 2000)
        elif (address >= 4000 and address < 6000):
            return ('bool', 4000)
        else:
            return ('string', 6000)

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

    def set_value_in_address(self, address, value):

        table_scope, data_type, index = self.get_table_keys(address)

        if not table_scope:
            return None

        self.table[table_scope][data_type][index] = value

    def get_value_from_address(self, address):

        table_scope, data_type, index = self.get_table_keys(address)

        if not table_scope:
            return (None, None)

        return (data_type, self.table[table_scope][data_type][index])


# gm = LocalMemory()
# gm.set_value_in_address(8004, 'tripsi')
# print(gm.table)


class GlobalMemory:
    def __init__(self, vars_sizes, consts_sizes, consts_table):

        vars_int, vars_float, vars_bool, vars_string = vars_sizes

        consts_int, consts_float, consts_bool, consts_string = consts_sizes

        self.fm = Formatter()

        self.table = {
            'vars': {'int': [0] * vars_int, 'float': [0.0] * vars_float, 'bool': [False] * vars_bool, 'string': [''] * vars_string},
            'constants': {'int': [0] * consts_int, 'float': [0.0] * consts_float, 'bool': [False] * consts_bool, 'string': [''] * consts_string}
        }

        for data_type, value_dict in consts_table.items():
            for value, address in value_dict.items():
                self.set_const_in_address(address, value)
        # print(self.table)

    def get_scope_key(self, address):
        if (address >= 0 and address < 8000):
            return 'vars'
        return 'constants'

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

    def get_table_keys(self, address):

        scope_key = self.get_scope_key(address)
        if scope_key == 'vars':
            address -= 0
        else:
            address -= 24000
        data_type, index = self.get_data_type(address)
        return (scope_key, data_type, index)

    def set_const_in_address(self, address, value):
        # We're using our own Formatter here due to constants loading are not defined in quads
        table_scope, data_type, index = self.get_table_keys(address)
        value = self.fm.cast(value, data_type)
        self.table[table_scope][data_type][index] = value

    def set_value_in_address(self, address, value):

        table_scope, data_type, index = self.get_table_keys(address)
        self.table[table_scope][data_type][index] = value

    def get_value_from_address(self, address):

        table_scope, data_type, index = self.get_table_keys(address)

        value = self.table[table_scope][data_type][index]

        return (data_type, value)
