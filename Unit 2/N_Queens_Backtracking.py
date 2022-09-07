import time
import sys

def goal_test(state):
    for i in range(len(state)):
        if state[i] < 0:
            return False
    return True

def get_next_unassigned_var(state):
    if(len(state)%2==1):
        for i in range(0,len(state),2):
            if state[i] < 0:
                return i
        for i in range(1,len(state)+1,2):
            if state[i] < 0:
                return i
    else:
        for i in range(1,len(state)+1,2):
            if state[i] < 0:
                return i
        for i in range(0,len(state),2):
            if state[i] < 0:
                return i
    return None

def is_valid(state, row, idx):
    for i in range(len(state)):
        if(i!=row and state[i]>=0 and(state[i]==idx or abs(state[i]-idx)== abs(i-row))):
                return False
    return True

def get_sorted_values(state, row):
    curr = {state[i] for i in range(0,len(state))}
    return [idx for idx in range(len(state)) if(idx not in curr and is_valid(state, row, idx))]
    
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

def csp_backtracking(state):
    if goal_test(state):
        return state
    var = get_next_unassigned_var(state)
    for val in get_sorted_values(state, var):
        new_state = state[:var] + [val] + state[var+1:]
        result = csp_backtracking(new_state)
        if result is not None:
            return result
    return None

board_size = 80
board_1 = [-1 for i in range(board_size)]
time1 = time.perf_counter()
temp = csp_backtracking(board_1)
print(temp)
print(test_solution(temp))
board_size = 200
board_2 = [-1 for i in range(board_size)]
temp = csp_backtracking(board_2)
print(temp)
print(test_solution(temp))
time2 = time.perf_counter()    
print(time2-time1)