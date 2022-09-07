import sys

idxes = '012345678'

puzzle = sys.argv[1]
isComputerNext = True
computer = ''
player = ''
case = 1

if puzzle.count('.')==9:
	val = input("Should I be X or O? ")
	isComputerNext = False if val != 'X' else True
	case = 1 if val == 'X' else 2
else: case = 1 if puzzle.count('X') == puzzle.count('O') else 2

if case == 1:
	computer = 'X'
	player = 'O'
else:
	computer = 'O'
	player = 'X'

def print_board(string):
	print()
	print("Current board: ")
	for i in range(0, len(string), 3): 
		print(''.join(string[i:i+3]) + '\t' + idxes[i:i+3])
	print()

def game_over(string):
	x = ''
	o = ''
	for i, char in enumerate(string):
		if char == 'X': x+=str(i)
		elif char == 'O': o+=str(i)
	winStates = ['012', '345', '678', '036', '147', '258', '048', '246']
	for state in winStates:
		if state[0] in x and state[1] in x and state[2] in x: 
			return 1
		elif state[0] in o and state[1] in o and state[2] in o: 
			return -1
	if string.count('.')==0: return 0
	return -2

def possible_next_boards(board, isCompNext):
	boards = []
	for place in range(len(board)):
		if board[place] == '.': 
			if isCompNext: boards.append(board[:place] + computer + board[place+1:])
			else: boards.append(board[:place] + player + board[place+1:])
	return boards

def max_step(board, isCompNext):
	score = game_over(board)
	if score != -2: return score
	currentPlayer = computer if isCompNext else player
	results = list()
	for next_board in possible_next_boards(board, isCompNext):
		results.append(min_step(next_board, not isCompNext))
	return max(results) if currentPlayer == 'X' else min(results)

def min_step(board, isCompNext):
	score = game_over(board)
	if score != -2: return score
	currentPlayer = computer if isCompNext else player
	results = list()
	for next_board in possible_next_boards(board, isCompNext):
		results.append(max_step(next_board, not isCompNext))
	return max(results) if currentPlayer == 'X' else min(results)
	
def result(score):
	if score == 0:
		return "We tied!"
	else:
		if score == 1:
			return "I win!" if computer == 'X' else "You win!"
		else:
		    return "I win!" if computer == 'O' else "You win!"

def showPlayerMoves(moves):
	string = ''
	for i in range(len(moves)):
		string += str(moves[i])
		if i < len(moves) - 1: string += ', '
	return string + '.'

def showMoves(moves, idxes):
	loss = -1 if computer == 'X' else 1
	win = 1 if computer == 'X' else -1
	for i, move in enumerate(moves):
		if move == win: print("Moving at", idxes[i], "results in a win.")
		elif move == loss: print("Moving at", idxes[i], "results in a loss.")
		else: print("Moving at", idxes[i], "results in a tie.")
	
def makeChoice(moves, idxes):
	best = 1
	worst = -1
	if computer == 'O':
		best *= -1
		worst *= -1
	if best in moves: return idxes[moves.index(best)]
	elif 0 in moves: return idxes[moves.index(0)]
	else: return idxes[moves.index(worst)]

def do_game(board, isCompNext):
	print_board(board)
	score = game_over(board)
	if score != -2: return result(score)
	pos = [ch for ch in range(len(board)) if board[ch]=='.']
	if isCompNext:
		ways = [min_step(board[:idx] + computer + board[idx+1:], not isCompNext) for idx in pos]
		showMoves(ways, pos)
		idx = makeChoice(ways, pos)
		print()
		print("I chose space " + str(idx) + '.')
		board = board[:idx] + computer + board[idx+1:]
		return do_game(board, not isCompNext)
	else:
		print("You can move to any of these spaces:", showPlayerMoves(pos))
		idx = int(input("Your choice? "))
		board = board[:idx] + player + board[idx+1:]
		return do_game(board, not isCompNext)
	
print(do_game(puzzle, isComputerNext))