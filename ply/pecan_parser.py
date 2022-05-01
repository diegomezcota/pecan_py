from function_directory import FunctionDirectory
from avail import Avail
from quadruples import Quadruples
from ast import Pass
import ply.yacc as yacc
from lexer import tokens

import json

function_directory = FunctionDirectory()
avail = Avail()
quads = Quadruples()
operand_stack = []
operator_stack = []

# TODO: main scope and their variables, meternos al los statements
# ideas: main function part be their own function to add to the function directory in an easier way
# class scope:
#   class_scopes: {function_name -> function_type, vars_table}
# scopes
#   global
#   functions
#   main
#   class
#       name -> function
# to fix? no permitir que una funcion se llame "global", o guardarla como 0_global o algo así que sea imposible llamarse
# TODO: Check how are the function parameters handled


def p_program(p):
    '''
    program : PROGRAM np_start_func_dir ID SEMICOLON declaration_loop main_function
    '''
    #print(json.dumps(function_directory.table, indent=2))
    print(operator_stack)
    print(operand_stack)
    pass


def p_main_function(p):
    '''
    main_function : MAIN OPEN_PARENTHESIS CLOSE_PARENTHESIS OPEN_KEY variable_declaration_loop statement_loop CLOSE_KEY
    '''
    function_directory.add_function_with_variables(
        function_variables=p[5], function_name=p[1], function_type='void')


def p_np_start_func_dir(p):
    '''
    np_start_func_dir : epsilon
    '''
    global function_directory
    function_directory.init_global_scope()


def p_declaration_loop(p):
    '''
    declaration_loop : declaration declaration_loop
                     | epsilon
    '''
    # Up to this point, we know we are in global scope
    if len(p) == 3:
        # If the declaration is a variable one
        if p[1] and p[1][0] == 'variable_declaration':
            function_directory.add_global_variable(declaration=p[1])


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
    p[0] = ("Variable " + p[1], 'string')


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
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_variable_declaration(p):
    '''
    variable_declaration    : VAR data_type ID SEMICOLON
                            | GROUP ID ASSIGN data_type OPEN_BRACKET INT_VALUE CLOSE_BRACKET SEMICOLON
                            | OBJ ID ASSIGN ID OPEN_PARENTHESIS variable_declaration1 CLOSE_PARENTHESIS SEMICOLON

    '''
    # Return info related to each variable type (var_type, data_type, ID)
    if p[1] == 'var':
        p[0] = ('variable_declaration', p[1], p[2], p[3])
    elif p[1] == 'group':
        p[0] = ('variable_declaration', p[1], p[4], p[2])
    else:
        p[0] = ('variable_declaration', p[1], p[4], p[2])


def p_var_type(p):
    '''
    var_type    : VAR
                | GROUP
                | OBJ
    '''
    p[0] = p[1]


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
    pass


def p_hyper_exp(p):
    '''
    hyper_exp   : super_exp hyper_exp1
    '''
    pass


def p_hyper_exp1(p):
    '''
    hyper_exp1  : AND super_exp hyper_exp1
                | OR super_exp hyper_exp1
                | epsilon
    '''
    pass


def p_super_exp(p):
    '''
    super_exp   : exp super_exp1
    '''
    pass


def p_super_exp1(p):
    '''
    super_exp1  : GREATER_THAN exp super_exp1
                | LESS_THAN exp super_exp1
                | EQUAL_TO exp super_exp1
                | NOT_EQUAL_TO exp super_exp1
                | epsilon
    '''
    pass


def p_exp(p):
    '''
    exp : term exp1
    '''
    pass


def p_exp1(p):
    '''
    exp1    : PLUS term exp1
            | MINUS term exp1
            | epsilon
    '''
    pass


def p_term(p):
    '''
    term    : factor term1
    '''
    pass


def p_term1(p):
    '''
    term1   : MULTIPLICATION factor term1
            | DIVISION factor term1
            | epsilon
    '''
    pass


