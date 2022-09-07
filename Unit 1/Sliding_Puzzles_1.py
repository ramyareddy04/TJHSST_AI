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

def solve_question_6():
    string = '12345678.'
    fringe = deque([[string, 0]])
    list = [[string, 0]]
    visited = set([string])

    while len(fringe)!=0:
        v = fringe.popleft()
        for c in get_children(3, v[0]):
            if c not in visited:
                visited.add(c)
                list.append([c, v[1] + 1])
                fringe.append([c, v[1] + 1])

    max = list[-1][1]
    max_steps = []
    for i in range(len(list)-1, 0, -1):
        if(list[i][1] == max):
            max_steps.append(list[i][0])
    return max_steps

with open("./"+sys.argv[1],"r") as f:
    line_list = [line.strip() for line in f]
    
    for i in range(len(line_list)):
        start = time.perf_counter()
        temp = line_list[i].split()
        bfs_result = BFS(temp[1], False)
        end = time.perf_counter()
        print("Line ", i ,": ", temp[1],", ", bfs_result," moves found in ", (end - start), " seconds")