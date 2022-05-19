from memory import GlobalMemory
from memory import LocalMemory
from ovejota_manager import OvejotaManager

ovejota_manager = OvejotaManager()

gvw = ovejota_manager.get_variable_workspace('#global', '#global')
global_variable_workspace = (
    gvw['int'], gvw['float'], gvw['bool'], gvw['string'])
global_memory = GlobalMemory(global_variable_workspace)

quads = ovejota_manager.quads

instruction_pointer = 0

while (instruction_pointer < len(quads)):
    current_quad = quads[instruction_pointer]
