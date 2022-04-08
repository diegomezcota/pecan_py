# ------------------------------------------------------------
# lexer.py
#
# tokenizer for PecanPy expression evaluator
# ------------------------------------------------------------

import ply.lex as lex

# List of token names.   This is always required
tokens = [
    'ID',
    'SEMICOLON',
    'OPEN_PARENTHESIS',
    'CLOSE_PARENTHESIS',
    'OPEN_KEY',
    'CLOSE_KEY',
    'COMMA',
    'ASSIGN',
    'OPEN_BRACKET',
    'CLOSE_BRACKET',
    'INT_VALUE',
    'AND',
    'OR',
    'PLUS',
    'MINUS',
    'MULTIPLICATION',
    'DIVISION',
    'GREATER_THAN',
    'LESS_THAN',
    'EQUAL_TO',
    'NOT_EQUAL_TO',
    'FLOAT_VALUE',
    'STRING_VALUE',
    'BOOL_VALUE',
    'DOT',
    'AT_CLASS'
]

# Regular expression rules for simple tokens

# Reserved words
reserved = {
    'program' : 'PROGRAM',
    'main' : 'MAIN',
    'class' : 'CLASS',
    'is' : 'IS',
    'constructor' : 'CONSTRUCTOR',
    'var' : 'VAR',
    'group' : 'GROUP',
    'int' : 'INT',
    'float' : 'FLOAT',
    'string' : 'STRING',
    'bool' : 'BOOL',
    'function' : 'FUNCTION',
    'returns' : 'RETURNS',
    'void' : 'VOID',
    'if' : 'IF',
    'else' : 'ELSE',
    'read' : 'READ',
    'write' : 'WRITE',
    'for' : 'FOR',
    'in' : 'IN',
    'while' : 'WHILE',
    'return' : 'RETURN'
}

tokens += list(reserved.values())

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n'