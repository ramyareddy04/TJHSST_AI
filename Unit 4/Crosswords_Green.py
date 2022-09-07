import sys; args = sys.argv[1:]
import random
#myLines = open(args[0], 'r').read().splitlines()

seeded = []
pastStates = []
dims, sqrs = args[:2]
dims = dims.split('x')
dims = [int(dims[i]) for i in range(len(dims))] 
sqrs = int(sqrs)
strs = args[2:]

crossword = ''.join(['*' for i in range(dims[0]*dims[1])]) if sqrs!=dims[0]*dims[1] else ''.join(['#' for i in range(dims[0]*dims[1])])

def toGrid(dims, board):
    for i in range(0, len(board), int(dims[1])): print(' '.join(board[i:i+int(dims[1])]))

def putSeededStrings(dims, board, seededstrs, addChars):
    for s in seededstrs:
        row = int(s[1:s.index('x')])*int(dims[1])
        temp2 = s.index('x')+1
        if len(s)-1 > temp2:
            while len(s) > temp2 and s[temp2] in '0123456789': temp2+=1
            if temp2 == len(s): break
            col = int(s[s.index('x')+1:temp2])
            word = s[temp2:].upper()
            if len(word)==0: board[row + col] = '#'
            else:
                for idx, ch in enumerate(word):
                    temp = ch if (addChars or ch=='#') else '-'
                    board = board[:row + col] + temp + board[row + col+1:]
                    if s[0] in ['H', 'h']: col += 1
                    else: row += int(dims[1])
    return board

def spiral_fill(dims, blocked, board):
    dr = [-1, 0, 1, 0] #[0, 1, 0, -1]
    dc = [0, 1, 0, -1] #[1, 0, -1, 0]
    di = 0

    row = 0
    col = 0
    idx = 0
    visited = [False for i in range(len(board))]
    while board.count('#')!=blocked:
        visited[idx] = True
        if board[idx] == '*': board = board[:idx] + '#' + board[idx+1:]
        if not (row + dr[di]>=0 and row + dr[di] < dims[0] and col + dc[di] >= 0 and col + dc[di] < dims[1] and visited[(row+dr[di])*dims[1]+col+dc[di]] == False): di = (di+1)%4
        row += dr[di]
        col += dc[di]
        idx = row*dims[1]+col
    return board

def get_split(board):
    filled = []
    remaining = []
    for i in range(len(board)): 
        if i not in seeded:
            if board[i] != '#': remaining += [i]
            else: filled += [i]
    return filled, remaining

def area_fill(idx, dims, temp, board):
    if idx < 0 or idx > len(board): return 
    if board[idx] != '#' and temp[idx]==False: temp[idx] = True 
    else: return
    row = idx//dims[1]
    col = idx%dims[1]
    if row > 0: area_fill((row-1)*dims[1]+col, dims, temp, board)
    if row < dims[0]-1: area_fill((row+1)*dims[1]+col, dims, temp, board)
    if col > 0: area_fill(row*dims[1]+col-1, dims, temp, board)
    if col < dims[1]-1: area_fill(row*dims[1]+col+1, dims, temp, board)
    return

