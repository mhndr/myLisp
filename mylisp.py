
import re
import pdb 

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

def split(delimiters, string, maxsplit=0):
    import re
    regex_pattern = '|'.join(map(re.escape, delimiters))
    return re.split(regex_pattern, string, maxsplit)


def evaluate(expression):
    stack = []
    #pdb.set_trace()
    delimiters = '(',')',',',' ','`'
    expression = split(delimiters,expression)
    for token in reversed(expression):
        if token == '' or token == ',':
            continue
        
        if token in unary_operators or token[0]=='`':
            operands = []
            while stack :
                operands.append(stack.pop())
            if token == 'atom':
                stack.append(atom(operands))
            elif token == 'quote' or token == '`':
                stack.append(quote(operands))

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
                ret = car(operands)
                stack.append(ret)
            elif token == 'cdr':
                ret = cdr(operands)
                stack.append(ret)
            elif token == 'cons':
                ret = cons(operands)
                stack.append(ret)
            elif token == 'cond':
                ret = cond(operands)
                stack.append(ret)

                
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
            
    ret =" ".join(stack.pop())
    ret = "("+ret+")" 
    return ret



def execute(program):
    if type(program)!=str:
        return None

    #valid_str_len = get_longest_valid_paren_str(program)
    #if valid_str_len != len(program):
    #    return "Syntax Error - Parenthesis Mismatch"

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
     execute('(cdr (x y))')
2

execute('(- 5 (+ 1 2))')
     
2

execute('(car (cons `a `(b,c)))')
['a', '(b,c']
execute('(car (cons `a `(b,c))')
'Syntax Error - Parenthesis Mismatch'

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
