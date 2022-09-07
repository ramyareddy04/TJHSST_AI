import sys
import random
import numpy as np
import math

def partial(x, y):
    if sys.argv[1] == 'A':
        return np.array([[8*x-3*y+24, -3*x+4*y-20]])
    else:
        return np.array([[2*(x-y), -2*x+4*y-2]])

def one_d_minimize(f, left, right, tolerance):
    l = left
    r = right
    #print(left,right)
    if r-l < tolerance: return (l+r)/2
    dX = r-l
    v1 = f(l+dX/3)
    v2 = f(r-dX/3)
    if v1 >= v2: l += dX/3
    elif v2 >= v1: r -= dX/3
    return one_d_minimize(f, l, r, tolerance)

def make_funct(a, b):
    def f(x):
        i = a - b*x 
        #print(i)
        j = i[0][0]
        k = i[0][1]
        if sys.argv[1] == 'A':
            return 4*pow(j,2) - 3*j*k + 2*pow(k,2) + 24*j -20*k
        else:
            return pow(1-j,2) + pow(j-pow(k,2),2)
    return f

x = np.array([[0,0]])
grad = partial(x[0][0], x[0][1])
print(x[0], grad[0])
while np.linalg.norm(grad[0]) > pow(10, -8):
    f = make_funct(x, grad)
    x = x - one_d_minimize(f,0,1,pow(10,-3))*grad
    grad = partial(x[0][0], x[0][1])
    print(x[0], grad[0])