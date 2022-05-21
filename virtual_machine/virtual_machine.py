from memory import GlobalMemory
from memory import LocalMemory
from ovejota_manager import OvejotaManager
from formatter import Formatter

ovejota_manager = OvejotaManager()
formatter = Formatter()

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
memory_stack = []

def get_type_and_value_global(address):
    type, value = global_memory.get_value_from_address(address)
    if not type:
        print('not found')
        return (None, None)
    return (type, value)

def get_type_and_value(local_memory, address):
    type, value = local_memory.get_value_from_address(address)
    if not type:
        return get_type_and_value_global(address)
    return (type, value)

def get_memory_scope(address):
    if address >= 8000 and address < 24000:
        return 'local_memory'
    return 'global_memory'

def get_binary_operands(local_memory, lo_address, ro_address):
    lo_type, lo_value = get_type_and_value(local_memory, lo_address)
    if not lo_type:
        raise Exception('Left operator address was not found')
    left_operand = formatter.cast(lo_value, lo_type)
    ro_type, ro_value = get_type_and_value(local_memory, ro_address)
    if not ro_type:
        raise Exception('Right operator address was not found')
    right_operand = formatter.cast(ro_value, ro_type)
    return (left_operand, right_operand)

def set_value_in_memory(address, local_memory, value):
    # get memory scope of address to assign
    memory_scope = get_memory_scope(address)
    if memory_scope == 'local_memory':
        local_memory.set_value_in_address(address, value)
    else:
        global_memory.set_value_in_address(address, value)
    # return local memory since it is a copy and should be reassigned
    return local_memory 

while (instruction_pointer < len(quads)):
    current_quad = quads[instruction_pointer]
    if current_quad[0] == 'GOTOMAIN':
        main_vw = ovejota_manager.get_variable_workspace('#global', 'main')
        main_tw = ovejota_manager.get_temps_workspace('#global', 'main')
        # create tuples with sizes
        main_variable_workspace = (main_vw['int'], main_vw['float'], main_vw['bool'], main_vw['string'])
        main_temps_workspace = (main_tw['int'], main_tw['float'], main_tw['bool'], main_tw['string'])
        main_memory = LocalMemory(main_variable_workspace, main_temps_workspace)
        memory_stack.append(main_memory)
        instruction_pointer = current_quad[3]
        continue
    elif current_quad[0] == '=':
        to_assign_type, to_assign_value = get_type_and_value(memory_stack[-1], current_quad[1])
        to_assign_value = formatter.cast(to_assign_value, to_assign_type)
        memory_stack[-1] = set_value_in_memory(current_quad[3], memory_stack[-1], to_assign_value)
    elif current_quad[0] == '+':
        left_operand, right_operand = get_binary_operands(memory_stack[-1], current_quad[1], current_quad[2])
        sum_result = left_operand + right_operand
        memory_stack[-1] = set_value_in_memory(current_quad[3], memory_stack[-1], sum_result)
    instruction_pointer += 1

print(quads)
print(memory_stack[-1].table)
print(global_memory.table)