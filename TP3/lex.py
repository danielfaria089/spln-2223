import ply.lex as lex

tokens=['ID','VAL','LINHA_B','ID_LING']
literals=['@','-','+',':']

def t_ID(t):
    r'[0-9]+'
    return t

def t_VAL(t):
    r'".*?"'
    return t

def t_LINHA_B(t):
    r'\n\s*\n'
    return t

def t_ID_LING(t):
    r'[a-zA-Z]*'
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore = ' \t'

lexer = lex.lex()