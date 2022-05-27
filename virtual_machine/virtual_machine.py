from Memory import GlobalMemory
from Memory import LocalMemory
from ovejota_manager import OvejotaManager
from formatter import Formatter

# try to read ovejota for successful compilation
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


def clean_quad_addresses(current_quad, memory):
    for i, element in enumerate(current_quad):
        if element is not None and str(element)[0] == '&':
            element = element[1:]
            element = int(element)
            _, new_address = get_type_and_value(memory, element)
            current_quad[i] = new_address
    return current_quad


print('--------------------START OF EXECUTION-----------------------------')

while (instruction_pointer < len(quads)):
    current_quad = quads[instruction_pointer].copy()
    if memory_stack:
        current_quad = clean_quad_addresses(current_quad, memory_stack[-1])
    # GOTOMAIN execution
    if current_quad[0] == 'GOTOMAIN':
        main_vw = ovejota_manager.get_variable_workspace('#global', 'main')
        main_tw = ovejota_manager.get_temps_workspace('#global', 'main')
        # create tuples with sizes
        main_variable_workspace = (
            main_vw['int'], main_vw['float'], main_vw['bool'], main_vw['string'])
        main_temps_workspace = (
            main_tw['int'], main_tw['float'], main_tw['bool'], main_tw['string'])
        main_memory = LocalMemory(
            main_variable_workspace, main_temps_workspace)
        memory_stack.append(main_memory)
        instruction_pointer = current_quad[3]
        continue

    # Assignment execution
    elif current_quad[0] == '=':
        to_assign_type, to_assign_value = get_type_and_value(
            memory_stack[-1], current_quad[1])
        to_assign_value = formatter.cast(to_assign_value, to_assign_type)
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], to_assign_value)

    # Addition execution
    elif current_quad[0] == '+':
        left_operand, right_operand = get_binary_operands(
            memory_stack[-1], current_quad[1], current_quad[2])
        sum_result = left_operand + right_operand
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], sum_result)

    # Subtraction execution
    elif current_quad[0] == '-':
        left_operand, right_operand = get_binary_operands(
            memory_stack[-1], current_quad[1], current_quad[2])
        sub_result = left_operand - right_operand
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], sub_result)

    # Multiplication execution
    elif current_quad[0] == '*':
        left_operand, right_operand = get_binary_operands(
            memory_stack[-1], current_quad[1], current_quad[2])
        mult_result = left_operand * right_operand
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], mult_result)

    # Division execution
    elif current_quad[0] == '/':
        left_operand, right_operand = get_binary_operands(
            memory_stack[-1], current_quad[1], current_quad[2])
        div_result = left_operand / right_operand
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], div_result)

    # Greater than execution
    elif current_quad[0] == '>':
        left_operand, right_operand = get_binary_operands(
            memory_stack[-1], current_quad[1], current_quad[2])
        gt_result = left_operand > right_operand
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], gt_result)

    # Less than execution
    elif current_quad[0] == '<':
        left_operand, right_operand = get_binary_operands(
            memory_stack[-1], current_quad[1], current_quad[2])
        lt_result = left_operand < right_operand
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], lt_result)

    # Equals execution
    elif current_quad[0] == '==':
        left_operand, right_operand = get_binary_operands(
            memory_stack[-1], current_quad[1], current_quad[2])
        equals_result = left_operand == right_operand
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], equals_result)

    # Not equals execution
    elif current_quad[0] == '!=':
        left_operand, right_operand = get_binary_operands(
            memory_stack[-1], current_quad[1], current_quad[2])
        not_equals_result = left_operand != right_operand
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], not_equals_result)

    # And execution
    elif current_quad[0] == '&&':
        left_operand, right_operand = get_binary_operands(
            memory_stack[-1], current_quad[1], current_quad[2])
        if left_operand and right_operand:
            and_result = True
        else:
            and_result = False
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], and_result)

    # Or execution
    elif current_quad[0] == '||':
        left_operand, right_operand = get_binary_operands(
            memory_stack[-1], current_quad[1], current_quad[2])
        if left_operand or right_operand:
            or_result = True
        else:
            or_result = False
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], or_result)

    # Write execution
    elif current_quad[0] == 'WRITE':
        to_write_type, to_write_value = get_type_and_value(
            memory_stack[-1], current_quad[3])
        print(to_write_value) # This is functionality and not for testing

    # Read execution
    elif current_quad[0] == 'READ':
        to_save_type, to_save_value = get_type_and_value(
            memory_stack[-1], current_quad[3])
        to_save_value = input()
        # print(type(to_save_value))
        if to_save_type == 'int':
            try:
                to_save_value = int(to_save_value)
                set_value_in_memory(
                    current_quad[3],  memory_stack[-1], to_save_value)
            except Exception as e:
                raise Exception(
                    'Input type mismatch, expected: ' + to_save_type)
        elif to_save_type == 'float':
            # If Pythono cast to int is successful, then break since it is not a PecanPy float
            try:
                if '.' not in to_save_value:
                    raise Exception(
                        'Input type mismatch, expected: ' + to_save_type)
                to_save_value = float(to_save_value)
                set_value_in_memory(
                    current_quad[3],  memory_stack[-1], to_save_value)
            except Exception as e:
                raise Exception(e)

        elif to_save_type == 'bool':
            if to_save_value == 'true' or to_save_value == 'false':
                to_save_value = to_save_value == 'true'
                set_value_in_memory(
                    current_quad[3],  memory_stack[-1], to_save_value)
            else:
                raise Exception(
                    'Input type mismatch, expected: ' + to_save_type)

        elif to_save_type == 'string':
            if '"' in to_save_value:
                raise Exception(
                    'Input type mismatch, expected: ' + to_save_type)
            else:
                set_value_in_memory(
                    current_quad[3],  memory_stack[-1], to_save_value)
        else:
            raise Exception('Input type mismatch, expected: ' + to_save_type)

     # GOTO execution
    elif current_quad[0] == 'GOTO':
        instruction_pointer = current_quad[3]
        continue

    # GOTOF execution
    elif current_quad[0] == 'GOTOF':
        _, condition_value = get_type_and_value(
            memory_stack[-1], current_quad[1])
        if not condition_value:
            instruction_pointer = current_quad[3]
            continue

    # GOTOT execution
    elif current_quad[0] == 'GOTOT':
        _, condition_value = get_type_and_value(
            memory_stack[-1], current_quad[1])
        if condition_value:
            instruction_pointer = current_quad[3]
            continue

    instruction_pointer += 1

print('--------------------END OF EXECUTION-----------------------------')
print(*quads, sep='\n')
# print(memory_stack[-1].table)
# print(global_memory.table)