def produce_conflicts(dims, val, board, returnCount):
    problems = []
    count = 0
    row = val//dims[1]
    col = val%dims[1]
    if board[(dims[0]-row-1)*dims[1]+dims[1]-col-1] != '#': 
        count += 2
        problems.append((dims[0]-row-1)*dims[1]+dims[1]-col-1)
    if col == 1:
        if board[val-1] != '#':
            count += 1
            problems.append(val-1)
    if col == 2:
        if board[val-1] != '#' and board[val-2] != '#': 
            count += 1
            if board[val-1]!='#': problems.append(val-1)
            if board[val-2]!='#': problems.append(val-2)
    if col > 2: 
        if board[val-1] != '#' and board[val-2] =='#': 
            count += 1
            problems.append(val-1)
    if col > 3: 
        if board[val-1] != '#' and board[val-2] !='#' and board[val-3] =='#': 
            count += 1
            if board[val-1]!='#': problems.append(val-1)
            if board[val-2]!='#': problems.append(val-2)
    if col < dims[1]-2: 
        if board[val+1] != '#' and board[val+2] =='#': 
            count += 1
            problems.append(val+1)
    if col < dims[1]-3: 
        if board[val+1] != '#' and board[val+2] !='#' and board[val+3] =='#': 
            count += 1
            if board[val+1]!='#': problems.append(val+1)
            if board[val+2]!='#': problems.append(val+2)
    if col == dims[1]-2:
        if board[val+1] != '#':
            count += 1
            problems.append(val+1)
    if col == dims[1]-3:
        if board[val+1] != '#' and board[val+2] != '#': 
            count += 1
            if board[val+1]!='#': problems.append(val+1)
            if board[val+2]!='#': problems.append(val+2)
    if row == 1:
        if board[val-dims[1]] != '#': 
            count += 1
            problems.append(val-dims[1])
    if row == 2:
        if board[val-dims[1]] != '#' and board[val-2*dims[1]] != '#':
            count += 1
            if board[val-dims[1]]!='#': problems.append(val-dims[1])
            if board[val-2*dims[1]]!='#': problems.append(val-2*dims[1])
    if row > 2: 
        if board[val-dims[1]] != '#' and board[val-2*dims[1]] =='#': 
            count += 1
            problems.append(val-dims[1])
    if row > 3: 
        if board[val-dims[1]] != '#' and board[val-2*dims[1]] !='#' and board[val-3*dims[1]] =='#': 
            count += 1
            if board[val-dims[1]]!='#': problems.append(val-dims[1])
            if board[val-2*dims[1]]!='#': problems.append(val-2*dims[1])
    if row < dims[0]-2: 
        if board[val+dims[1]] != '#' and board[val+2*dims[1]] =='#': 
            count += 1
            problems.append(val+dims[1])
    if row < dims[0]-3: 
        if board[val+dims[1]] != '#' and board[val+2*dims[1]] !='#' and board[val+3*dims[1]] =='#': 
            count += 1
            if board[val+dims[1]]!='#': problems.append(val+dims[1])
            if board[val+2*dims[1]]!='#': problems.append(val+2*dims[1])
    if row == dims[0]-2:
        if board[val+dims[1]] != '#': 
            count += 1
            problems.append(val+dims[1])
    if row == dims[0]-3:
        if board[val+dims[1]] != '#' and board[val+2*dims[1]] != '#': 
            count += 1
            if board[val+dims[1]]!='#': problems.append(val+dims[1])
            if board[val+2*dims[1]]!='#': problems.append(val+2*dims[1])
    return count if returnCount else problems

def produce_fixes(dims, val, numConflicts, arr, board):
    solutions = []
    tempBoard = board[:val] + '*' + board[val+1:]
    for idx in arr:
        temp = produce_conflicts(dims, idx, tempBoard[:idx]+'#'+tempBoard[idx+1:], True)
        if temp < numConflicts and tempBoard[:idx]+'#'+tempBoard[idx+1:] not in pastStates: solutions += [idx]
    return solutions

def goal_test(dims, filled, remaining, blocked, board):
    temp = [False for i in range(len(board))]
    area = area_fill(filled[0], dims, temp, board)
    conflicts = []
    for val in remaining:
        temp2 = produce_conflicts(dims, val, board, True)
        if temp2!=0: conflicts += [val for i in range(temp2)]
    return False if temp.count(False) == blocked and len(conflicts)==0 else conflicts

def switch_vals(orig, other, board):
    board2 = board[:orig] + '*' + board[orig+1:]
    board2 = board2[:other] + '#' + board2[other+1:]
    return board2

def construct(dims, blocked, board):
    taken, spaces = get_split(board)
    conflicts = goal_test(dims, spaces, taken, blocked, board)
    if conflicts==False: return board
    org = conflicts[random.randint(0, len(conflicts)-1)]
    switch = produce_fixes(dims, org, conflicts.count(org), spaces, board)
    count = 0
    while len(switch)==0 and count<len(conflicts):
        org = conflicts[random.randint(0, len(conflicts)-1)]
        switch = produce_fixes(dims, org, conflicts.count(org), spaces, board)
        count += 1
    if count == len(conflicts): switch = spaces
    switch = switch[random.randint(0,len(switch)-1)] 
    pastStates.append(switch_vals(org, switch, board))
    result = construct(dims, blocked, pastStates[-1])
    if result is not None: return result
    return None

