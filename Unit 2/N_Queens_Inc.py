import time
import sys
from heapq import heappush, heappop, heapify
from random import randint

def generate_state(length):
    state = []
    for i in range(length):
        state.append(randint(0,length-1))
    return state

def get_conflicts(state, row, idx):
    count = 0
    for i in range(len(state)):
        if(i!=row and (state[i]==idx or abs(state[i]-idx)==abs(i-row))):
                count += 1
    return count

def get_all_conflicts(state):
    return [get_conflicts(state, idx, state[idx]) for idx in range(len(state))]

def goal_test(state):
    conflicts = get_all_conflicts(state)
    if sum(conflicts)==0:
        return False
    else:
        return conflicts

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

def get_idxes(conflicts):
    ways = []
    for i in range(len(conflicts)):
        heappush(ways, (conflicts[i], i))

    val = max(conflicts)
    while(ways[0][0] != val):
        heappop(ways)
    return ways

def get_sorted_values(state, row):
    ways = []
    for idx in range(len(state)):
        temp = state[:row]+[idx]+state[row+1:]
        conflict = get_all_conflicts(temp)
        heappush(ways, (sum(conflict), temp, conflict))
    finWays = []
    minMoves = ways[0][0]
    moveOn = True
    while(moveOn == True):
        temp = heappop(ways)
        if(temp[0] == minMoves):
            heappush(finWays, temp)
        else:
            moveOn = False
    return finWays
    
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

def incremental(state, path):
    conflicts = goal_test(state)
    if conflicts==False:
        return state, path + str(state) + ", Conflicts: 0"
    path += str(state) + ", Conflicts: " + str(sum(conflicts)) + "\n"
    idxes = get_idxes(conflicts)
    rand = randint(0, len(idxes)-1)
    ways = get_sorted_values(state,idxes[rand][1])
    rand = randint(0,len(ways)-1)
    result = incremental(ways[rand][1], path)
    if result is not None:
        return result
    return None

board_size = 32
board_1 = generate_state(board_size)
time1 = time.perf_counter()
result = incremental(board_1, "")
print(result[1])
print(test_solution(result[0]))
board_size = 70
board_2 = generate_state(board_size)
result = incremental(board_2, "")
print(result[1])
print(test_solution(result[0]))
time2 = time.perf_counter()    
print(time2-time1)