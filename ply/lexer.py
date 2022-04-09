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
t_SEMICOLON         = r';'
t_OPEN_PARENTHESIS  = r'\('
t_CLOSE_PARENTHESIS = r'\)'
t_OPEN_KEY          = r'{'
t_CLOSE_KEY         = r'}'
t_COMMA             = r','
t_ASSIGN            = r'='
t_OPEN_BRACKET      = r'\['
t_CLOSE_BRACKET     = r'\]'
t_AND               = r'&&'
t_OR                = r'\|\|'
t_PLUS              = r'\+'
t_MINUS             = r'-'
t_MULTIPLICATION    = r'\*'
t_DIVISION          = r'/'
t_GREATER_THAN      = r'>'
t_LESS_THAN         = r'<'
t_EQUAL_TO          = r'=='
t_NOT_EQUAL_TO      = r'!='
t_DOT               = r'\.'
t_AT_CLASS          = r'@class'

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
    'return' : 'RETURN',
    'obj' : 'OBJ'
}

tokens += list(reserved.values())

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n'
t_ignore_COMMENT = r'//.*'

# ID check for reserved words
def t_BOOL_VALUE(t):
    r'true|false'
    t.type = reserved.get(t.value, 'BOOL_VALUE')
    return t
    

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_FLOAT_VALUE(t):
    r'[0-9]+\.[0-9]+'
    t.type = reserved.get(t.value, 'FLOAT_VALUE')
    return t

def t_INT_VALUE(t):
    r'[0-9]+'
    t.type = reserved.get(t.value, 'INT_VALUE')
    return t

def t_STRING_VALUE(t):
    r'".*"'
    t.type = reserved.get(t.value, 'STRING_VALUE')
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
lexer = lex.lex()