from function_directory import FunctionDirectory
from avail import Avail
from quadruples import Quadruples
from semantic_cube import SemanticCube
import ply.yacc as yacc
from lexer import tokens

import json

# TODO: Hacer cuadruplos de las funciones 
# TODO: Agregar variable global con el nombre de la funcion
# TODO: Agregar parametros a la vars table de cada funcion
# TODO: checar existencia de funciones
# TODO: Usar direcciones para todo
# TODO: Resolver discrepancia entre que los cuadruplos que usen variables temporales, a veces usamos tupla y en otras veces no
# TODO: Arreglar return de funciones (podemos usar current scopes para saber el tipo de la función y checar el match)
# TODO: Hacer tabla de constantes y asignar memoria

function_directory = None
avail = None
quads = None
semantic_cube = None
operand_stack = None
operator_stack = None
jump_stack = None
control_variable_stack = None

current_general_scope = None
current_internal_scope = None
current_var_name = None
current_var_type = None
current_var_data_type = None


def p_program(p):
    '''
    program : PROGRAM np_start_state np_start_func_dir ID SEMICOLON declaration_loop main_function
    '''
    #print(json.dumps(function_directory.table, indent=2))
    print(quads.list)
    pass


def p_main_function(p):
    '''
    main_function : MAIN np_add_main_internal_scope OPEN_PARENTHESIS CLOSE_PARENTHESIS OPEN_KEY variable_declaration_loop statement_loop CLOSE_KEY
    '''


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


def p_np_start_state(p):
    '''
    np_start_state : epsilon
    '''
    global function_directory, avail, quads, semantic_cube, operand_stack, operator_stack, jump_stack, control_variable_stack
    global current_general_scope, current_internal_scope, current_var_name, current_var_type, current_var_data_type
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
    if (function_directory.has_variable(current_general_scope, current_internal_scope, p[1])):
        variable_map = function_directory.table[current_general_scope][current_internal_scope]['vars_table'][p[1]]
        variable_address, variable_data_type = variable_map[
            'var_virtual_address'], variable_map['var_data_type']
        p[0] = (variable_address, variable_data_type)
    elif (function_directory.has_variable(current_general_scope, '#global', p[1])):
        variable_map = function_directory.table[current_general_scope]['#global']['vars_table'][p[1]]
        variable_address, variable_data_type = variable_map[
            'var_virtual_address'], variable_map['var_data_type']
        p[0] = (variable_address, variable_data_type)
    else:
        raise VariableNotDefined()


def p_variable1(p):
    '''
    variable1   : OPEN_BRACKET hyper_exp CLOSE_BRACKET
                | DOT ID
                | epsilon

    '''
    pass


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
                            | GROUP np_set_current_var_type ID np_set_current_var_name ASSIGN data_type np_set_current_var_data_type OPEN_BRACKET INT_VALUE CLOSE_BRACKET SEMICOLON np_add_variable
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


def p_variable_declaration1(p):
    '''
    variable_declaration1   : hyper_exp_loop
                            | epsilon
    '''


def p_statement(p):
    '''
    statement   : assignment
                | conditional
                | cycle
                | read
                | write
                | function_call
    '''
    p[0] = p[1]
    pass


def p_assignment(p):
    '''
    assignment  : variable ASSIGN hyper_exp SEMICOLON
    '''
    var_value, var_type = p[1]
    exp_value, exp_type = operand_stack.pop()
    result_type = semantic_cube.is_type_match(var_type, exp_type, '=')
    if result_type:
        quads.generate_quad('=', exp_value, None, var_value)
    else:
        raise TypeMismatchError()


def p_np_add_operator(p):
    '''
    np_add_operator : epsilon
    '''
    operator_stack.append(p[-1])


def p_hyper_exp(p):
    '''
    hyper_exp   : super_exp np_hyper_exp hyper_exp1
    '''
    pass


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
    add_exp_quad(['&&', '||'])


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
    add_exp_quad(['>', '<', '==', '!='])


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
    add_exp_quad(['+', '-'])


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
    add_exp_quad(['*', '/'])


def add_exp_quad(operator_list):
    if operator_stack and operator_stack[-1] in operator_list:
        ro_value, ro_type = operand_stack.pop()
        lo_value, lo_type = operand_stack.pop()
        operator = operator_stack.pop()
        result_type = semantic_cube.is_type_match(lo_type, ro_type, operator)
        if result_type:
            new_temp = avail.get_new_temp(result_type)
            quads.generate_quad(operator, lo_value, ro_value, new_temp)
            operand_stack.append(new_temp)
        else:
            raise TypeMismatchError()


