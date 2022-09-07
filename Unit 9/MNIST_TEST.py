from platform import architecture
import sys
import math
import numpy as np
import random
import pickle

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

def determine_accuracy(train, w_list, b_list):
    accuracy = 0
    for x, y in train:
        out = p_net(sigmoid, x, w_list, b_list)
        step(out)
        if (out == y).all(): accuracy += 1
    print("Accuracy:", 100*accuracy/len(train))
    return accuracy

choice = input("Weights filename? ")
with open(choice, 'rb') as file:
    myVar = pickle.load(file)
    w_list = myVar[0]
    b_list = myVar[1]
test = []
test_file = input("Which csv? ")
with open(test_file) as f:
    lines = f.readlines()
    for line in lines:
        x = [float(i)/255 for i in line.split(',')[1:]]
        y = [0 if i!=int(line[0]) else 1 for i in range(10)]
        test.append([np.array([x]), np.array(y)])
run = determine_accuracy(test, w_list, b_list)