from collections import deque
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

def opp_BFS(string, printPath):
    goal = find_goal(string)
    fringe = deque([[goal, [goal]]])
    visited = set([goal])
    length = int(len(string)**(1/2))

    while len(fringe)!=0:
        v = fringe.popleft()
        if ''.join(v[0])==string:
            if printPath:
                show_moves(length, v[1])
            return len(v[1])-1
        for c in get_children(length, v[0]):
            if c not in visited:
                visited.add(c)
                fringe.append([c, v[1] + [c]])
    return None

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

with open("./"+sys.argv[1],"r") as f:
    line_list = [line.strip() for line in f]
    
    for i in range(len(line_list)):
        start = time.perf_counter()
        temp = line_list[i].split()
        bfs_result = BFS(temp[1], False)
        end = time.perf_counter()
        print("Line ", i ,": ", temp[1],", ", bfs_result," moves found in ", (end - start), " seconds")

        start = time.perf_counter()
        temp = line_list[i].split()
        bibfs_result = BiBFS(temp[1], False)
        end = time.perf_counter()
        print("Line ", i ,": ", temp[1],", ", bibfs_result," moves found in ", (end - start), " seconds")