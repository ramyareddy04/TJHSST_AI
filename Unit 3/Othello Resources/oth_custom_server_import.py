import time
import sys
import random

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

def get_score(board, token):
    val = 0
    piecesX = board.count('x')
    piecesY = board.count('o')
    movesX = len(possible_moves(board, 'x'))
    movesY = len(possible_moves(board, 'o'))
    if board.count('.')==0 or movesX+movesY==0:
        win = 999999 if token == 'x' else -999999
        winRatio = board.count(token)/(piecesX+piecesY)
        return win*winRatio if winRatio < 0.75 else 2*win*winRatio
    else: 
        if board.count('.') < 8:
            val = 1000*board.count(token) if token=='x' else -1000*board.count(token)
        else:
            diffP = 11*(piecesX-piecesY)/(piecesX+piecesY)
            diffM = 12*(movesX-movesY)/(movesX+movesY) if movesX+movesY!=0 else 0
            corners = [board[i] for i in [0,7,56,63]]
            if ('x' or 'o') in corners:
                diffC = 24*(corners.count('x')-corners.count('o'))/(corners.count('x')+corners.count('o'))
                opp = 0
                my = 0
                adj = {0:[1,8,9], 7:[6,14,15], 56:[48,49,57], 63:[54,55,62]}
                for key in adj.keys():
                    for val in adj[key]:
                        if board[key] in [token, '.']:
                            if board[val] not in [token, '.']: opp += 1
                        if board[key] != token:
                            if board[val] == token: my+=1
                diffA = 10*(opp-my)/(my + opp) if my+opp!=0 else 0
                if token == 'o': diffA *= -1
                return diffP+diffM+diffC+diffA
            else:
                return diffP + diffM

def find_next_move_pruning(board, player, depth, alpha, beta):
   otherPlayer = 'o' if player == 'x' else 'x'
   score = get_score(board, player)
   if board.count('.') == 0 or depth == 0: return score
   else:
       pos = possible_moves(board, player)
       if len(pos)==0: return -find_next_move_pruning(board, otherPlayer, depth-1, -alpha, -beta)
       else:
           results = list()
           for idx in pos:
                 # ALPHA/BETA PRUNING HERE
               val = -find_next_move_pruning(make_move(board, player, idx), otherPlayer, depth-1, -beta, -alpha)
               if val >= beta: return val
               if val >= alpha: alpha = val
   return alpha

def find_next_move(board, player, depth):
    nextPlayer = 'o' if player == 'x' else 'x'
    ways = possible_moves(board, player)
    nextStates = [-find_next_move_pruning(make_move(board, player, way), nextPlayer, depth, float('inf'), float('-inf')) for way in ways]
    val = ways[nextStates.index(max(nextStates))] if player == 'x' else ways[nextStates.index(min(nextStates))]
    return val

class Strategy():
   logging = True  # Optional
   def best_strategy(self, board, player, best_move, still_running):
       depth = 1
       for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
           best_move.value = find_next_move(board, player, depth)
           depth += 1