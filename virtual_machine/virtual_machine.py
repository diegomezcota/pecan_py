from memory import GlobalMemory
from memory import LocalMemory
from ovejota_manager import OvejotaManager

ovejota_manager = OvejotaManager()

gvw = ovejota_manager.get_variable_workspace('#global', '#global')
cw = ovejota_manager.get_constants_table()
global_variable_workspace = (
    gvw['int'], gvw['float'], gvw['bool'], gvw['string'])
constants_workspace = (cw['int'], cw['float'], cw['bool'], cw['string'])
global_memory = GlobalMemory(global_variable_workspace, constants_workspace)

quads = ovejota_manager.quads

instruction_pointer = 0

while (instruction_pointer < len(quads)):
    current_quad = quads[instruction_pointer]
