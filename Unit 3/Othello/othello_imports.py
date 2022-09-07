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
    for place in range(len(temp)):
        if temp[place]==otherPlayer:
            dir = [-11, -10, -9, -1, 1, 9, 10, 11]
            for way in dir:
                if temp[place-way]==token and temp[place+way]!=token:
                    inc = way
                    while temp[place+inc]!= '?' and (place+inc)>=0 and (place+inc)<100 and temp[place+inc] == otherPlayer: inc += way
                    if temp[place+inc]!= '?' and (place+inc)>=0 and (place+inc)<100 and temp[place+inc] == '.': moves.add(place+inc-11-(2*(-1 + (place+inc)//10)))
    return list(moves)

def make_move(board, token, index):
    otherPlayer = 'o' if token == 'x' else 'x'
    temp = convert_board(board)
    moves = []
    dir = [-11, -10, -9, -1, 1, 9, 10, 11]
    accDir = [-9, -8, -7, -1, 1, 7, 8, 9]
    index2 = index + 11 + (2*(index//8))
    for way in dir:
        if temp[index2+way]==otherPlayer:
                inc = way
                while temp[index2+inc]!= '?' and (index2+inc)>=0 and (index2+inc)<100 and temp[index2+inc] == otherPlayer: inc += way
                if temp[index2+inc]== token and (index2+inc)>=0 and (index2+inc)<100: moves.append(way)
    s = temp[:index2] + token + temp[index2+1:]    
    for i in moves:
        inc = i
        while s[index2+inc] == otherPlayer: 
            s = s[:index2+inc] + token + s[index2+inc+1:]
            inc += i
    return convert_back(s)