def p_factor(p):
    '''
    factor  : function_call
            | FLOAT_VALUE
            | INT_VALUE
            | BOOL_VALUE
            | STRING_VALUE
            | variable
            | OPEN_PARENTHESIS hyper_exp CLOSE_PARENTHESIS
    '''
    if len(p) == 2:
        temp_tuple = p[1]
        operand_stack.append(temp_tuple)
    else:
        print('aucsilio')


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
    parameter   : var_type data_type ID parameter1
                | epsilon
    '''
    if len(p) == 5:
        p[0] = [(p[1], p[2])] + p[3]
    else:
        p[0] = []


def p_parameter1(p):
    '''
    parameter1  : COMMA var_type data_type ID parameter1
                | epsilon
    '''
    if len(p) == 6:
        p[0] = [(p[2], p[3])] + p[4]
    else:
        p[0] = []


def p_conditional(p):
    '''
    conditional : IF OPEN_PARENTHESIS hyper_exp CLOSE_PARENTHESIS OPEN_KEY statement_loop CLOSE_KEY conditional1
    '''
    pass


def p_conditional1(p):
    '''
    conditional1    : ELSE OPEN_KEY statement_loop CLOSE_KEY
                    | epsilon
    '''
    pass


def p_cycle(p):
    '''
    cycle   : FOR OPEN_PARENTHESIS ID IN ID CLOSE_PARENTHESIS cycle1
            | WHILE OPEN_PARENTHESIS hyper_exp CLOSE_PARENTHESIS cycle1
    '''
    pass


def p_cycle1(p):
    '''
    cycle1  : OPEN_KEY statement_loop CLOSE_KEY
    '''
    pass


def p_read(p):
    '''
    read    : READ OPEN_PARENTHESIS variable_loop CLOSE_PARENTHESIS SEMICOLON
    '''
    pass


def p_variable_loop(p):
    '''
    variable_loop   : variable variable_loop1
    '''
    pass


def p_variable_loop1(p):
    '''
    variable_loop1  : COMMA variable variable_loop1
                    | epsilon
    '''
    pass


def p_write(p):
    '''
    write   : WRITE OPEN_PARENTHESIS hyper_exp_loop CLOSE_PARENTHESIS SEMICOLON
    '''
    pass


def p_hyper_exp_loop(p):
    '''
    hyper_exp_loop  : hyper_exp hyper_exp_loop1
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
    function_call   : ID function_call1 OPEN_PARENTHESIS function_call2 CLOSE_PARENTHESIS SEMICOLON
    '''
    p[0] = ("Function call " + p[1], 'string')


def p_function_call1(p):
    '''
    function_call1  : DOT ID
                    | epsilon
    '''
    pass


def p_function_call2(p):
    '''
    function_call2  : hyper_exp_loop
                    | epsilon
    '''
    pass


def p_class_function(p):
    '''
    class_function  : AT_CLASS ID FUNCTION ID OPEN_PARENTHESIS parameter CLOSE_PARENTHESIS RETURNS return_arg OPEN_KEY function_statement_loop function_return CLOSE_KEY

    '''
    pass


def p_function_declaration(p):
    '''
    function_declaration    : FUNCTION ID OPEN_PARENTHESIS parameter CLOSE_PARENTHESIS RETURNS return_arg OPEN_KEY variable_declaration_loop function_statement_loop function_return CLOSE_KEY
    '''
    function_directory.add_function_with_variables(
        function_variables=p[9], function_name=p[2], function_type=p[7])


def p_function_return(p):
    '''
    function_return : RETURN hyper_exp SEMICOLON
                    | epsilon
    '''
    pass


def p_function_statement_loop(p):
    '''
    function_statement_loop  : statement_loop
                    | epsilon
    '''
    p[0] = p[1]


def p_epsilon(p):
    '''epsilon :'''
    p[0] = 'epsilon'


class SyntaxError(Exception):
    pass


def p_error(p):
    print('syntax error', p)
    raise SyntaxError


parser = yacc.yacc()
