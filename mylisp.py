



code = "(+ (* (^ (d) 1) 2) 6)"


def atom(token):
	pass
	


def parse(tokens):
 	if len(tokens) == 0:
		return None	
	token = tokens.pop(0)
	L = []
	if '(' == token:
		while (True):
			token = parse(tokens)
			if token == None:
				print "Error while parsing input"
				return None
			if token == ')':
				return L
			L.append(token)
	else:
		return token


while True:
	print "myList>",
	code = raw_input()
	if code:
		tokens  = code.replace('(',' ( ').replace(')',' ) ').split()
		import pdb
#		pdb.set_trace()
		op  = parse(tokens)
		if op != None:
			print op