if sqrs != len(crossword):
    # preliminary spaces
    crossword = putSeededStrings(dims, crossword, strs, True)
    seeded = [i for i in range(len(crossword)) if crossword[i]!='*']
    seededX = [i for i in seeded if crossword[i]=='#']
    for val in seededX:
        row = val//dims[1]
        col = val%dims[1]
        if row <= 2:
            for i in range(row-1, -1, -1):
                temp = i*dims[1]+col
                crossword = crossword[:temp] + '#' + crossword[temp+1:]
                if col <= 2:
                    for j in range(col, -1, -1):
                        temp = i*dims[1]+j
                        crossword = crossword[:temp] + '#' + crossword[temp+1:]
                if col >= dims[1]-3:
                    for j in range(col, dims[1]):
                        temp = i*dims[1]+j
                        crossword = crossword[:temp] + '#' + crossword[temp+1:]
        if row >= dims[0]-3:
            for i in range(row+1, dims[0]):
                temp = i*dims[1]+col
                crossword = crossword[:temp] + '#' + crossword[temp+1:]
                if col <= 2:
                    for j in range(col-1, -1, -1):
                        temp = i*dims[1]+j
                        crossword = crossword[:temp] + '#' + crossword[temp+1:]
                if col >= dims[1]-3:
                    for j in range(col+1, dims[1]):
                        temp = i*dims[1]+j
                        crossword = crossword[:temp] + '#' + crossword[temp+1:]
        if col <= 2:
            for i in range(col-1, -1, -1):
                temp = row*dims[1]+i
                crossword = crossword[:temp] + '#' + crossword[temp+1:]
                if row <= 2:
                    for j in range(row, -1, -1):
                        temp = i*dims[1]+j
                        crossword = crossword[:temp] + '#' + crossword[temp+1:]
                if row >= dims[0]-3:
                    for j in range(row, dims[1]):
                        temp = i*dims[1]+j
                        crossword = crossword[:temp] + '#' + crossword[temp+1:]
        if col >= dims[1]-3:
            for i in range(col+1, dims[1]):
                temp = row*dims[1]+i
                crossword = crossword[:temp] + '#' + crossword[temp+1:]
                if row <= 2:
                    for j in range(row-1, -1, -1):
                        temp = i*dims[1]+j
                        crossword = crossword[:temp] + '#' + crossword[temp+1:]
                if row >= dims[0]-3:
                    for j in range(row+1, dims[1]):
                        temp = i*dims[1]+j
                        crossword = crossword[:temp] + '#' + crossword[temp+1:]
    seededX = [i for i in range(len(crossword)) if crossword[i]=='#']
    seeded += [i for i in seededX if i not in seeded]
    for val in seeded:
        row = val//dims[1]
        col = val%dims[1]
        temp = (dims[0]-row-1)*dims[1]+dims[1]-col-1
        if temp not in seeded:
            if val in seededX: 
                crossword = crossword[:temp] + '#' + crossword[temp+1:]
                seededX.append(temp)
            else: crossword = crossword[:temp] + '-' + crossword[temp+1:]
            seeded.append(temp)
    problems = []
    for val in seededX: problems += produce_conflicts(dims, val, crossword, False)
    problems = list(set(problems))
    while len(problems)!=0:
        seededX += problems
        seeded += problems
        for val in problems: crossword = crossword[:val] + '#' + crossword[val+1:]
        problems.clear()
        for val in seededX: problems += produce_conflicts(dims, val, crossword, False)
        problems = list(set(problems))
    if sqrs%2==1:
        mid = (len(crossword)-1)/2
        if mid not in seededX: 
            crossword = crossword[:mid] + '#' + crossword[mid+1:]
            seededX.append(mid)
            seeded.append(mid)
    temp = [False for i in range(len(crossword))]
    area = area_fill(crossword.index('*'), dims, temp, crossword)
    if temp.count(False)!=0:
        for i in range(len(temp)):
            if temp[i] == False: crossword = crossword[:i] + '#' + crossword[i+1:]
    crossword = spiral_fill(dims, sqrs, crossword)
    pastStates.append(crossword)
    crossword = construct(dims, sqrs, crossword)
    for i in range(len(crossword)):
        if crossword[i]=='*': crossword = crossword[:i] + '-' + crossword[i+1:]
    
print(crossword)
#toGrid(dims, crossword)

# Ramya Reddy, 2, 2023