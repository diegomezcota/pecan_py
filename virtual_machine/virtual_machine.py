from Memory import GlobalMemory
from Memory import LocalMemory
from ovejota_manager import OvejotaManager
from formatter import Formatter
from collections import deque

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
# Queue of start quads constructors for global objects
global_objects_constructors_start_quads_queue = deque(ovejota_manager.get_global_objects_constructors_start_quads())

quads = ovejota_manager.quads

instruction_pointer = 0
memory_stack = []
memories_to_be = []
instruction_pointer_stack = []


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
            # make the check for && operand
            if len(str(element)) > 1 and str(element)[1] == '&':
                continue
            element = element[1:]
            element = int(element)
            _, new_address = get_type_and_value(memory, element)
            current_quad[i] = new_address
    return current_quad

def clean_object_quads(current_quad, memory):
    object_base_addresses = None
    if memory.object:
        object_base_addresses = memory.object['object_base_addresses']       
    for i, element in enumerate(current_quad):
        if element is not None and type(element) is list:
            new_element = element.copy()
            el_type = new_element[1]
            new_element[0] += object_base_addresses[el_type]
            new_element[1] = memory.object['object_scope']
            current_quad[i] = new_element
                     
    return current_quad

def is_method_quad(quad_element):
    return quad_element is not None and type(quad_element) is list

def get_method_binary_operands(method_memory, calling_function_memory, left_operand_elem, right_operand_elem):
    if is_method_quad(left_operand_elem):
        _, left_operand = get_type_and_value(
            calling_function_memory, left_operand_elem[0])
    else:
        _, left_operand = get_type_and_value(
            method_memory, left_operand_elem)
    if is_method_quad(right_operand_elem):
        _, right_operand = get_type_and_value(
            calling_function_memory, right_operand_elem[0])
    else:
        _, right_operand = get_type_and_value(
            method_memory, right_operand_elem)
    return left_operand, right_operand

print('--------------------START OF EXECUTION-----------------------------')

