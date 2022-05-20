from memory import GlobalMemory
from memory import LocalMemory
from ovejota_manager import OvejotaManager

ovejota_manager = OvejotaManager()

gvw = ovejota_manager.get_variable_workspace('#global', '#global')
cs = ovejota_manager.get_constants_summary()
constants_table = ovejota_manager.get_constants_table()
global_variable_workspace = (
    gvw['int'], gvw['float'], gvw['bool'], gvw['string'])
constants_workspace = (cs['int'], cs['float'], cs['bool'], cs['string'])
global_memory = GlobalMemory(
    global_variable_workspace, constants_workspace, constants_table)

quads = ovejota_manager.quads

instruction_pointer = 0

while (instruction_pointer < len(quads)):
    current_quad = quads[instruction_pointer]
    instruction_pointer += 1
