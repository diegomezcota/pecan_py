from function_directory import FunctionDirectory
from avail import Avail
from quadruples import Quadruples
from semantic_cube import SemanticCube
from constants import Constants
import ply.yacc as yacc
from lexer import tokens

import json

function_directory = None
avail = None
quads = None
semantic_cube = None
operand_stack = None
operator_stack = None
jump_stack = None
control_variable_stack = None
constants = None
dim_stack = None

current_general_scope = None
current_internal_scope = None
current_var_name = None
current_var_type = None
current_var_data_type = None
current_group_internal_scope = None

# For function calls
function_param_counter = None
current_function_call_name = None


def p_program(p):
    '''
    program : PROGRAM np_start_state np_start_func_dir ID SEMICOLON declaration_loop main_function
    '''
    #print(*quads.list, sep='\n')
    #print(json.dumps(function_directory.table, indent=2))

    function_directory.generate_variable_workspace('#global', '#global')

    function_directory.delete_vars_table('#global', '#global')

    constants_table = avail.get_counter_summary('constants')

    obj = {"function_directory": function_directory.table,
           "quads": quads.list, "constants_summary": constants_table, "constants_table": constants.table}
    with open('ovejota.json', "w") as output_file:
        json.dump(obj, output_file, indent=2)


def p_main_function(p):
    '''
    main_function : MAIN np_add_main_internal_scope OPEN_PARENTHESIS CLOSE_PARENTHESIS OPEN_KEY variable_declaration_loop np_generate_variable_workspace np_add_function_start_quad statement_loop CLOSE_KEY np_end_function
    '''
    global current_internal_scope
    current_internal_scope = '#global'
    avail.reset_local_counters()


def p_np_add_main_internal_scope(p):
    '''
    np_add_main_internal_scope : epsilon
    '''
    global function_directory, current_internal_scope
    current_internal_scope = 'main'
    function_directory.add_internal_scope(
        current_general_scope, current_internal_scope)
    function_directory.set_function_type(
        current_general_scope, current_internal_scope, 'void')

    # Llenar el numero de cuadruplo de inicio de la funcion main al primer cuadruplo
    quads.fill_quad(0, 3, quads.counter)


def p_np_start_state(p):
    '''
    np_start_state : epsilon
    '''
    global function_directory, avail, quads, semantic_cube, operand_stack, operator_stack, jump_stack, control_variable_stack
    global current_general_scope, current_internal_scope, current_var_name, current_var_type, current_var_data_type, constants, dim_stack, current_group_internal_scope
    function_directory = FunctionDirectory()
    avail = Avail()
    quads = Quadruples()
    semantic_cube = SemanticCube()
    operand_stack = []
    operator_stack = []
    jump_stack = []
    control_variable_stack = []
    current_general_scope = None
    current_internal_scope = None
    current_var_name = None
    current_var_type = None
    current_var_data_type = None
    constants = Constants()
    dim_stack = []
    # Agregar constante 1 para funcionalidad for
    one_constant_address = avail.get_new_address('int', 'constants')
    constants.add_constant('int', one_constant_address, '1')

    # Primer cuadruplo para empezar en el main
    quads.generate_quad('GOTOMAIN', None, None, None)

    # Arrays and matrices
    current_group_internal_scope = None


def p_np_start_func_dir(p):
    '''
    np_start_func_dir : epsilon
    '''
    global function_directory, current_general_scope, current_internal_scope
    current_general_scope = '#global'
    current_internal_scope = '#global'
    function_directory.add_general_scope(current_general_scope)
    function_directory.add_internal_scope(
        current_general_scope, current_internal_scope)
    function_directory.set_function_type(
        current_general_scope, current_internal_scope, 'void')


def p_declaration_loop(p):
    '''
    declaration_loop : declaration declaration_loop
                     | epsilon
    '''
    pass


def p_statement_loop(p):
    '''
    statement_loop  : statement statement_loop1
    '''
    p[0] = [p[1]] + p[2]


def p_statement_loop1(p):
    '''
    statement_loop1 : statement statement_loop1
                    | epsilon
    '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_declaration(p):
    '''
    declaration : class_declaration
                | variable_declaration
                | function_declaration
    '''
    p[0] = p[1]
    pass


def p_variable(p):
    '''
    variable    : ID variable1
    '''
    p[0] = p[2]


def p_variable1(p):
    '''
    variable1   : np_array_access1 OPEN_BRACKET np_array_access2 hyper_exp np_array_access3 CLOSE_BRACKET group_access
                | DOT ID
                | epsilon

    '''
    if len(p) == 2:
        if (function_directory.has_variable(current_general_scope, current_internal_scope, p[-1])):
            variable_map = function_directory.table[current_general_scope][
                current_internal_scope]['vars_table'][p[-1]]
            variable_address, variable_data_type = variable_map[
                'var_virtual_address'], variable_map['var_data_type']
            p[0] = (variable_address, variable_data_type)
        elif (function_directory.has_variable(current_general_scope, '#global', p[-1])):
            variable_map = function_directory.table[current_general_scope]['#global']['vars_table'][p[-1]]
            variable_address, variable_data_type = variable_map[
                'var_virtual_address'], variable_map['var_data_type']
            p[0] = (variable_address, variable_data_type)
        else:
            raise VariableNotDefined(
                "Variable " + p[-1] + " not defined in line " + str(p.lineno(1)))
    elif len(p) == 8:
        p[0] = p[7]


def p_group_access(p):
    '''
    group_access    : np_array_access4 OPEN_BRACKET hyper_exp np_array_access3 CLOSE_BRACKET np_array_access5
                    | np_array_access5
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[6]


