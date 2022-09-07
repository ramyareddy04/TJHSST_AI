import sys
import time

n=3
length = int(sys.argv[2])
inpWord = sys.argv[3].lower() if len(sys.argv) > 3 else ''
oppPlayer = [i for i in [j for j in range(n)] if i != (len(inpWord)+1)%n]

alph = 'abcdefghijklmnopqrstuvwxyz'
allWords = {ch:set() for ch in alph} if inpWord == '' else {inpWord[0] : set()}
tree = {ch:{} for ch in alph} if inpWord == '' else {inpWord[0] : {}}

def create_dict():
	with open("./"+sys.argv[1],"r") as f:
		start = time.perf_counter()
		for line in f:
			temp = line.strip().lower()
			if temp.isalpha() and len(temp) >= length and temp[:len(inpWord)]==inpWord:
				idx = temp[0]
				idx2 = len(inpWord)
				if len(temp)==idx2:
					smallest = temp
				else:
					smallest = temp[:idx2]
					while smallest not in allWords[idx] and idx2 <= len(temp):
						smallest = temp[:idx2]
						idx2 += 1	
				allWords[idx].add(smallest)
	
	for ch in allWords.keys():
		for word in allWords[ch]:
			branch = tree[ch]
			for char in word[1:]:
				if char not in branch.keys():
					branch[char] = {}
					branch = branch[char]
				else: branch = branch[char]
	
def game_over(word):
	if word != '':
		if word in allWords[word[0]]:
			return -1 if len(word)%n in oppPlayer else 1
	return 0

def possible_moves(word):
	if word!='':
		branch = tree[word[0]]
		for ch in word[1:]:
			branch = branch[ch]
		return list(branch.keys())
	else: return [ch for ch in alph]

def minimax(word):
	score = game_over(word)
	if score != 0: return score
	currPlayer = (len(word)+1)%n
	results = list()
	for next_move in possible_moves(word):
		results.append(minimax(word+next_move))
	return min(results) if currPlayer not in oppPlayer else max(results)

def winning_moves():
	moves = possible_moves(inpWord)
	result = [minimax(inpWord+pos) for pos in moves]
	bestMoves = []
	for i in range(len(moves)):
		if result[i] == -1: bestMoves.append(moves[i].upper())
	if len(bestMoves)!=0: print("Next player can guarantee victory by playing any of these letters:\t",bestMoves)
	else: print("Next player will lose!")

create_dict()
winning_moves()