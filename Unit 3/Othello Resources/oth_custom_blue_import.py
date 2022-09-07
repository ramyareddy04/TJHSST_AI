import time
import sys

board = sys.argv[1]
player = sys.argv[2]

weights = [
    120, -20,  20,   5,   5,  20, -20, 120,
    -20, -40,  1,  -5,  -5,  1, -40, -20,
    20,  1,  15,   4,   4,  15,  1,  20,
    5,  -5,   4,   2,   2,   4,  -5,   5, 
    5,  -5,   4,   2,   2,   4,  -5,   5, 
    20,  1,  15,   4,   4,  15,  1,  20,
    -20, -40,  1,  -5,  -5,  1, -40, -20,
    120, -20,  20,   5,   5,  20, -20, 120
    ]

def convert_board(board):
    s = ''
    for i in range(10): s+= '?'
    for i in range(0, len(board), 8): s += '?' + board[i:i+8] + '?'
    for i in range(10): s+= '?'
    return s

def convert_back(converted):
    s = ''
    for i in range(10, len(converted)-10, 10): s += converted[i+1: i+9]
    return s

def possible_moves(board, token):
    moves = set()
    temp = convert_board(board)
    otherPlayer = 'o' if token == 'x' else 'x'
    dir = [-11, -10, -9, -1, 1, 9, 10, 11]
    for place in range(11,89):
        if temp[place]==otherPlayer:
            for i, way in enumerate(dir):
                if temp[place-way]==token and temp[place+way]!=token:
                    inc = way
                    while temp[place+inc] == otherPlayer: inc += way
                    if temp[place+inc] == '.': moves.add(place+inc-11-(2*(-1 + (place+inc)//10)))
    return list(moves)

def make_move(board, token, index):
    otherPlayer = 'o' if token == 'x' else 'x'
    temp = convert_board(board)
    moves = []
    dir = [-11, -10, -9, -1, 1, 9, 10, 11]
    index2 = index + 11 + (2*(index//8))
    for way in dir:
        if temp[index2+way]==otherPlayer:
                inc = way
                while temp[index2+inc] == otherPlayer: inc += way
                if temp[index2+inc] == token: 
                    moves.append(way)
    s = temp[:index2] + token + temp[index2+1:]    
    for i in moves:
        inc = i
        while s[index2+inc] == otherPlayer: 
            s = s[:index2+inc] + token + s[index2+inc+1:]
            inc += i
    return convert_back(s)

def get_score(board, player):
    val = 0#(len(possible_moves(board, 'x')) - len(possible_moves(board, 'o')))*0.8
    for num in range(len(weights)):
        if board[num]=='x': val+=weights[num]
        elif board[num]=='o': val-=weights[num]
    return val #if player == 'x' else val*-1

def find_next_move(board, player, depth):
   otherPlayer = 'o' if player == 'x' else 'x'
   score = get_score(board, player)
   if board.count('.') == 0 or depth == 0: return score
   else:
       pos = possible_moves(board, player)
       results = list()
       if len(pos)==0:
           results.append(find_next_move(board, otherPlayer, depth-1))
       else:
           for idx in pos:
              results.append((find_next_move(make_move(board, player, idx), otherPlayer, depth-1)))
   return max(results) if player=='x' else min(results)

nextPlayer = 'o' if player == 'x' else 'x'
ways = possible_moves(board, player)
if len(ways) == 1: print(ways[0])
else:
    if len(ways) < 3: depth = 7 if player == 'x' else 5
    elif len(ways) < 5: depth = 4 #if player == 'x' else 5
    elif len(ways) < 16: depth = 3 #if player == 'o' else 4
    else: depth = 3 if player == 'x' else 2
    nextStates = [find_next_move(make_move(board, player, way), nextPlayer, depth) for way in ways] if player =='x' else [-find_next_move(make_move(board, player, way), nextPlayer, depth) for way in ways]
    print(ways[nextStates.index(max(nextStates))])