def p_np_array_access1(p):
    '''
    np_array_access1 : epsilon
    '''
    global current_var_name, current_group_internal_scope

    if (function_directory.has_variable(current_general_scope, current_internal_scope, p[-1])):
        variable_map = function_directory.table[current_general_scope][
            current_internal_scope]['vars_table'][p[-1]]
        variable_address, variable_data_type = variable_map[
            'var_virtual_address'], variable_map['var_data_type']
        current_group_internal_scope = current_internal_scope
    elif (function_directory.has_variable(current_general_scope, '#global', p[-1])):
        variable_map = function_directory.table[current_general_scope]['#global']['vars_table'][p[-1]]
        variable_address, variable_data_type = variable_map[
            'var_virtual_address'], variable_map['var_data_type']
        current_group_internal_scope = '#global'
    else:
        raise VariableNotDefined(
            "Variable " + p[-1] + " not defined in line " + str(p.lineno(1)))

    current_var_name = p[-1]
    operand_stack.append((variable_address, variable_data_type))


def p_np_array_access2(p):
    '''
    np_array_access2 : epsilon
    '''

    group_id_address, _ = operand_stack.pop()
    group_dim = function_directory.get_group_dimensions(
        current_general_scope, current_group_internal_scope, current_var_name)

    # TODO: Check for second dimension validation
    if group_dim > 0:
        dim_arr = [group_id_address, 1,
                   current_group_internal_scope, current_var_name]
        dim_stack.append(dim_arr)
        operator_stack.append('[')
    else:
        raise Exception(
            'Variable ' + current_var_name + ' does not have dimensions.')


def p_np_array_access3(p):
    '''
    np_array_access3 : epsilon
    '''
    dim_size = function_directory.get_dim_size(
        current_general_scope, dim_stack[-1][2], dim_stack[-1][3], dim_stack[-1][1])
    index = operand_stack[-1][0]

    quads.generate_quad('VERIFY', dim_size, index, None)

    aux_address, aux_type = operand_stack.pop()
    if aux_type != 'int':
        raise Exception('Can not index variable ' +
                        dim_stack[-1][3] + ' with type ' + aux_type)
    mdim = function_directory.get_m_dim(
        current_general_scope, dim_stack[-1][2], dim_stack[-1][3], dim_stack[-1][1])
    new_address = constants.get_constant_address('int', str(int(mdim)))
    temp_address = avail.get_new_address('int', 'temps')
    quads.generate_quad('*', aux_address, new_address, temp_address)
    operand_stack.append((temp_address, 'int'))

    if dim_stack[-1][1] > 1:
        aux2_address, _ = operand_stack.pop()
        aux1_address, _ = operand_stack.pop()
        temp_address = avail.get_new_address('int', 'temps')
        quads.generate_quad('+', aux1_address, aux2_address, temp_address)
        operand_stack.append((temp_address, 'int'))


def p_np_array_access4(p):
    '''
    np_array_access4 : epsilon
    '''
    global dim_stack

    # dim_stack[-1][2] contiene el internal_scope del group
    # dim_stack[-1][3] contiene el nombre de la variable del group
    if function_directory.get_group_dimensions(current_general_scope, dim_stack[-1][2], dim_stack[-1][3]) != 2:
        raise Exception(
            'Variable ' + dim_stack[-1][3] + ' has only one dimension')
    else:
        dim_stack[-1][1] += 1


def p_np_array_access5(p):
    '''
    np_array_access5 : epsilon
    '''
    aux1_address, _ = operand_stack.pop()
    group_virtual_address = function_directory.get_variable_virtual_address(
        current_general_scope, dim_stack[-1][2], dim_stack[-1][3])
    new_address = None
    if not constants.has_constant('int', str(group_virtual_address)):
        new_address = avail.get_new_address('int', 'constants')
        constants.add_constant('int', new_address, str(group_virtual_address))
    else:
        new_address = constants.get_constant_address(
            'int', str(group_virtual_address))
    new_temp_address = avail.get_new_address('int', 'temps')
    quads.generate_quad('+', aux1_address, new_address, new_temp_address)
    pointer_address = '&' + str(new_temp_address)
    dim_stack.pop()
    operator_stack.pop()
    p[0] = (pointer_address, 'int')


