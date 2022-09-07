import time
import sys

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