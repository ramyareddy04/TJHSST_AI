from matplotlib import pyplot as plt

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

def stabilize(n, w, b):
    tt = truth_table(len(w), n)
    epoch = 1
    isNotSame = True
    lr = 1
    while isNotSame and epoch != 101:
        for i in range(len(tt)):
            converted = [int(ch) for ch in tt[i][0]]
            f_curr = perceptron(step, w, b, converted)
            w = add(w, scale((int(tt[i][1])-f_curr)*lr, converted))
            b = b + (int(tt[i][1])-f_curr)*lr
            if i == len(tt) - 1:
                if epoch != 1:
                    if w == lastW and b == lastB:
                        isNotSame = False
                if isNotSame:
                    lastW = w
                    lastB = b
                    epoch += 1                
    return w, b

def iterate(w, b, x0, xf, dif):
    i = x0
    x = []
    y = []
    color = []
    while i < xf + dif:
        j = x0
        while j < xf + dif:
            x.append(i)
            y.append(j)
            value = perceptron(step, w, b, [i, j])
            color.append('#FF0000' if value == 0 else '#00FF00')
            j += dif
        i += dif
    return x, y, color

def all_graphs():
    n = 2
    figure, axis = plt.subplots(4, 4)
    for i in range(2**(2**n)):
        w = [0  for j in range(n)]
        b = 0
        w, b = stabilize(i, w, b)
        r = i//4
        c = i%4
        j = -2
        axis[r,c].axhline(0, color='black')
        axis[r,c].axvline(0, color='black')
        x, y, color = iterate(w, b, -2, 2, 0.1)
        axis[r,c].scatter(x, y, s=1, color=color)
        tt = truth_table(len(w), i)
        for true_val in tt:
            color = '#FF0000' if int(true_val[1]) == 0 else '#00FF00'
            axis[r,c].scatter(int(true_val[0][0]), int(true_val[0][1]),color=color)
    plt.show()

all_graphs()