def p_class_declaration(p):
    '''
    class_declaration   : CLASS ID class_declaration1 OPEN_KEY class_body CLOSE_KEY SEMICOLON constructor class_declaration2
    '''
    pass


def p_class_declaration1(p):
    '''
    class_declaration1  : IS ID
                        | epsilon
    '''
    pass


def p_class_declaration2(p):
    '''
    class_declaration2  : class_function class_declaration2
                        | epsilon
    '''
    pass


def p_class_body(p):
    '''
    class_body  : class_body1 class_body3
    '''
    pass


def p_class_body1(p):
    '''
    class_body1 : variable_declaration class_body2
    '''
    pass


def p_class_body2(p):
    '''
    class_body2 : variable_declaration class_body2
                | epsilon
    '''
    pass


def p_class_body3(p):
    '''
    class_body3 : class_function_declaration class_body4
    '''
    pass


def p_class_body4(p):
    '''
    class_body4 : class_function_declaration class_body4
                | epsilon

    '''
    pass


def p_constructor(p):
    '''
    constructor : CONSTRUCTOR ID OPEN_PARENTHESIS parameter CLOSE_PARENTHESIS OPEN_KEY statement_loop CLOSE_KEY
    '''
    pass


def p_variable_declaration_loop(p):
    '''
    variable_declaration_loop : variable_declaration variable_declaration_loop
                                | epsilon
    '''
    pass


def p_variable_declaration(p):
    '''
    variable_declaration    : VAR np_set_current_var_type data_type np_set_current_var_data_type ID np_set_current_var_name SEMICOLON np_add_variable
                            | GROUP np_set_current_var_type ID np_set_current_var_name ASSIGN data_type np_set_current_var_data_type np_add_variable OPEN_BRACKET np_add_dim1_list INT_VALUE np_add_dim1 CLOSE_BRACKET group1 SEMICOLON
                            | OBJ np_set_current_var_type ID np_set_current_var_name ASSIGN ID OPEN_PARENTHESIS variable_declaration1 CLOSE_PARENTHESIS SEMICOLON np_add_variable

    '''
    pass


def p_np_set_current_var_type(p):
    '''
    np_set_current_var_type : epsilon
    '''
    global current_var_type
    current_var_type = p[-1]


def p_np_set_current_var_data_type(p):
    '''
    np_set_current_var_data_type : epsilon
    '''
    global current_var_data_type
    current_var_data_type = p[-1]


def p_np_set_current_var_name(p):
    '''
    np_set_current_var_name : epsilon
    '''
    global current_var_name
    current_var_name = p[-1]


def p_np_add_variable(p):
    '''
    np_add_variable : epsilon
    '''
    new_variable_address = None
    if (current_general_scope == '#global'):
        if (current_internal_scope == '#global'):
            new_variable_address = avail.get_new_address(
                current_var_data_type, 'globals')
        else:
            new_variable_address = avail.get_new_address(
                current_var_data_type, 'locals')

    function_directory.add_variable(current_general_scope, current_internal_scope,
                                    current_var_name, current_var_type, current_var_data_type, new_variable_address)


def p_group1(p):
    '''
    group1  : epsilon
            | OPEN_BRACKET np_add_dim2_list INT_VALUE np_add_dim2 CLOSE_BRACKET
    '''
    function_directory.generate_dim_ms(
        current_general_scope, current_internal_scope, current_var_name)

    group_scope = None
    if (current_general_scope == '#global'):
        if (current_internal_scope == '#global'):
            group_scope = 'globals'
        else:
            group_scope = 'locals'

    group_size = function_directory.get_group_size(
        current_general_scope, current_internal_scope, current_var_name)

    # size - 1 : the original id is assigned to an address in np_add_variable
    avail.get_group_addresses(current_var_data_type,
                              group_scope, group_size - 1)


def p_np_add_dim1_list(p):
    '''
    np_add_dim1_list : epsilon
    '''
    function_directory.add_dim1_list(
        current_general_scope, current_internal_scope, current_var_name)


def p_np_add_dim2_list(p):
    '''
    np_add_dim2_list : epsilon
    '''
    function_directory.add_dim2_list(
        current_general_scope, current_internal_scope, current_var_name)


def p_np_add_dim1(p):
    '''
    np_add_dim1 : epsilon
    '''
    dim_size, _ = p[-1]
    dim_size = int(dim_size)
    function_directory.add_dim_size_and_update_r(
        current_general_scope, current_internal_scope, current_var_name, 0, dim_size)

    # Add size's int value as constant
    if not constants.has_constant('int', p[-1][0]):
        constant_address = avail.get_new_address('int', 'constants')
        constants.add_constant('int', constant_address, p[-1][0])


