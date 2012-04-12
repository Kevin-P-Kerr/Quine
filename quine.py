
reserved = { 'U' : 'ALL', 'E' : 'EXIST', 'in' : 'ISIN',} #'Q' : 'QUERY' }  
tokens = list(reserved.values()) + ['LPAREN', 'RPAREN', 'VAR', 'QUERY' ]

t_ignore = ' \t'

t_QUERY = r'\?'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def  t_VAR(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value, 'VAR')
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")

def t_error(t):
	print("ILLEGAL CHARACTER %s" % t.value[0])
	t.lex.skip[1]

import ply.lex as lex
lex.lex()


def p_statementu(p):
	'statement : ALL LPAREN VAR RPAREN ISIN VAR'
	p[0] = (p[1], p[3], p[6])

def p_statemente(p):
	'statement : EXIST LPAREN VAR RPAREN ISIN VAR'
	p[0] = (p[1], p[3], p[6])

def p_statementq(p):
	'statement : QUERY LPAREN VAR RPAREN ISIN VAR'
 	p[0] = (p[1], p[3], p[6])

# define eval
global_env = {}

exist_env = {}

def eval(x):
	if x[0] == 'U' : 
		global_env[x[1]] = x[2]
		print("ACCEPTED")
	elif x[0] == 'E':
		 exist_env[x[1]] = x[2]
		 print("ACCEPTED")
	elif x[0] == '?' : checkeval(x[1], x[2]) #print("THIS WORKS") #checkeval(x[1], x[2]) 
	else:
		print("EVAL ERROR")


def checkeval(x, y):
	if exist_env[x] == y : print("TRUE")
	else:
		 checkglobalenv(y, exist_env[x])

def checkglobalenv(y, z):
	if z not in global_env : print("FALSE")
	elif y == global_env[z] : print("TRUE")
	else:
		tmp = global_env[z]
		z = tmp
		checkglobalenv(y, z)
#build it
import ply.yacc as yacc 

#build the parser
parser = yacc.yacc()

while True:
	try:
		s = raw_input('quine => ')
	except EOFError:
		break
	if not s: continue
	result = parser.parse(s)
	eval(result)




