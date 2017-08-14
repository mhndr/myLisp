



code = "(+ (* 5 2) 6)"


def parse(tokens):
 	if len(tokens) == 0:
		return None	
	token = tokens.pop(0)
	L = []
	if '(' == token:
		while (True):
			token = parse(tokens)
			if token == ')':
				return L
			L.append(token)
	else:
		return token
	



tokens  = code.replace('(',' ( ').replace(')',' ) ').split()
import pdb
#pdb.set_trace()
op  = parse(tokens)
print op
