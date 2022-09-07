import sys
import math
import numpy as np
import random

def rv():
    return 2*np.random.rand() - 1

def step(num):
    return 1 if num >= 0.5 else 0

def sigmoid(num):
    return pow(1+pow(math.e,-num),-1)

def p_net(A, x, w_list, b_list):
    new_A = np.vectorize(A)
    a0 = x
    for layer in range(len(w_list)):
        a0 = new_A(a0@w_list[layer] + b_list[layer])
    return a0

def error(out, correct):
    return 0.5*pow(np.linalg.norm(correct-out),2)

def backpropogate(A, train, w_list, b_list, lr, epochs):
    new_A = np.vectorize(A)
    new_Step = np.vectorize(step)
    for epoch in range(epochs):
        for x, y in train:
            a = [x]
            for layer in range(len(w_list)):
                a.append(new_A(a[-1]@w_list[layer] + b_list[layer]))
            delta = [(a[-1]*(1-a[-1]))*(y-a[-1])]
            if len(sys.argv) > 1 and sys.argv[1] == 'S':
                t_lr = lr
            elif len(sys.argv) > 1 and sys.argv[1] == 'C':
                t_lr = error(a[-1], y)*lr
            for layer in range(len(w_list)-2, -1, -1):
                delta = [(a[layer+1]*(1-a[layer+1]))*(delta[0]@w_list[layer+1].T)] + delta
            for layer in range(len(w_list)):
                b_list[layer] = b_list[layer] + t_lr*delta[layer]
                w_list[layer] = w_list[layer] + t_lr*(a[layer].T@delta[layer])
            out = p_net(sigmoid, x, w_list, b_list)
            if len(sys.argv) > 1 and sys.argv[1] == 'S': print(out)
            err = error(out, y)
        if len(sys.argv) > 1 and sys.argv[1] == 'C':
            accuracy = 0
            for x, y in train:
                out = new_Step(p_net(sigmoid, x, w_list, b_list))
                if (out == y).all(): accuracy += 1
            print("Misclassified # of Points for Epoch",epoch+1, ": ", len(train)-accuracy)
    # accuracy = 0
    # for x, y in train:
    #     out = new_Step(p_net(sigmoid, x, w_list, b_list))
    #     if (out == y).all(): accuracy += 1
    # print("Accuracy:", 100*accuracy/len(train))
    return err

if sys.argv[1] == 'S':
    w_list = [
            np.array([[rv(),rv()],[rv(),rv()]]),
            np.array([[rv(),rv()],[rv(),rv()]])
            ]
    b_list = [
            np.array([[rv(),rv()]]),
            np.array([[rv(),rv()]])
            ]
    run = backpropogate(sigmoid, [[np.array([[0,0]]), np.array([[0,0]])], [np.array([[0,1]]), np.array([[0,1]])], [np.array([[1,0]]), np.array([[0,1]])], [np.array([[1,1]]), np.array([[1,0]])]], w_list, b_list, 0.7, 500)
elif sys.argv[1] == 'C':
    w_list = [
            np.array([[1,1,-1,-1],[1,-1,1,-1]]),
            np.array([[1],[1],[1],[1]]) 
        ]
    b_list = [
            np.array([[2.090,2.090,2.090,2.090]]),
            np.array([[-3.410]])
    ]
    train = []
    with open('10000_pairs.txt') as file:
        for line in file:
            l = [float(i) for i in line.split()]
            x = np.array([[l[0], l[1]]])
            y = 1 if pow(l[0],2)+pow(l[1],2) < 1 else 0
            train.append([x, np.array([[y]])])
    run = backpropogate(sigmoid, train, w_list, b_list, 0.2, 20)