def p_np_add_dim2(p):
    '''
    np_add_dim2 : epsilon
    '''
    dim_size, _ = p[-1]
    dim_size = int(dim_size)
    function_directory.add_dim_size_and_update_r(
        current_general_scope, current_internal_scope, current_var_name, 1, dim_size)

    # Add size's int value as constant
    if not constants.has_constant('int', p[-1][0]):
        constant_address = avail.get_new_address('int', 'constants')
        constants.add_constant('int', constant_address, p[-1][0])


def p_variable_declaration1(p):
    '''
    variable_declaration1   : hyper_exp_loop
                            | epsilon
    '''
    pass


def p_statement(p):
    '''
    statement   : assignment
                | conditional
                | cycle
                | read
                | write
                | function_call SEMICOLON
    '''
    p[0] = p[1]
    pass


def p_assignment(p):
    '''
    assignment  : variable np_variable_assignment ASSIGN hyper_exp SEMICOLON
    '''
    var_value, var_type = p[1]
    exp_value, exp_type = operand_stack.pop()
    result_type = semantic_cube.is_type_match(var_type, exp_type, '=')
    if result_type:
        quads.generate_quad('=', exp_value, None, var_value)
    else:
        error_msg = "Impossible assignment between " + var_type + " and " + exp_type
        raise TypeMismatchError(error_msg + " in line " + str(p.lineno(3)))


def p_np_variable_assignment(p):
    '''
    np_variable_assignment : epsilon
    '''
    var_address, _ = p[-1]
    if var_address in control_variable_stack:
        raise Exception(
            "Changing the control variable inside a for loop is invalid in line " + str(p.lineno(1)))


def p_np_add_operator(p):
    '''
    np_add_operator : epsilon
    '''
    operator_stack.append(p[-1])


def p_hyper_exp(p):
    '''
    hyper_exp   : super_exp np_hyper_exp hyper_exp1
    '''


def p_hyper_exp1(p):
    '''
    hyper_exp1  : AND np_add_operator super_exp np_hyper_exp hyper_exp1
                | OR np_add_operator super_exp np_hyper_exp hyper_exp1
                | epsilon
    '''
    pass


def p_np_hyper_exp(p):
    '''
    np_hyper_exp : epsilon
    '''
    add_exp_quad(['&&', '||'], p.lineno(1))


def p_super_exp(p):
    '''
    super_exp   : exp np_super_exp super_exp1
    '''
    pass


def p_super_exp1(p):
    '''
    super_exp1  : GREATER_THAN np_add_operator exp np_super_exp super_exp1
                | LESS_THAN np_add_operator exp np_super_exp super_exp1
                | EQUAL_TO np_add_operator exp np_super_exp super_exp1
                | NOT_EQUAL_TO np_add_operator exp np_super_exp super_exp1
                | epsilon
    '''
    pass


def p_np_super_exp(p):
    '''
    np_super_exp : epsilon
    '''
    add_exp_quad(['>', '<', '==', '!='], p.lineno(1))


def p_exp(p):
    '''
    exp : term np_exp exp1
    '''
    pass


def p_exp1(p):
    '''
    exp1    : PLUS np_add_operator term np_exp exp1
            | MINUS np_add_operator term np_exp exp1
            | epsilon
    '''
    pass


def p_np_exp(p):
    '''
    np_exp : epsilon
    '''
    add_exp_quad(['+', '-'], p.lineno(1))


def p_term(p):
    '''
    term    : factor np_term term1
    '''
    pass


def p_term1(p):
    '''
    term1   : MULTIPLICATION np_add_operator factor np_term term1
            | DIVISION np_add_operator factor np_term term1
            | epsilon
    '''
    pass


def p_np_term(p):
    '''
    np_term : epsilon
    '''
    add_exp_quad(['*', '/'], p.lineno(1))


def add_exp_quad(operator_list, program_line_no='indefinite_line'):
    if operator_stack and operator_stack[-1] in operator_list:
        ro_value, ro_type = operand_stack.pop()
        lo_value, lo_type = operand_stack.pop()
        operator = operator_stack.pop()
        result_type = semantic_cube.is_type_match(lo_type, ro_type, operator)
        if result_type:
            temp_address, temp_type = avail.get_new_temp(result_type)
            quads.generate_quad(operator, lo_value, ro_value, temp_address)
            operand_stack.append((temp_address, temp_type))
        else:
            error_msg = "Invalid operator " + operator + " between " + \
                lo_type + " type and " + ro_type + " type"
            raise TypeMismatchError(
                error_msg + " in line " + str(program_line_no))


