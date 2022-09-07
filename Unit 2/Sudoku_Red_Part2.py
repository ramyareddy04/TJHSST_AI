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
    constraint = {i:[] for i in range(len(string))}
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
    return True


def get_most_constrained_var(d, string):
    vals = [len(d[key]) for key in d.keys() if len(d[key])!=1]
    if len(vals)==0: return None
    minVals = min(vals)
    for key in d.keys():
        if len(d[key]) ==minVals:
            return key
    return None

def get_sorted_values(neighbors, constraint, attrs, string, index):
    if string[index]!='.': return []
    pos = attrs[-1]
    constraintVals = constraint[index]
    used = set()
    for i in neighbors['row'][constraintVals[0]]: used.add(string[i])
    for i in neighbors['col'][constraintVals[1]]: used.add(string[i])
    for i in neighbors['sub-block'][constraintVals[2]]: used.add(string[i])
    return [val for val in pos if val not in used]

def get_all_pos(neighbors, constraint, attrs, string):
    return {i:get_sorted_values(neighbors, constraint, attrs, string, i) for i in range(len(string)) if string[i]=='.'}
        
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

def getIdx(d, grp, ch):
    idx = -1
    for val in grp:
        if val in d.keys():
            if ch in d[val]:
                if len(d[val])==1: idx = val
                else:
                    if idx==-1: idx = val
                    else: idx = -2
    return idx

def assign(d, neighbors, constraint, string, idx, ch):
    set = constraint[idx]
    otherIdxes = neighbors['row'][set[0]] + neighbors['col'][set[1]] + neighbors['sub-block'][set[2]]
    issues = [i for i in otherIdxes if i in d.keys()]
    for i in issues:
        if ch in d[i]: 
            if(len(d[i])==1): return False, None
            d[i].remove(ch)

def constraint_propogation_all(d, neighbors, constraint, attrs, string):
    s = string
    if goal_test_rig(neighbors, attrs, s): return True, s
    for pos in [neighbors['sub-block'],neighbors['row'],neighbors['col']]:
        for i in pos.keys():
            grp = [s[j] for j in pos[i]]
            for ch in attrs[-1]:
                if ch not in grp:
                    idx = getIdx(d, pos[i], ch)
                    if idx!=-1 and idx!=-2: 
                        s = s[:idx] + ch + s[idx+1:]
                        d.pop(idx)
                        assign(d, neighbors, constraint, s, idx, ch)
                    elif idx == -2: continue
                    else: return False, None
    if s==string: return False, s
    return forward_looking(d, neighbors, constraint, attrs, s)
 
def forward_looking(d, neighbors, constraint, attrs, string):
    s = string
    if goal_test_rig(neighbors, attrs, s): return True, s
    for i in d.keys():
        if len(d[i])==1:
            s = s[:i] + d[i][0] + s[i+1:]
            grps = constraint[i]
            vals = [j for j in neighbors['row'][grps[0]] if j != i and j in d.keys()] + [j for j in neighbors['col'][grps[1]] if j != i and j in d.keys()] + [j for j in neighbors['sub-block'][grps[2]] if j != i and j in d.keys()]
            for j in vals:
                if d[i][0] in d[j]:
                    if(len(d[j])==1): return False, None
                    d[j].remove(d[i][0])
    if s==string: return False, string
    return forward_looking(d, neighbors, constraint, attrs, s)

def backtracking_opt(d, neighbors, constraint, attrs, string):
    if goal_test_rig(neighbors, attrs, string): return string
    var = get_most_constrained_var(d, string) 
    for val in d[var]:
        new_state = string[:var] + val + string[var+1:]
        newD = get_all_pos(neighbors, constraint, attrs, new_state)
        _, checked_board = forward_looking(newD, neighbors, constraint, attrs, new_state)
        if checked_board is not None: 
            _, checked_board2 = constraint_propogation_all(newD, neighbors, constraint, attrs, checked_board)
            if checked_board2 is not None:
                result = backtracking_opt(newD, neighbors, constraint, attrs, checked_board2)
                if result is not None: return result
    return None

with open("./"+sys.argv[1],"r") as f:
    lines = []
    line_list = [line.strip() for line in f]
    for i in range(len(line_list)):
        attr = get_attrs(line_list[i])
        neighbors, constraint = get_neighbors(attr, line_list[i])
        pos = get_all_pos(neighbors, constraint, attr, line_list[i])
        isSolved, p = forward_looking(pos, neighbors, constraint, attr, line_list[i])
        if isSolved==True: lines.append(p)
        else: lines.append(backtracking_opt(get_all_pos(neighbors, constraint, attr, p), neighbors, constraint, attr, p))
    for i, line in enumerate(lines): print(line)