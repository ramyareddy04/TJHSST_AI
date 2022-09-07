from collections import deque
import time
import sys

def get_children(dict):
    children = {}
    letters = 'abcdefghijklmnopqrstuvwxyz'
    
    for word in dict:
        children[word] = [word[:idx] + letter + word[idx+1:] for letter in letters for idx in range(len(word)) if word[idx]!=letter and word[:idx] + letter + word[idx+1:] in dict]
    return children

def goal_test(string1, string2):
    return string1 == string2

def BFS(string, goal, children, dict):
    fringe = deque([[string, [string]]])
    visited = set([string])
    length = len(string)
    
    while len(fringe)!=0:
        v = fringe.popleft()
        if goal_test(''.join(v[0]), goal):
            return v[1]
        for c in children[v[0]]:
            if c not in visited:
                visited.add(c)
                fringe.append([c, v[1] + [c]])
    return None

def brainteaser_1(children, dict):
    count = 0
    for word in dict:
        if len(children[word])==0:
            count+=1
    return count

def brainteaser_2(children, dict):
    clump = 0
    for string in dict:
        fringe = deque([[string, [string]]])
        visited = set([string])

        while len(fringe)!=0:
            v = fringe.popleft()
            for c in children[v[0]]:
                if c not in visited:
                    visited.add(c)
                    fringe.append([c, v[1] + [c]])
        clump = max(clump, len(visited))
    return clump
    
def brainteaser_3(children, d):
    count = 0
    dict = [key for key in d]
    while len(dict)!=0:
        for string in dict:
            fringe = deque([[string, 0]])
            list = [[string, 0]]
            visited = set([string])

            while len(fringe)!=0:
                v = fringe.popleft()
                dict.remove(v[0])
                for c in children[v[0]]:
                    if c not in visited:
                        visited.add(c)
                        list.append([c, v[1] + 1])
                        fringe.append([c, v[1] + 1])
            if len(visited)!=1:
                count += 1
    return count

def brainteaser_4(children, dict):
    path = []
    for string in dict:
        string = string
        fringe = deque([[string, [string]]])
        list = [[string, [string]]]
        visited = set([string])

        while len(fringe)!=0:
            v = fringe.popleft()
            for c in children[v[0]]:
                if c not in visited:
                    visited.add(c)
                    list.append([c, v[1] + [c]])
                    fringe.append([c, v[1] + [c]])
        if len(path) < len(list[-1][1]):
            path = list[-1][1]
    return path[0], path[-1], path

start = time.perf_counter()
with open("./"+sys.argv[1],"r") as f:
    dict = [line[:-1] for line in f]
end = time.perf_counter()
print("Time to create the data structure was: %s seconds\n" % (end-start))
start = time.perf_counter()

children = get_children(dict)
with open("./"+sys.argv[2],"r") as f:

    idx = 0
    for line in f:
        temp = line.split()
        print("Line: ", idx)
        method1 = BFS(temp[1], temp[0], children, dict)
        if method1 == None:
            print("No solution!")
        else:
            print("Length is: ",len(method1))
            for move in method1:
                print(move)
        idx += 1
        print()
        end = time.perf_counter()

print("Time to solve all of these puzzles was: %s seconds" % (end-start))