def p_factor(p):
    '''
    factor  : function_call
            | FLOAT_VALUE np_add_constant_virtual_address
            | INT_VALUE np_add_constant_virtual_address
            | BOOL_VALUE np_add_constant_virtual_address
            | STRING_VALUE np_add_constant_virtual_address
            | variable
            | OPEN_PARENTHESIS np_add_open_parenthesis hyper_exp CLOSE_PARENTHESIS np_remove_open_parenthesis
    '''
    if len(p) == 2:
        temp_tuple = p[1]
        operand_stack.append(temp_tuple)
    elif len(p) == 3:
        _, const_type = p[1]
        temp_tuple = (p[2], const_type)
        operand_stack.append(temp_tuple)


def p_np_add_constant_virtual_address(p):
    '''
    np_add_constant_virtual_address : epsilon
    '''
    const_value, const_type = p[-1]

    if not constants.has_constant(const_type, const_value):
        new_const_address = avail.get_new_address(const_type, 'constants')
        constants.add_constant(const_type, new_const_address, const_value)

    p[0] = constants.get_constant_address(const_type, const_value)


def p_np_add_open_parenthesis(p):
    '''
    np_add_open_parenthesis : epsilon
    '''
    operator_stack.append('(')


def p_np_remove_open_parenthesis(p):
    '''
    np_remove_open_parenthesis : epsilon
    '''
    operator_stack.pop()


def p_data_type(p):
    '''
    data_type   : INT
                | FLOAT
                | STRING
                | BOOL
    '''
    p[0] = p[1]


def p_class_function_declaration(p):
    '''
    class_function_declaration : FUNCTION ID OPEN_PARENTHESIS parameter CLOSE_PARENTHESIS RETURNS return_arg SEMICOLON
    '''
    pass


def p_return_arg(p):
    '''
    return_arg  : data_type
                | VOID
    '''
    p[0] = p[1]


def p_parameter(p):
    '''
    parameter   : data_type ID parameter1
                | epsilon
    '''
    if len(p) == 4:
        p[0] = [(p[1], p[2])] + p[3]
    else:
        p[0] = []


def p_parameter1(p):
    '''
    parameter1  : COMMA data_type ID parameter1
                | epsilon
    '''
    if len(p) == 5:
        p[0] = [(p[2], p[3])] + p[4]
    else:
        p[0] = []


def p_np_add_parameters_to_var_table(p):
    '''
    np_add_parameters_to_var_table : epsilon
    '''
    parameters = p[-1]
    for parameter in parameters:
        parameter_dt, parameter_name = parameter
        # Checar si el parametro ya existe
        if function_directory.has_variable(current_general_scope, current_internal_scope, parameter_name):
            raise ParamAlreadyDeclared(
                "Parameter '" + parameter_name + "' already declared in line " + str(p.lineno(1)))
        else:
            # pedimos memoria local
            param_address = avail.get_new_address(parameter_dt, 'locals')
            # Agregar variable a var table y agregar la firma de parametros
            function_directory.add_variable(
                current_general_scope, current_internal_scope, parameter_name, 'var', parameter_dt, param_address)
            function_directory.add_to_param_signature(
                current_general_scope, current_internal_scope, parameter_dt)


def p_conditional(p):
    '''
    conditional : IF OPEN_PARENTHESIS hyper_exp CLOSE_PARENTHESIS np_if_1 OPEN_KEY statement_loop CLOSE_KEY conditional1
    '''
    pass


def p_conditional1(p):
    '''
    conditional1    : ELSE np_if_3 OPEN_KEY statement_loop CLOSE_KEY np_if_2
                    | np_if_2
    '''
    pass


def p_np_if_1(p):
    '''
    np_if_1 : epsilon
    '''
    res_address, res_type = operand_stack.pop()
    if res_type != 'bool':
        raise TypeMismatchError(
            "Boolean expression expected and received " + res_type + " in line " + str(p.lineno(1)))
    else:
        quads.generate_quad('GOTOF', res_address, None, None)
        jump_stack.append(quads.counter - 1)


def p_np_if_2(p):
    '''
    np_if_2 : epsilon
    '''
    end_if = jump_stack.pop()
    quads.fill_quad(end_if, 3, quads.counter)


def p_np_if_3(p):
    '''
    np_if_3 : epsilon
    '''
    quads.generate_quad('GOTO', None, None, None)
    go_to_false_quad_id = jump_stack.pop()
    jump_stack.append(quads.counter - 1)
    quads.fill_quad(go_to_false_quad_id, 3, quads.counter)


def p_cycle(p):
    '''
    cycle   : FOR ID np_for_1 ASSIGN hyper_exp np_for_2 TO hyper_exp np_for_3 cycle_for
            | WHILE np_while_1 OPEN_PARENTHESIS hyper_exp CLOSE_PARENTHESIS np_while_2 cycle_while
            | DO np_do_while_1 OPEN_KEY statement_loop CLOSE_KEY WHILE OPEN_PARENTHESIS hyper_exp CLOSE_PARENTHESIS np_do_while_2 SEMICOLON
    '''
    pass