while (instruction_pointer < len(quads)):
    current_quad = quads[instruction_pointer].copy()
    if len(memory_stack) > 100000:
        raise Exception('Stack overflow: too many pending calls')
    if memory_stack:
        current_quad = clean_quad_addresses(current_quad, memory_stack[-1])
        current_quad = clean_object_quads(current_quad, memory_stack[-1])
    # SOLVE_GLOBAL_OBJ execution
    if current_quad[0] == 'SOLVE_GLOBAL_OBJ':
        if len(global_objects_constructors_start_quads_queue) > 0:
            constructor_start_quad = global_objects_constructors_start_quads_queue.popleft()
            instruction_pointer = constructor_start_quad
            continue
    if current_quad[0] == 'GO_BACK_TO_SOLVE_GLOBAL_OBJ':
        instruction_pointer = 0
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
        to_assign_type, to_assign_value = None, None
        # check if value to assign involves two memories
        if is_method_quad(current_quad[1]):
            # check where the address "lives" (global, local)
            object_scope = memory_stack[-1].object['object_scope']
            # handle special case of global constructor
            if len(memory_stack) >= 2:
                to_assign_type, to_assign_value = get_type_and_value(
                        memory_stack[-2], current_quad[1][0])
            else:
                to_assign_type, to_assign_value = get_type_and_value(
                        global_memory, current_quad[1][0])
        else:
            to_assign_type, to_assign_value = get_type_and_value(
                memory_stack[-1], current_quad[1])
        to_assign_value = formatter.cast(to_assign_value, to_assign_type)
        # check which memory to assign to
        if is_method_quad(current_quad[3]):
            # check where the address "lives" (global, local)
            object_scope = memory_stack[-1].object['object_scope']
            # handle special case of global constructor
            if len(memory_stack) >= 2:
                memory_stack[-2] = set_value_in_memory(
                        current_quad[3][0], memory_stack[-2], to_assign_value)
            else:
                global_memory = set_value_in_memory(
                        current_quad[3][0], global_memory, to_assign_value)
        else:
            memory_stack[-1] = set_value_in_memory(
                current_quad[3], memory_stack[-1], to_assign_value)

    # Addition execution
    elif current_quad[0] == '+':
        left_operand, right_operand = None, None
        # check if it's a method quad
        if is_method_quad(current_quad[1]) or is_method_quad(current_quad[2]):
            if len(memory_stack) >= 2:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], memory_stack[-2], current_quad[1], current_quad[2])
            else:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], global_memory, current_quad[1], current_quad[2])
        else:
            left_operand, right_operand = get_binary_operands(
                memory_stack[-1], current_quad[1], current_quad[2])
        sum_result = left_operand + right_operand
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], sum_result)

    # Subtraction execution
    elif current_quad[0] == '-':
        left_operand, right_operand = None, None
        # check if it's a method quad
        if is_method_quad(current_quad[1]) or is_method_quad(current_quad[2]):
            if len(memory_stack >= 2):
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], memory_stack[-2], current_quad[1], current_quad[2])
            else:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], global_memory, current_quad[1], current_quad[2])
        else:
            left_operand, right_operand = get_binary_operands(
                memory_stack[-1], current_quad[1], current_quad[2])
        sub_result = left_operand - right_operand
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], sub_result)

    # Multiplication execution
    elif current_quad[0] == '*':
        left_operand, right_operand = None, None
        # check if it's a method quad
        if is_method_quad(current_quad[1]) or is_method_quad(current_quad[2]):
            if len(memory_stack) >= 2:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], memory_stack[-2], current_quad[1], current_quad[2])
            else:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], global_memory, current_quad[1], current_quad[2])
        else:
            left_operand, right_operand = get_binary_operands(
                memory_stack[-1], current_quad[1], current_quad[2])
        mult_result = left_operand * right_operand
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], mult_result)

    # Division execution
    elif current_quad[0] == '/':
        left_operand, right_operand = None, None
        # check if it's a method quad
        if is_method_quad(current_quad[1]) or is_method_quad(current_quad[2]):
            if len(memory_stack) >= 2:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], memory_stack[-2], current_quad[1], current_quad[2])
            else:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], global_memory, current_quad[1], current_quad[2])
        else:
            left_operand, right_operand = get_binary_operands(
                memory_stack[-1], current_quad[1], current_quad[2])
        div_result = left_operand / right_operand
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], div_result)

    # Greater than execution
    elif current_quad[0] == '>':
        left_operand, right_operand = None, None
        # check if it's a method quad
        if is_method_quad(current_quad[1]) or is_method_quad(current_quad[2]):
            if len(memory_stack) >= 2:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], memory_stack[-2], current_quad[1], current_quad[2])
            else:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], global_memory, current_quad[1], current_quad[2])
        else:
            left_operand, right_operand = get_binary_operands(
                memory_stack[-1], current_quad[1], current_quad[2])
        gt_result = left_operand > right_operand
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], gt_result)

    # Less than execution
    elif current_quad[0] == '<':
        left_operand, right_operand = None, None
        # check if it's a method quad
        if is_method_quad(current_quad[1]) or is_method_quad(current_quad[2]):
            if len(memory_stack) >= 2:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], memory_stack[-2], current_quad[1], current_quad[2])
            else:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], global_memory, current_quad[1], current_quad[2])
        else:
            left_operand, right_operand = get_binary_operands(
                memory_stack[-1], current_quad[1], current_quad[2])
        lt_result = left_operand < right_operand
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], lt_result)

    # Equals execution
    elif current_quad[0] == '==':
        left_operand, right_operand = None, None
        # check if it's a method quad
        if is_method_quad(current_quad[1]) or is_method_quad(current_quad[2]):
            if len(memory_stack) >= 2:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], memory_stack[-2], current_quad[1], current_quad[2])
            else:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], global_memory, current_quad[1], current_quad[2])
        else:
            left_operand, right_operand = get_binary_operands(
                memory_stack[-1], current_quad[1], current_quad[2])
        equals_result = left_operand == right_operand
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], equals_result)

    # Not equals execution
    elif current_quad[0] == '!=':
        left_operand, right_operand = None, None
        # check if it's a method quad
        if is_method_quad(current_quad[1]) or is_method_quad(current_quad[2]):
            if len(memory_stack) >= 2:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], memory_stack[-2], current_quad[1], current_quad[2])
            else:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], global_memory, current_quad[1], current_quad[2])
        else:
            left_operand, right_operand = get_binary_operands(
                memory_stack[-1], current_quad[1], current_quad[2])
        not_equals_result = left_operand != right_operand
        memory_stack[-1] = set_value_in_memory(
            current_quad[3], memory_stack[-1], not_equals_result)

    # And execution
    elif current_quad[0] == '&&':
        left_operand, right_operand = None, None
        # check if it's a method quad
        if is_method_quad(current_quad[1]) or is_method_quad(current_quad[2]):
            if len(memory_stack) >= 2:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], memory_stack[-2], current_quad[1], current_quad[2])
            else:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], global_memory, current_quad[1], current_quad[2])
        else:
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
        left_operand, right_operand = None, None
        # check if it's a method quad
        if is_method_quad(current_quad[1]) or is_method_quad(current_quad[2]):
            if len(memory_stack) >= 2:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], memory_stack[-2], current_quad[1], current_quad[2])
            else:
                left_operand, right_operand = get_method_binary_operands(memory_stack[-1], global_memory, current_quad[1], current_quad[2])
        else:
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
        to_write_type, to_write_value = None, None
        if is_method_quad(current_quad[3]):
            if len(memory_stack) >= 2:
                to_write_type, to_write_value = get_type_and_value(
                    memory_stack[-2], current_quad[3][0])
            else:
                to_write_type, to_write_value = get_type_and_value(
                    global_memory, current_quad[3][0])
        else:
            to_write_type, to_write_value = get_type_and_value(
                memory_stack[-1], current_quad[3])
        print(to_write_value)  # This is functionality and not for testing

    # Read execution
    elif current_quad[0] == 'READ':
        to_save_type, to_save_value = None, None
        flag_method_quad = is_method_quad(current_quad[3]) 
        if flag_method_quad:
            if len(memory_stack) >= 2:
                to_save_type, to_save_value = get_type_and_value(
                    memory_stack[-2], current_quad[3][0])
            else:
                to_save_type, to_save_value = get_type_and_value(
                    global_memory, current_quad[3][0])
        else:
            to_save_type, to_save_value = get_type_and_value(
                memory_stack[-1], current_quad[3])
        to_save_value = input()
        # print(type(to_save_value))
        if to_save_type == 'int':
            try:
                to_save_value = int(to_save_value)
                if flag_method_quad:
                    if len(memory_stack) >= 2:
                        set_value_in_memory(
                            current_quad[3][0],  memory_stack[-2], to_save_value)
                    else:
                        set_value_in_memory(
                            current_quad[3][0],  global_memory, to_save_value)
                else:
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
                if flag_method_quad:
                    if len(memory_stack) >= 2:
                        set_value_in_memory(
                            current_quad[3][0],  memory_stack[-2], to_save_value)
                    else:
                        set_value_in_memory(
                            current_quad[3][0],  global_memory, to_save_value)
                else:
                    set_value_in_memory(
                        current_quad[3],  memory_stack[-1], to_save_value)
            except Exception as e:
                raise Exception(e)

        elif to_save_type == 'bool':
            if to_save_value == 'true' or to_save_value == 'false':
                to_save_value = to_save_value == 'true'
                if flag_method_quad:
                    if len(memory_stack) >= 2:
                        set_value_in_memory(
                            current_quad[3][0],  memory_stack[-2], to_save_value)
                    else:
                        set_value_in_memory(
                            current_quad[3][0],  global_memory, to_save_value)
                else:
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
                if flag_method_quad:
                    if len(memory_stack) >= 2:
                        set_value_in_memory(
                            current_quad[3][0],  memory_stack[-2], to_save_value)
                    else:
                        set_value_in_memory(
                            current_quad[3][0],  global_memory, to_save_value)
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
        condition_value = None
        if is_method_quad(current_quad[1]):
            if len(memory_stack) >= 2:
                _, condition_value = get_type_and_value(
                memory_stack[-2], current_quad[1][0])
            else:
                _, condition_value = get_type_and_value(
                global_memory, current_quad[1][0])
        else:
            _, condition_value = get_type_and_value(
                memory_stack[-1], current_quad[1])
        if not condition_value:
            instruction_pointer = current_quad[3]
            continue

    # GOTOT execution
    elif current_quad[0] == 'GOTOT':
        condition_value = None
        if is_method_quad(current_quad[1]):
            if len(memory_stack) >= 2:
                _, condition_value = get_type_and_value(
                memory_stack[-2], current_quad[1][0])
            else:
                 _, condition_value = get_type_and_value(
                global_memory, current_quad[1][0])
        else:
            _, condition_value = get_type_and_value(
                memory_stack[-1], current_quad[1])
        if condition_value:
            instruction_pointer = current_quad[3]
            continue

    # VERIFY execution (for group data structures)
    elif current_quad[0] == 'VERIFY':
        dim_size = current_quad[1]
        index_type, index_value = None, None
        if is_method_quad(current_quad[2]):
            if len(memory_stack) >= 2:
                index_type, index_value = get_type_and_value(
                    memory_stack[-2], current_quad[2][0])
            else:
                index_type, index_value = get_type_and_value(
                    global_memory, current_quad[2][0])
        else:
            index_type, index_value = get_type_and_value(
                memory_stack[-1], current_quad[2])
        if 0 > index_value or index_value >= dim_size:
            raise Exception('Group index out of bounds')

    # GOSUB execution (for global functions)
    elif current_quad[0] == 'GOSUB':
        function_name = current_quad[1]
        function_start_quad = current_quad[3]
        new_memory_to_execute = memories_to_be.pop()
        memory_stack.append(new_memory_to_execute[0])
        instruction_pointer_stack.append(instruction_pointer)
        instruction_pointer = function_start_quad
        continue

    # ERA execution (for global functions)
    elif current_quad[0] == 'ERA':
        function_name = current_quad[3]
        function_vw = ovejota_manager.get_variable_workspace(
            '#global', function_name)
        function_tw = ovejota_manager.get_temps_workspace(
            '#global', function_name)
        function_variable_workspace = (
            function_vw['int'], function_vw['float'], function_vw['bool'], function_vw['string'])
        function_temps_workspace = (
            function_tw['int'], function_tw['float'], function_tw['bool'], function_tw['string'])
        function_memory = LocalMemory(
            function_variable_workspace, function_temps_workspace)
        memories_to_be.append(
            [function_memory, {'int': 8000, 'float': 10000, 'bool': 12000, 'string': 14000}])

    # PARAM execution
    elif current_quad[0] == 'PARAM':
        param_address = current_quad[1]
        param_index = current_quad[3]
        param_type, param_value = None, None
        # if it's called from method
        if memory_stack:
            param_type, param_value = get_type_and_value(
                memory_stack[-1], param_address)
        else:
            param_type, param_value = get_type_and_value(
                global_memory, param_address)
        new_param_address = memories_to_be[-1][1][param_type]
        memories_to_be[-1][0].set_value_in_address(
            new_param_address, param_value)
        memories_to_be[-1][1][param_type] += 1

    # ENDFUNC execution
    elif current_quad[0] == 'ENDFUNC':
        memory_stack.pop()
        instruction_pointer = instruction_pointer_stack.pop()
    
    # ERA_OBJ_MET execution (for class methods)
    elif current_quad[0] == 'ERA_OBJ_MET':
        object_scope = current_quad[1] # helps us see where it was declared (global, main, etc)
        object_base_addresses = current_quad[2] # helps us see the specific base addresses for the object calling the method
        function_codename = current_quad[3]
        class_name = function_codename.split('#')[0]
        class_method_name = function_codename.split('#')[1]
        method_vw = ovejota_manager.get_variable_workspace(class_name, class_method_name)
        method_tw = ovejota_manager.get_temps_workspace(class_name, class_method_name)
        method_variable_workspace = (
             method_vw['int'], method_vw['float'], method_vw['bool'], method_vw['string'])
        method_temps_workspace = (
             method_tw['int'], method_tw['float'], method_tw['bool'], method_tw['string'])
        method_memory = LocalMemory(
             method_variable_workspace, method_temps_workspace)
        # set object characteristics
        method_memory.set_object_characteristics(object_scope, object_base_addresses)
        memories_to_be.append(
             [method_memory, {'int': 8000, 'float': 10000, 'bool': 12000, 'string': 14000}])
    
    # GOSUB_OBJ execution (for class methods)
    elif current_quad[0] == 'GOSUB_OBJ':
        class_method_name = current_quad[1]
        object_var_name = current_quad[2]
        method_start_quad = current_quad[3]
        new_memory_to_execute = memories_to_be.pop()
        memory_stack.append(new_memory_to_execute[0])
        instruction_pointer_stack.append(instruction_pointer)
        instruction_pointer = method_start_quad
        continue

    instruction_pointer += 1

print('--------------------END OF EXECUTION-----------------------------')
# print(*quads, sep='\n')
# print(memory_stack[-1].table)
# print(global_memory.table)
