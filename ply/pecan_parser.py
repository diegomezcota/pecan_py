from ast import Pass
import ply.yacc as yacc
from lexer import tokens

import json

function_directory = {}


def p_program(p):
    '''
    program : PROGRAM np_start_func_dir ID SEMICOLON declaration_loop MAIN OPEN_PARENTHESIS CLOSE_PARENTHESIS OPEN_KEY statement_loop CLOSE_KEY
    '''
    print (json.dumps(function_directory, indent=2))
    pass


def p_np_start_func_dir(p):
    '''
    np_start_func_dir : epsilon
    '''
    function_directory["global"] = {"function_type": "void", "vars_table": {}}
    pass


def p_declaration_loop(p):
    '''
    declaration_loop : declaration declaration_loop
                     | epsilon
    '''
    # Up to this point, we know we are in global scope
    if len(p) == 3:
        # If the declaration is a variable one
        if p[1] and p[1][0] == 'variable_declaration':
            _, var_type, var_data_type, var_name = p[1]
            function_directory['global']['vars_table'][var_name] = {'var_data_type' : var_data_type, 'var_type' : var_type}
    pass


def p_statement_loop(p):
    '''
    statement_loop  : statement statement_loop1
    '''
    pass


def p_statement_loop1(p):
    '''
    statement_loop1 : statement statement_loop1
                    | epsilon
    '''
    pass


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
    pass


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
                | variable_declaration
    '''
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
    hyper_exp1  : AND super_exp
                | OR super_exp
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
    super_exp1  : GREATER_THAN exp
                | LESS_THAN exp
                | EQUAL_TO exp
                | NOT_EQUAL_TO exp
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
    pass


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
    pass


def p_parameter(p):
    '''
    parameter   : data_type ID parameter1
                | epsilon
    '''
    pass


def p_parameter1(p):
    '''
    parameter1  : COMMA data_type ID parameter1
                | epsilon
    '''
    pass


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
    pass


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
    function_declaration    : FUNCTION ID OPEN_PARENTHESIS parameter CLOSE_PARENTHESIS RETURNS return_arg OPEN_KEY function_statement_loop function_return CLOSE_KEY
    '''
    pass


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
    pass


def p_epsilon(p):
    '''epsilon :'''
    pass


class SyntaxError(Exception):
    pass


def p_error(p):
    print('syntax error', p)
    raise SyntaxError


parser = yacc.yacc()
