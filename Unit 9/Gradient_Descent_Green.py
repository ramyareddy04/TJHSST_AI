import sys
import numpy as np
import math

def partial(x, y):
    if sys.argv[1] == 'A':
        return np.array([[8*x-3*y+24, -3*x+4*y-20]])
    else:
        return np.array([[2*(x-y), -2*x+4*y-2]])

n = 1
x = np.array([[0,0]])
lr = 0.1
grad = partial(x[0][0], x[0][1])
print(n, x[0], grad[0])
while np.linalg.norm(grad[0]) > pow(10, -8):
    x = x - lr*grad
    grad = partial(x[0][0], x[0][1])
    n += 1
    print(n, x[0], grad[0])