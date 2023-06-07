

"""
seven primitive operators:
atom, quote, eq, car, cdr, cons, cond

"""

binary_operators = set(['eq', '+','-','*','/','^'])
unary_operators = set(['atom', 'quote','`',])
list_operators = set(['car', 'cdr', 'cons', 'cond'])

def atom(x):
    if type(x) != list:
        return 't'
    return '()'

def quote(x):
    if x=='()':
        return ""
    return x

def eq(x,y):
    if x==y:
        return 't'
    return '()'

def car(x):
    if atom(x) != 't':
        return list(x[0])
    return '()'

def cdr(x):
    if atom(x) != 't':
        return x[1:]
    return '()'

def cons(x):
    if atom(x)=='t' and len(x)==1:
        return list(x)
    
    res = []
    _s = str(x)
    for c in _s.split():
        if c != '[' and c != ']' and c !='`':
            c = c.strip(",[]\"'")
            res.append(c)
        
    return res

def cond(plist):
    ret = '()'
    for p,e in plist:
        if atom(p) != 't' and _eval(p[0]) == 't':
            ret += e #TODO
    return '()'


"""
functions:
lambda, label
"""
def _lambda_(params, expr, args):
    for arg in args:
        if not atom(p):
            arg = _eval(arg)
    
    if len(arg) == len(params):
        pass


"""
***********************************
"""

def get_longest_valid_paren_str(s):
    if not s:
        return 0

    B = [0]*len(s)
    for i,c in enumerate(s):
        if c=='(' or i ==0:
            B[i] = 0
            continue
        mid_len = B[i-1]
        mirror = i-mid_len-1

        if mirror<0 or B[mirror]==')':
            B[i]=0
            continue
        if mirror>0:
            prefix = B[mirror-1]
        else:
            prefix = 0
        B[i] = prefix+mid_len+2

    return max(B)


def evaluate(expression):
    stack = []
    #import pdb
    #pdb.set_trace()
    for token in reversed(expression.split()):
        token = token.strip('(')
        token = token.rstrip(')')
        
        if token in unary_operators or token[0]=='`':
            if token[0]=='`':
                operand = token[1:]
                token=token[0]
            else:
                operand = stack.pop()
            operand = operand.rstrip(')')
            if token == 'atom':
                stack.append(atom(operand))
            elif token == 'quote' or token == '`':
                stack.append(quote(operand))

        elif token in binary_operators:
            operand1 = stack.pop()
            operand2 = stack.pop()
            
            if token == '+':
                stack.append(operand1 + operand2)
            elif token == '-':
                stack.append(operand1 - operand2)
            elif token == '*':
                stack.append(operand1 * operand2)
            elif token == '/':
                stack.append(operand1 / operand2)
            elif token == 'eq':
                stack.append(eq(operand1,operand2))
                
        elif token in list_operators:
            operands = []
            while stack :
                operands.append(stack.pop())
            if token == 'car':
                stack.append(car(operands))
            elif token == 'cdr':
                stack.append(cdr(operands))
            elif token == 'cons':
                stack.append(cons(operands))
            elif token == 'cond':
                stack.append(cond(operands))

                
        elif token.isdigit():
            stack.append(int(token))

        elif token.isalpha():
            stack.append(token)

        elif token == ')':
            sub_expression = ''
            while stack and stack[-1] != '(':
                sub_expression += stack.pop()
            stack.pop()  # Remove the '('

            # Evaluate the sub-expression and push the result onto the stack
            sub_result = evaluate(sub_expression)
            stack.append(sub_result)
            

    return stack.pop()



def execute(program):
    if type(program)!=str:
        return None

#    valid_str_len = get_longest_valid_paren_str(program)
#    print(valid_str_len,len(program))
#    if valid_str_len != len(program)-1:
#        return "Syntax Error - Parenthesis Mismatch"

    res = evaluate(program)
    
    print(res)
    return


""" OUTPUT

execute('(quote a)')
'a'
execute('(` a)')
'a'
execute('(eq (a a))')
't'

execute('(car (a b))')
'a'

execute('(cdr (x y))')
['y']

execute('(- 8 (* (+ 1 2) (- 9 7)))')
     
2

execute('(- 5 (+ 1 2))')
     
2


execute('(`a)')
a
execute('(cons `a)')
['a']
execute('(cons (car (x y)  cdr (a b)))')
['x']
execute('(cons (cdr (x y)  cdr (a b)))')
['y', 'b']
execute('(cons (x y) (a b))')
['x', 'y', 'a', 'b'] ==> Output to be like -> (x y a b) 
____________________________________________
wrong output - WIP


execute('(cons `a (cons `b (cons `c `())))')
['a', 'b', 'c', '('] ==> need to remove '('
execute('(car (cons `a `(b,c)))')
['a', '(b,c']
execute('(cdr (cons `a `(b,c)))')
[]  ==> wrong output , correct output -> (b c)

"""