def p_cycle_for(p):
    '''
    cycle_for  : OPEN_KEY statement_loop CLOSE_KEY np_for_4
    '''
    pass


def p_np_for_1(p):
    '''
    np_for_1 : epsilon
    '''
    var_address = None
    var_data_type = None
    # Check existence for variable
    if not (function_directory.has_variable(current_general_scope, current_internal_scope, p[-1])):
        if not (function_directory.has_variable(current_general_scope, '#global', p[-1])):
            raise VariableNotDefined(
                "Variable " + p[-1] + " not defined in line " + str(p.lineno(1)))
        else:
            var_address = function_directory.get_variable_virtual_address(
                current_general_scope, '#global', p[-1])
            var_data_type = function_directory.get_variable_data_type(
                current_general_scope, '#global', p[-1])
    else:
        var_address = function_directory.get_variable_virtual_address(
            current_general_scope, current_internal_scope, p[-1])
        var_data_type = function_directory.get_variable_data_type(
            current_general_scope, current_internal_scope, p[-1])

    # Checar que el var_type de p[-1] sea int
    if var_data_type != 'int':
        raise Exception('Control variable ' +
                        p[-1] + ' should be of type int in line ' + str(p.lineno(1)))
    if var_address in control_variable_stack:
        raise Exception(
            "Changing the control variable " + p[-1] + " inside a for loop is invalid in line " + str(p.lineno(1)))
    else:
        operand_stack.append((var_address, 'int'))


def p_np_for_2(p):
    '''
    np_for_2 : epsilon
    '''
    exp_address, exp_type = operand_stack.pop()
    if exp_type != 'int':
        raise TypeMismatchError(
            "Expected int value but received " + exp_type + " in line " + str(p.lineno(1)))
    else:
        control_var_address, control_var_type = operand_stack[-1]
        control_variable_stack.append(control_var_address)
        result_type = semantic_cube.is_type_match(
            control_var_type, exp_type, '=')
        if result_type:
            quads.generate_quad('=', exp_address, None, control_var_address)
        else:
            error_msg = "No possible assignment between " + \
                control_var_type + " and " + result_type
            raise TypeMismatchError(error_msg + " in line " + str(p.lineno(1)))


def p_np_for_3(p):
    '''
    np_for_3 : epsilon
    '''
    exp_address, exp_type = operand_stack.pop()
    if exp_type != 'int':
        raise TypeMismatchError(
            "Expected int type but received " + exp_type + " in line " + str(p.lineno(1)))
    else:
        variable_final_address, _ = avail.get_new_temp('int')
        quads.generate_quad('=', exp_address, None, variable_final_address)
        new_temp_address, _ = avail.get_new_temp('bool')
        control_variable_address = control_variable_stack[-1]
        quads.generate_quad('<', control_variable_address,
                            variable_final_address, new_temp_address)
        jump_stack.append(quads.counter - 1)
        quads.generate_quad('GOTOF', new_temp_address, None, None)
        jump_stack.append(quads.counter - 1)


def p_np_for_4(p):
    '''
    np_for_4 : epsilon
    '''
    control_variable_address = control_variable_stack.pop()
    temp_address, _ = avail.get_new_temp('int')
    one_constant_address = constants.get_constant_address('int', '1')
    quads.generate_quad('+', control_variable_address,
                        one_constant_address, temp_address)
    quads.generate_quad('=', temp_address, None, control_variable_address)
    id_original_address, _ = operand_stack.pop()
    quads.generate_quad('=', temp_address, None, id_original_address)
    end_for = jump_stack.pop()
    return_for = jump_stack.pop()
    quads.generate_quad('GOTO', None, None, return_for)
    quads.fill_quad(end_for, 3, quads.counter)


def p_cycle_while(p):
    '''
    cycle_while  : OPEN_KEY statement_loop CLOSE_KEY np_while_3
    '''
    pass


def p_np_while_1(p):
    '''
    np_while_1 : epsilon
    '''
    jump_stack.append(quads.counter)


def p_np_while_2(p):
    '''
    np_while_2 : epsilon
    '''
    res_address, res_type = operand_stack.pop()
    if res_type != 'bool':
        raise TypeMismatchError(
            "Expected bool type but received " + res_type + " in line " + str(p.lineno(1)))
    else:
        quads.generate_quad('GOTOF', res_address, None, None)
        jump_stack.append(quads.counter - 1)


def p_np_while_3(p):
    '''
    np_while_3 : epsilon
    '''
    go_to_false_quad_id = jump_stack.pop()
    quad_id_to_return_to = jump_stack.pop()
    quads.generate_quad('GOTO', None, None, quad_id_to_return_to)
    quads.fill_quad(go_to_false_quad_id, 3, quads.counter)


