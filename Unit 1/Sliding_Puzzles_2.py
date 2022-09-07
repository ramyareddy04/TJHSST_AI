from collections import deque
from heapq import heappush, heappop, heapify
import time
import sys

def print_puzzle(size, string):
    for i in range(0, len(string), size):
        print(' '.join(string[i:i+size])+' ')
    return ''

def find_goal(string):
    return ''.join(sorted(string))[1:]+'.'

def get_children(size, string):
    directions = [-1, 1, size, -size]
    list = []

    idx = string.index('.')
    for move in directions:
        change = int((idx + move)/size)-int(idx/size)
        if((idx + move >= 0) and (idx + move < len(string)) and (abs(change)<=abs(int(move/size)))):
            curr = string[:idx+move] + string[idx] + string[idx+move+1:]
            curr = curr[:idx] + string[idx+move] + curr[idx+1:]
            list.append(curr)
    return list

def goal_test(string):
    return string == find_goal(string)

def show_moves(length, path):
    print([move for move in path])

def BFS(string, printPath):
    fringe = deque([[string, [string]]])
    visited = set([string])
    length = int(len(string)**(1/2))
    
    while len(fringe)!=0:
        v = fringe.popleft()
        if goal_test(''.join(v[0])):
            if printPath:
                show_moves(length, v[1])
            return len(v[1])-1
        for c in get_children(length, v[0]):
            if c not in visited:
                visited.add(c)
                fringe.append([c, v[1] + [c]])
    return None

def DFS(string, printPath):
    fringe = deque([[string, [string]]])
    visited = set([string])
    length = int(len(string)**(1/2))
    
    while len(fringe)!=0:
        v = fringe.pop()
        if goal_test(''.join(v[0])):
            if printPath:
                show_moves(length, v[1])
            return len(v[1])-1
        for c in get_children(length, v[0]):
            if c not in visited:
                visited.add(c)
                fringe.append([c, v[1] + [c]])
    return None

def k_DFS(string, k, goal, length):
    fringe = []
    start_node = (string, 0, {string})
    fringe.append(start_node)
    while len(fringe)!=0:
        v = fringe.pop()
        if v[0]==goal:
            return v
        if v[1] < k:
            for c in get_children(length, v[0]):
                if c not in v[2]:
                    tempSet = v[2].copy()
                    tempSet.add(c)
                    temp = (c, v[1]+1, tempSet)
                    fringe.append(temp)
    return None

def ID_DFS(string):
    max_depth = 0
    result = None
    goal = find_goal(string)
    length = int(len(string)**(1/2))
    while result is None:
        result = k_DFS(string, max_depth, goal, length)
        max_depth += 1
    return result[1]

def BiBFS(string, printPath):
    fringe = deque([[string, 0]])
    dict = {string : 0}
    visited = set([string])
    
    goal = find_goal(string)
    other_fringe = deque([[goal, 0]])
    other_dict = {goal : 0}
    other_visited = set([goal])
    length = int(len(string)**(1/2))

    while len(fringe)!=0 and len(other_fringe)!=0:
        v = fringe.popleft()
        if goal_test(''.join(v[0])):
            return v[1]
        elif v[0] in other_dict:
            return v[1]+other_dict[v[0]]
        for c in get_children(length, v[0]):
            if c not in visited:
                visited.add(c)
                fringe.append([c, v[1] + 1])
                dict[c] = v[1] + 1

        v = other_fringe.popleft()
        if ''.join(v[0])==string:
            return v[1]
        elif v[0] in dict:
            return v[1]+dict[v[0]]
        for c in get_children(length, v[0]):
            if c not in other_visited:
                other_visited.add(c)
                other_fringe.append([c, v[1] + 1])
                other_dict[c] = v[1] + 1
    return None

def parity_check(string):
    wrong = 0
    length = int(len(string)**(1/2))
    idx = string.index('.')
    row = int(idx/length)
    modStr = string[:idx] + string[idx+1:]
    alph = "".join(sorted(modStr))
    for i in range(len(alph)):
        idx = modStr.index(alph[i])
        for j in range(0, idx+1):
            if modStr[j] > alph[i]: 
                wrong += 1
    if length%2==0:
        if row%2==0:
            return wrong%2==1
        else:
            return wrong%2==0
    else:
        return wrong%2==0

def taxicab(string):
    wrong = 0
    length = int(len(string)**(1/2))
    alph = "".join(sorted(string))[1:]
    for i in range(len(alph)):
        row = i//length
        col = i%length
        idx = string.index(alph[i])
        currRow = idx//length
        currCol = idx%length
        wrong += abs(currRow-row) + abs(currCol-col)
    return wrong

def a_star(string):
    closed = set()
    fringe = []
    start_node = (taxicab(string), string, 0)
    heappush(fringe, start_node)

    goal = find_goal(string)
    length = int(len(string)**(1/2))

    while len(fringe)!=0:
        v = heappop(fringe)
        if v[1]==goal:
            return v[2]
        if v[1] not in closed:
            closed.add(v[1])
            for c in get_children(length, v[1]):
                if c not in closed:
                    temp = (v[2]+1+taxicab(c), c, v[2]+1)
                    heappush(fringe, temp)
    return None

with open("./"+sys.argv[1],"r") as f:
    line_list = [line.strip() for line in f]

    for i in range(len(line_list)): 
        start = time.perf_counter()
        temp = line_list[i].split()
        if parity_check(temp[1])==False:
            end = time.perf_counter()
            print("Line ", i, ": ", temp[1], ", no solution determined in", (end-start), "seconds")
        else:
            if(temp[2]=='B' or temp[2]=='!'):
                start = time.perf_counter()
                bfs = BFS(temp[1], False)
                end = time.perf_counter()
                print("Line ", i, ": ", temp[1], ", BFS - ", bfs, " moves found in ", (end - start), " seconds")
            if(temp[2]=='I' or temp[2]=='!'):
                start = time.perf_counter()
                dfs = ID_DFS(temp[1])
                end = time.perf_counter()
                print("Line ", i, ": ", temp[1], ", DFS - " , dfs, " moves found in ", (end - start), " seconds")
            if(temp[2]=='A' or temp[2]=='!'):
                start = time.perf_counter()
                a_s = a_star(temp[1])
                end = time.perf_counter()
                print("Line ", i, ": ", temp[1], ", A* - " , a_s, " moves found in ", (end - start), " seconds")