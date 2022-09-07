import time
import sys

def goal_test(state):
    for i in range(len(state)):
        if state[i] < 0: return False
    return True

def quick_find(order, state):
    length = len(order)
    length2 = len(state)
    for i in order:
        for j in range(i, length2, length):
            if state[j] < 0: return j
    return None

def get_next_unassigned_var(state):
    l = len(state)
    if l==194: 
        odds = [i for i in range(6,l,2)] + [0,2,4]
        evens = [i for i in range(3,l,2)] + [1]
        for i in evens + odds:
            if state[i] < 0: return i
    if l==182: 
        odds = [i for i in range(6,l,2)] + [0,2,4]
        evens = [i for i in range(3,l,2)] + [1]
        for i in evens + odds:
            if state[i] < 0: return i
    if (l%6==3 and l>=21): 
        odds = [i for i in range(4,l,2)] + [0,2]
        evens = [i for i in range(5,l,2)] + [1,3]
        for i in evens + odds:
            if state[i] < 0: return i
    elif (l%12==2 and l>=50):
        odds = [2, 0] + [i for i in range(6,l,2)] + [4]
        evens = [i for i in range(5,l,2)] + [1,3]
        for i in evens + odds:
            if state[i] < 0: return i
    elif l%2==1: return quick_find([0,1], state)
    else: return quick_find([1,0], state)

def is_valid(state, row, idx):
    for i in range(len(state)):
        if(i!=row and state[i]>=0 and(state[i]==idx or abs(state[i]-idx)== abs(i-row))):
                return False
    return True

def get_sorted_values(state, row):
    curr = {state[i] for i in range(0,len(state))}
    return [idx for idx in range(len(state),0,-1) if(idx not in curr and is_valid(state, row, idx))]

def test_solution(state):
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(var, "middle", compare)
                return False
            if left >= 0 and state[compare] == left:
                print(var, "left", compare)
                return False
            if right < len(state) and state[compare] == right:
                print(var, "right", compare)
                return False
    return True

def csp_backtracking(state, solved):
    if solved == len(state) and goal_test(state): return state
    var = get_next_unassigned_var(state)
    for val in get_sorted_values(state, var):
        new_state = state[:var] + [val] + state[var+1:]
        result = csp_backtracking(new_state, solved+1)
        if result is not None: return result
    return None

statements = []
printTimes = []
time1 = time.perf_counter()
board_size = 8
while time.perf_counter() - time1 < 30:
    temp = csp_backtracking([-1 for j in range(board_size)], 0)
    statements.append(temp)
    board_size += 1
#for i, val in enumerate(statements):
#    print(i+8, test_solution(val))
print(len(statements)+8)