def p_np_do_while_1(p):
    '''
    np_do_while_1 : epsilon
    '''
    jump_stack.append(quads.counter)


def p_np_do_while_2(p):
    '''
    np_do_while_2 : epsilon
    '''
    quad_id_to_return_to = jump_stack.pop()
    res_address, res_type = operand_stack.pop()
    if res_type != 'bool':
        raise TypeMismatchError(
            "Expected bool type but received " + res_type + " in line " + str(p.lineno(1)))
    else:
        quads.generate_quad('GOTOT', res_address, None, quad_id_to_return_to)


def p_read(p):
    '''
    read : READ OPEN_PARENTHESIS variable_loop CLOSE_PARENTHESIS SEMICOLON
    '''
    for variable in p[3]:
        variable_address, variable_type = variable
        # TODO: If variable address in variable stack raise error
        quads.generate_quad('READ', None, None, variable_address)


def p_variable_loop(p):
    '''
    variable_loop : variable variable_loop1
    '''
    p[0] = [p[1]] + p[2]


def p_variable_loop1(p):
    '''
    variable_loop1 : COMMA variable variable_loop1
                    | epsilon
    '''
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []


def p_write(p):
    '''
    write : WRITE OPEN_PARENTHESIS write_hyper_exp_loop CLOSE_PARENTHESIS SEMICOLON
    '''
    pass


def p_write_hyper_exp_loop(p):
    '''
    write_hyper_exp_loop : hyper_exp np_add_write_quad write_hyper_exp_loop1
    '''
    pass


def p_write_hyper_exp_loop1(p):
    '''
    write_hyper_exp_loop1 : COMMA hyper_exp np_add_write_quad write_hyper_exp_loop1
                    | epsilon

    '''
    pass


def p_np_add_write_quad(p):
    '''
    np_add_write_quad : epsilon
    '''
    operand_address, _ = operand_stack.pop()
    quads.generate_quad('WRITE', None, None, operand_address)


def p_hyper_exp_loop(p):
    '''
    hyper_exp_loop : hyper_exp hyper_exp_loop1
    '''
    pass


def p_hyper_exp_loop1(p):
    '''
    hyper_exp_loop1 : COMMA hyper_exp hyper_exp_loop1
                    | epsilon

    '''
    pass


def p_function_call(p):
    '''
    function_call : ID function_call1 OPEN_PARENTHESIS np_start_function_param_counter function_call2 CLOSE_PARENTHESIS
    '''
    param_signature_length = function_directory.get_param_signature_length(
        '#global', current_function_call_name)
    if param_signature_length != function_param_counter:
        error_msg = "'" + current_function_call_name + "'" + " function call expected " + \
            str(param_signature_length) + " params but received " + \
            str(function_param_counter)
        raise ParamLengthMismatch(error_msg + " in line " + str(p.lineno(6)))
    else:
        function_start_quad = function_directory.get_function_start_quad(
            '#global', current_function_call_name)
        quads.generate_quad(
            'GOSUB', current_function_call_name, None, function_start_quad)
        function_return_type = function_directory.get_function_type(
            '#global', current_function_call_name)
        if function_return_type != 'void':
            function_var_address = function_directory.get_function_virtual_address(
                '#global', '#global', current_function_call_name)
            new_temp_address, _ = avail.get_new_temp(function_return_type)
            p[0] = (new_temp_address, function_return_type)
            quads.generate_quad('=', function_var_address,
                                None, new_temp_address)


def p_function_call1(p):
    '''
    function_call1 : DOT ID
                    | np_validate_function_existance_and_era
    '''
    ...


def p_np_validate_function_existence_and_era(p):
    '''
    np_validate_function_existance_and_era : epsilon
    '''
    global current_function_call_name
    current_function_call_name = p[-1]
    # Checar si existe la funcion "global", luego soportaremos clases
    if not function_directory.has_internal_scope('#global', current_function_call_name):
        error_msg = "'" + current_function_call_name + "' function does not exist"
        raise FunctionNotDeclared(error_msg + " in line " + str(p.lineno(1)))
    else:
        quads.generate_quad('ERA', None, None, current_function_call_name)


def p_np_start_function_param_counter(p):
    '''
    np_start_function_param_counter : epsilon
    '''
    global function_param_counter
    function_param_counter = 0


def p_function_call2(p):
    '''
    function_call2 : function_hyper_exp_loop
                    | epsilon
    '''
    pass


def p_function_hyper_exp_loop(p):
    '''
    function_hyper_exp_loop : hyper_exp np_check_param_match function_hyper_exp_loop1
    '''
    pass


def p_function_hyper_exp_loop1(p):
    '''
    function_hyper_exp_loop1 : COMMA hyper_exp np_check_param_match function_hyper_exp_loop1
                    | epsilon

    '''
    pass


