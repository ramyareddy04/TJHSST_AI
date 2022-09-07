import sys
import math
import numpy as np
import random
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

def step(num):
    return 1 if num > 0 else 0

def sigmoid(num):
    return pow(1+pow(math.e,-num),-1)

def perceptron(A, w, b, x):
    return A(dot(w,x) + b)

def check(n, w, b):
    tt = truth_table(len(w), n)
    accuracy = 0
    for val in tt:
        converted = []
        for ch in val[0]: converted.append(int(ch))
        if perceptron(step, w, b, converted) == int(val[1]): accuracy += 1
    return accuracy/len(tt)

def p_net(A, x, w_list, b_list):
    new_A = np.vectorize(A)
    a0 = x
    for layer in range(len(w_list[0])):
        a0 = new_A(a0@w_list[layer] + b_list[layer])
    return a0

if len(sys.argv) == 2:
    # XOR HAPPENS HERE
    w_list = [
                np.array([[-1, 1],[-2, 1]]),
                np.array([[1],[2]])
             ]
    b_list = [
                np.array([[3,0]]),
                np.array([[-2]])
             ]
    inp = list(ast.literal_eval(sys.argv[1]))
    print(p_net(step, np.array([[inp[0],inp[1]]]), w_list, b_list)[0][0])
elif len(sys.argv) == 3:
    w_list = [
                np.array([[1,1,-1,-1],[1,-1,1,-1]]),
                np.array([[1],[2],[3],[4]]) # og : <1,2,3,4>
             ]
    b_list = [
                np.array([[1,1,1,1]]),
                np.array([[-9]]) # og : -9
             ]
    print('Inside' if p_net(step, np.array([[float(sys.argv[1]),float(sys.argv[2])]]), w_list, b_list)[0][0]==1 else 'Outside')
else:
    x =[]
    y= [] 
    for i in range(500):
        x.append(random.uniform(-1, 1))
        y.append(random.uniform(-1, 1))
    w_list = [
                np.array([[1,1,-1,-1],[1,-1,1,-1]]),
                np.array([[1],[1],[1],[1]]) 
             ]
    b_list = [
                np.array([[2.090,2.090,2.090,2.090]]),
                np.array([[-3.410]])
             ]
    accuracy = 0
    bad = []
    for i in range(500):
        value = 1 if p_net(sigmoid, np.array([[x[i],y[i]]]), w_list, b_list)[0][0] > 0.5 else 0
        real = 1 if pow(x[i],2)+pow(y[i],2) < 1 else 0
        if value == real: accuracy += 1
        else: bad.append((x[i],y[i]))
    print("Misclassified: ",bad,"\nAccuracy:",str(accuracy/5)+'%')