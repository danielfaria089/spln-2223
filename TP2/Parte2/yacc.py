import ply.yacc as yacc
from lex import tokens
import sys

def p_1(p): 
    "dic : es"
    pass

def p_2(p): 
    "es : es LINHA_B e"
    p[0]=p[1]+[p[3]]

def p_3(p): 
    "es : e"
    p[0]=p[1]

def p_4(p): 
    "e : items"
    p[0]=p[1]

def p_5(p): 
    r"items : items item"
    p[0]=p[1]+[p[2]]

def p_6(p): 
    "items : item"
    p[0]=p[1]

def p_7(p): 
    "item : '@' ling"
    p[0]=p[2]

def p_8(p): 
    "item : at_conc"
    p[0]=p[1]

def p_9(p): 
    "ling : ID_LING ':' ts"
    p[0]={p[1]:p[3]}

def p_10(p): 
    "at_conc : ID ':' VAL"
    p[0]={p[1]:p[3]}

def p_11(p): 
    r"ts : ts t"
    p[0]=p[1]+[p[2]]

def p_12(p): 
    "ts : t"
    p[0]=p[1]

def p_13(p): 
    r"t : '-' VAL at_ts"
    p[0]={p[1]:p[2]}

def p_14(p): 
    "at_ts : at_ts at_t"
    p[0]=p[1]+[p[2]]

def p_15(p): 
    "at_ts : "

def p_16(p): 
    r"at_t : '+' ID ':' VAL"
    p[0]={p[2]:p[4]}


# Syntatic Error handling rule
def p_error(p):
    print('Syntax error: ', p)


# Build the parser
parser = yacc.yacc(debug=True)

# Read the input file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = 'input.txt'