def p_np_check_param_match(p):
    '''
    np_check_param_match : epsilon
    '''
    global function_param_counter
    param_address, param_type = operand_stack.pop()
    nth_signature_type = function_directory.get_nth_param_type(
        '#global', current_function_call_name, function_param_counter)
    if nth_signature_type != param_type:
        error_msg = "Expected " + nth_signature_type + " type for " + \
            str(function_param_counter + 1) + "th param "
        error_msg += "in '" + current_function_call_name + \
            "' function call, but received " + param_type
        raise ParamTypeMismatch(error_msg + " in line " + str(p.lineno(1)))
    else:
        quads.generate_quad('PARAM', param_address,
                            None, function_param_counter)
        function_param_counter += 1


def p_class_function(p):
    '''
    class_function : AT_CLASS ID FUNCTION ID OPEN_PARENTHESIS parameter CLOSE_PARENTHESIS RETURNS return_arg OPEN_KEY function_statement_loop function_return CLOSE_KEY

    '''
    pass


def p_function_declaration(p):
    '''
    function_declaration : FUNCTION ID np_add_function_internal_scope OPEN_PARENTHESIS parameter np_add_parameters_to_var_table CLOSE_PARENTHESIS RETURNS return_arg np_set_function_return_type OPEN_KEY variable_declaration_loop np_generate_variable_workspace np_add_function_start_quad function_statement_loop function_return CLOSE_KEY np_end_function
    '''
    global current_internal_scope
    current_internal_scope = '#global'
    avail.reset_local_counters()


def p_np_generate_variable_workspace(p):
    '''
    np_generate_variable_workspace : epsilon
    '''
    function_directory.generate_variable_workspace(
        current_general_scope, current_internal_scope)


def p_np_add_function_start_quad(p):
    '''
    np_add_function_start_quad : epsilon
    '''
    function_directory.set_start_quad(
        current_general_scope, current_internal_scope, quads.counter)


def p_np_end_function(p):
    '''
    np_end_function : epsilon
    '''
    function_directory.delete_vars_table(
        current_general_scope, current_internal_scope)
    quads.generate_quad('ENDFUNC', None, None, None)
    temps_workspace = avail.get_counter_summary('temps')
    function_directory.set_temps_workspace(
        current_general_scope, current_internal_scope, temps_workspace)


def p_np_add_function_internal_scope(p):
    '''
    np_add_function_internal_scope : epsilon
    '''
    global current_internal_scope
    current_internal_scope = p[-1]
    function_directory.add_internal_scope(
        current_general_scope, current_internal_scope)


def p_np_set_function_return_type(p):
    '''
    np_set_function_return_type : epsilon
    '''
    function_directory.set_function_type(
        current_general_scope, current_internal_scope, p[-1])


def p_function_return(p):
    '''
    function_return : RETURN hyper_exp SEMICOLON
                    | RETURN SEMICOLON
    '''
    function_return_type = function_directory.table[
        current_general_scope][current_internal_scope]['function_type']
    if len(p) == 4:
        return_exp_address, return_exp_type = operand_stack.pop()
        if return_exp_type != function_return_type:
            error_msg = "Expected return type to be " + \
                function_return_type + " but received " + return_exp_type
            raise FunctionReturnError(
                error_msg + " in line " + str(p.lineno(3)))
        else:
            # TODO: Para apoyar a la recursion, pedir la direccion de esta funcion al inicio de la declaracion,
            # creo que no cambia nada el pedirla aqui, solo habria que hacer la query por la function address en este punto
            function_address = avail.get_new_global(function_return_type)
            function_directory.add_variable(
                '#global', '#global', current_internal_scope, 'var', function_return_type, function_address)
            quads.generate_quad('=', return_exp_address,
                                None, function_address)
    else:
        if function_return_type != 'void':
            error_msg = "Not returning the expected " + function_return_type
            raise FunctionReturnError(
                error_msg + " in line " + str(p.lineno(2)))


def p_function_statement_loop(p):
    '''
    function_statement_loop : statement_loop
                    | epsilon
    '''
    p[0] = p[1]


def p_epsilon(p):
    '''epsilon : '''
    p[0] = 'epsilon'


class SyntaxError(Exception):
    pass


class TypeMismatchError(Exception):
    ...


class FunctionReturnError(Exception):
    ...


class VariableNotDefined(Exception):
    pass


class FunctionNotDeclared(Exception):
    ...


class ParamTypeMismatch(Exception):
    ...


class ParamLengthMismatch(Exception):
    ...


class ParamAlreadyDeclared(Exception):
    ...


def p_error(p):
    if not p:
        error_msg = "Syntax error"
    else:
        error_msg = 'syntax error in line ' + \
            str(p.lineno) + ' when parsing ' + str(p)
    raise SyntaxError(error_msg)


parser = yacc.yacc()
