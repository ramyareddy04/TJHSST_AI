import sys
import math
import ast

def convert(bits, n):
    result = ['0' for i in range(bits)]
    while(n!=0):
        result[math.trunc(math.log(n, 2))] = '1'
        n -= 2**math.trunc(math.log(n, 2))
    return ''.join(result)[::-1]
        
def truth_table(bits, n):
    truth = []
    integerRep = convert(2**bits, n)
    for i in range(2**bits-1, -1, -1):
        inp = convert(bits, i)
        out = integerRep[2**bits-i-1]
        truth.append([inp, out])
    return truth

def pretty_print_tt(table):
    numInp = len(table[0][0])
    s = ''
    for i in range(1, numInp+1): s += 'In' + str(i) + ' '
    s += '| Out\n'
    n = len(s) - 1
    for i in range(n-5): s+= '-'
    s += '|'
    for i in range(n-4, n): s+= '-'
    s += '\n'
    for val in table:
        for inp in val[0]: s+= ' ' + str(inp) + '  '
        s += '|  ' + str(val[1]) + '\n'
    return s[:-1]

def dot(mat1, mat2):
    return sum([mat1[i]*mat2[i] for i in range(len(mat1))])

def add(mat1, mat2):
    return [mat1[i]+mat2[i] for i in range(len(mat1))]

def scale(n, mat1):
    return [val*n for val in mat1]

def step(num, b):
    return 1 if num > -b else 0

def perceptron(A, w, b, x):
    return A(dot(w,x), b)

def check(n, w, b):
    tt = truth_table(len(w), n)
    accuracy = 0
    for val in tt:
        converted = []
        for ch in val[0]: converted.append(int(ch))
        if perceptron(step, w, b, converted) == int(val[1]): accuracy += 1
    return accuracy/len(tt)

# XOR HAPPENS HERE
def xor_function(in1, in2):
    p1 = perceptron(step, [-1,-2], 3, [in1, in2])
    p2 = perceptron(step, [1,1], 0, [in1, in2])
    return perceptron(step, [1,2], -2, [p1, p2])

inp = list(ast.literal_eval(sys.argv[1]))
print(xor_function(inp[0], inp[1]))