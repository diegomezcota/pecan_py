import json


class OvejotaManager:
    def __init__(self):

        with open('ovejota.json') as json_file:
            self.ovejota = json.load(json_file)
        
        if 'error' in self.ovejota.keys():
            raise Exception(self.ovejota['error'])

        self.function_directory = self.ovejota['function_directory']

        self.quads = self.ovejota['quads']

        self.constants_summary = self.ovejota['constants_summary']

        self.constants_table = self.ovejota['constants_table']

    def get_variable_workspace(self, general_name, internal_name):
        return self.function_directory[general_name][internal_name]['workspace']['variables_workspace']

    def get_temps_workspace(self, general_name, internal_name):
        return self.function_directory[general_name][internal_name]['workspace']['temps_workspace']

    def get_constants_summary(self):
        return self.constants_summary

    def get_constants_table(self):
        return self.constants_table


#om = OvejotaManager()
#print(json.dumps(om.function_directory, indent=2))
#print(json.dumps(om.quads, indent=2))
