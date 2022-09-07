import time
import sys

symbol_set = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
neighbors = {}

def print_puzzle(attrs, string):
    for i in range(0, len(string), attrs[0]):
        row = ""
        for j in range(i, i+attrs[0], attrs[2]):
            row += (' '.join(string[j:j+attr[2]]+' ')+' ')
        print(row)
        if((i/attrs[0])%attrs[1]==attrs[1]-1): print()
    return ''

def get_attrs(string):
    n = int(len(string)**(1/2))
    sq = int(n**(1/2))
    if(sq**2 != n):
        while(n%int(sq)!=0):
            sq -= 1
    height = sq
    width = n//height
    symbols = symbol_set[:n]
    sub_blocks = len(string)//(width*height)
    return (n, height, width, sub_blocks, symbols)

def get_neighbors(attrs, string):
    neighbors = {'row':{i:[] for i in range(attrs[0])}, 'col':{i:[] for i in range(attrs[0])}, 'sub-block':{i:[] for i in range(attrs[3])}}
    constraint = [i for i in range(len(string))]
    for i in range(len(string)):
        r = (i//attrs[0])
        c = (i%attrs[0])
        sb = attrs[1]*(r//attrs[1])+(c//attrs[2])
        neighbors['row'][r] += [i]
        neighbors['col'][c] += [i]
        neighbors['sub-block'][sb] += [i]
        constraint[i] = [r, c, sb]
    return neighbors, constraint

def get_instances(string):
    return {char : string.count(char) for char in string}

def goal_test(attrs, string):
    insts = get_instances(string)
    for key in insts.keys():
        if insts[key]!=1:
            return False
    return True

def goal_test_rig(neighbors, attrs, string):
    prelimCheck = {ch:string.count(ch) for ch in attrs[-1]}
    for key in prelimCheck:
        if prelimCheck[key]!=attrs[0]:
            return False
    for key in neighbors['row'].keys():
        r = [string[i] for i in neighbors['row'][key]]
        if(goal_test([len(r)], ''.join(r))==False):
            return False
    for key in neighbors['col'].keys():
        c = [string[i] for i in neighbors['col'][key]]
        if(goal_test([len(c)], ''.join(c))==False):
            return False
    for key in neighbors['sub-block'].keys():
        sb = [string[i] for i in neighbors['sub-block'][key]]
        if(goal_test([len(sb)], ''.join(sb))==False):
            return False
    return True

def get_next_unassigned_var(string):
    for i in range(len(string)):
        if string[i]=='.':
            return i
    return None

def get_sorted_values(neighbors, constraint, attrs, string, index):
    pos = attrs[-1]
    constraintVals = constraint[index]
    used = set()
    for i in neighbors['row'][constraintVals[0]]: used.add(string[i])
    for i in neighbors['col'][constraintVals[1]]: used.add(string[i])
    for i in neighbors['sub-block'][constraintVals[2]]: used.add(string[i])
    return [val for val in pos if val not in used]

def csp_backtracking(neighbors, constraint, attrs, string):
    if goal_test_rig(neighbors, attrs, string):
        return string
    var = get_next_unassigned_var(string)
    for val in get_sorted_values(neighbors, constraint, attrs, string, var):
        new_state = string[:var] + val + string[var+1:]
        result = csp_backtracking(neighbors, constraint, attrs, new_state)
        if result is not None:
            return result
    return None

with open("./"+sys.argv[1],"r") as f:
    line_list = [line.strip() for line in f]
    start = time.perf_counter()
    for i in range(len(line_list)):
        attr = get_attrs(line_list[i])
        neighbors, constraint = get_neighbors(attr, line_list[i])
        print(csp_backtracking(neighbors, constraint, attr, line_list[i]))
    print(time.perf_counter()-start)     