def p_factor(p):
    '''
    factor  : function_call
            | FLOAT_VALUE
            | INT_VALUE
            | BOOL_VALUE
            | STRING_VALUE
            | variable
            | OPEN_PARENTHESIS np_add_open_parenthesis hyper_exp CLOSE_PARENTHESIS np_remove_open_parenthesis
    '''
    if len(p) == 2:
        temp_tuple = p[1]
        operand_stack.append(temp_tuple)


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
            print('Parametro doblemente declarado')
            # TODO: Raise error
        else:
            # pedimos memoria local
            param_address = avail.get_new_address(parameter_dt, 'locals')
            # Agregar variable a var table y agregar la firma de parametros
            function_directory.add_variable(current_general_scope, current_internal_scope, parameter_name, 'var', parameter_dt, param_address)
            function_directory.add_to_param_signature(current_general_scope, current_internal_scope, parameter_dt)

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
        raise TypeMismatchError()
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
    # Check existence for variable
    if not (function_directory.has_variable(current_general_scope, current_internal_scope, p[-1])):
        if not (function_directory.has_variable(current_general_scope, '#global', p[-1])):
            raise VariableNotDefined()
        # else get variable address
    var_address = p[-1]
    # TODD: Checar que el var_type de p[-1] sea int
    operand_stack.append((var_address, 'int'))


def p_np_for_2(p):
    '''
    np_for_2 : epsilon
    '''
    exp_address, exp_type = operand_stack.pop()
    if exp_type != 'int':
        raise TypeMismatchError()
    else:
        control_var_address, control_var_type = operand_stack[-1]
        control_variable_stack.append((control_var_address, control_var_type))
        result_type = semantic_cube.is_type_match(
            control_var_type, exp_type, '=')
        if result_type:
            quads.generate_quad('=', exp_address, None, control_var_address)
        else:
            raise TypeMismatchError()


def p_np_for_3(p):
    '''
    np_for_3 : epsilon
    '''
    exp_address, exp_type = operand_stack.pop()
    if exp_type != 'int':
        raise TypeMismatchError()
    else:
        variable_final_address, _ = avail.get_new_temp('int')
        quads.generate_quad('=', exp_address, None, variable_final_address)
        new_temp_address, new_temp_type = avail.get_new_temp('bool')
        control_variable_address, _ = control_variable_stack[-1]
        quads.generate_quad('<', control_variable_address,
                            variable_final_address, (new_temp_address, new_temp_type))
        jump_stack.append(quads.counter - 1)
        quads.generate_quad('GOTOF', new_temp_address, None, None)
        jump_stack.append(quads.counter - 1)


def p_np_for_4(p):
    '''
    np_for_4 : epsilon
    '''
    control_variable_address, _ = control_variable_stack.pop()
    new_temp = avail.get_new_temp('int')
    # TODO: Pedir temporal de constante 1
    quads.generate_quad('+', control_variable_address, 1, new_temp)
    quads.generate_quad('=', new_temp[0], None, control_variable_address)
    id_original_address, _ = operand_stack.pop()
    quads.generate_quad('=', new_temp[0], None, id_original_address)
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
        raise TypeMismatchError()
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
        raise TypeMismatchError()
    else:
        quads.generate_quad('GOTOT', res_address, None, quad_id_to_return_to)


def p_read(p):
    '''
    read : READ OPEN_PARENTHESIS variable_loop CLOSE_PARENTHESIS SEMICOLON
    '''
    for variable in p[3]:
        quads.generate_quad('READ', None, None, variable)


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
    operand_tuple = operand_stack.pop()  # TODO: Check further what to do with the type
    quads.generate_quad('WRITE', None, None, operand_tuple)


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
    function_call : ID function_call1 OPEN_PARENTHESIS function_call2 CLOSE_PARENTHESIS SEMICOLON
    '''
    p[0] = ("Function call " + p[1], 'string')


def p_function_call1(p):
    '''
    function_call1 : DOT ID
                    | epsilon
    '''
    pass


def p_function_call2(p):
    '''
    function_call2 : hyper_exp_loop
                    | epsilon
    '''
    pass


def p_class_function(p):
    '''
    class_function : AT_CLASS ID FUNCTION ID OPEN_PARENTHESIS parameter CLOSE_PARENTHESIS RETURNS return_arg OPEN_KEY function_statement_loop function_return CLOSE_KEY

    '''
    pass


def p_function_declaration(p):
    '''
    function_declaration : FUNCTION ID np_add_function_internal_scope OPEN_PARENTHESIS parameter np_add_parameters_to_var_table CLOSE_PARENTHESIS RETURNS return_arg np_set_function_return_type OPEN_KEY variable_declaration_loop np_generate_variable_workspace np_add_function_start_quad function_statement_loop function_return CLOSE_KEY
    '''
    global current_internal_scope
    current_internal_scope = '#global'
    avail.reset_local_counters()

def p_np_generate_variable_workspace(p):
    '''
    np_generate_variable_workspace : epsilon
    '''
    function_directory.generate_variable_workspace(current_general_scope, current_internal_scope)
    
def p_np_add_function_start_quad(p):
    '''
    np_add_function_start_quad : epsilon
    '''
    function_directory.set_start_quad(current_general_scope, current_internal_scope, quads.counter)

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
                    | epsilon
    '''
    pass


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
    pass


class VariableNotDefined(Exception):
    pass


def p_error(p):
    print('syntax error', p)
    raise SyntaxError


parser = yacc.yacc()
