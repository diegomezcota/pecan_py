# TODO: Mandar tabla de constantes thru ovejota

class LocalMemory:
    def __init__(self, vars_sizes, temps_sizes):

        vars_int, vars_float, vars_bool, vars_string = vars_sizes

        temps_int, temps_float, temps_bool, temps_string = temps_sizes

        self.table = {
            'vars': {'int': [None] * vars_int, 'float': [None] * vars_float, 'bool': [None] * vars_bool, 'string': [None] * vars_string},
            'temps': {'int': [None] * temps_int, 'float': [None] * temps_float, 'bool': [None] * temps_bool, 'string': [None] * temps_string}
        }

    def get_scope_key(self, address):
        if (address >= 8000 and address < 16000):
            return 'locals'
        elif (address >= 16000 and address < 24000):
            return 'temps'
        else:
            return 'constants'

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

        print(index)

        self.table[table_scope][data_type][index] = value

    def get_value_from_address(self, address):

        table_scope, data_type, index = self.get_table_keys(address)

        return self.table[table_scope][data_type][index]


# gm = LocalMemory()
# gm.set_value_in_address(8004, 'tripsi')
# print(gm.table)


class GlobalMemory:
    def __init__(self, vars_sizes):

        vars_int, vars_float, vars_bool, vars_string = vars_sizes

        self.table = {
            'vars': {'int': [None] * vars_int, 'float': [None] * vars_float, 'bool': [None] * vars_bool, 'string': [None] * vars_string}
        }

    def get_table_keys(self, address):

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

    def set_value_in_address(self, address, value):

        data_type, index = self.get_table_keys(address)

        self.table['vars'][data_type][index] = value

    def get_value_from_address(self, address):

        data_type, index = self.get_table_keys(address)

        return self.table['vars'][data_type][index]


gm = GlobalMemory()
gm.set_value_in_address(2003, 3.14)
print(gm.table)