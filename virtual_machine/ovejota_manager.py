import json


class OvejotaManager:
    def __init__(self):

        with open('../ovejota.json') as json_file:
            self.ovejota = json.load(json_file)

        self.function_directory = self.ovejota['function_directory']

        self.quads = self.ovejota['quads']

        self.constants = self.ovejota['constants']

    def get_variable_workspace(self, general_name, internal_name):
        return self.function_directory[general_name][internal_name]['workspace']['variables_workspace']

    def get_temps_workspace(self, general_name, internal_name):
        return self.function_directory[general_name][internal_name]['workspace']['temps_workspace']

    def get_constants_table(self):
        return self.constants


#om = OvejotaManager()
#print(json.dumps(om.function_directory, indent=2))
#print(json.dumps(om.quads, indent=2))
