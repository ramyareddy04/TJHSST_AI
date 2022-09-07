from platform import architecture
import sys
import math
import numpy as np
import random
import pickle

w_list = []
b_list = []

def rv():
    return 2*np.random.rand() - 1

def create_architecture(layers):
    for i in range(len(layers)-1):
        w_list.append(np.array([[rv() for k in range(layers[i+1])] for j in range(layers[i])]))
        b_list.append(np.array([[rv() for j in range(layers[i+1])]]))

def save_weights(weights_file):
    with open(weights_file, 'wb') as f:
        var = [w_list, b_list]
        pickle.dump(var, f)
        f.close()

def step(nums):
    row = nums[0, :]
    val = np.max(row)
    for i in range(len(row)):
        row[i] = 0 if row[i] != val else 1

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
    weights_file = input("What file do you want to save the weights and biases to? ")
    for epoch in range(epochs):
        for x, y in train:
            a = [x]
            for layer in range(len(w_list)):
                a.append(new_A(a[-1]@w_list[layer] + b_list[layer]))
            delta = [(a[-1]*(1-a[-1]))*(y-a[-1])]
            t_lr = math.sqrt(error(a[-1], y))*lr # variable lr
            for layer in range(len(w_list)-2, -1, -1):
                delta = [(a[layer+1]*(1-a[layer+1]))*(delta[0]@w_list[layer+1].T)] + delta
            for layer in range(len(w_list)):
                b_list[layer] = b_list[layer] + t_lr*delta[layer]
                w_list[layer] = w_list[layer] + t_lr*(a[layer].T@delta[layer])
            out = p_net(sigmoid, x, w_list, b_list)
            err = error(out, y)
        accuracy = 0
        for x, y in train:
            out = p_net(sigmoid, x, w_list, b_list)
            step(out)
            if (out == y).all(): accuracy += 1
        print("Misclassified # of Data Points for Epoch",epoch+1, ": ", len(train)-accuracy)
        save_weights(weights_file)
    return err

choice = input("(N)ew process, or (L)oad saved process? ")
if choice.lower() == 'l':
    filename = input("Filename? ")
    with open(filename, 'rb') as f:
        myVar = pickle.load(f)
        w_list = myVar[0]
        b_list = myVar[1]
else:
    architecture = [784, 300, 100, 10]
    create_architecture(architecture)
train = []
with open('mnist_train.csv') as f:
    lines = f.readlines()
    for line in lines:
        x = [float(i)/255 for i in line.split(',')[1:]]
        y = [0 if i!=int(line[0]) else 1 for i in range(10)]
        train.append([np.array([x]), np.array(y)])
run = backpropogate(sigmoid, train, w_list, b_list, 0.6, 10)