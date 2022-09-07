import random
import sys
import math

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
POPULATION_SIZE = 500 #200
NUM_CLONES = 1
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = .75
CROSSOVER_LOCATIONS = 5
MUTATION_RATE = 0.8

freq = {}
with open("./ngrams.txt","r") as f:
	for line in f: 
		temp = line.split()
		freq[temp[0]] = int(temp[1])

def encode(word, alph):
	newWord = ''
	for ch in word:
		if ch.upper() in letters:
			newWord += alph[letters.index(ch.upper())]
		else: newWord += ch
	return newWord

def decode(word, alph):
	newAlph = list(letters)
	newWord = ''
	for ch in word:
		if ch.upper() in letters:
			newWord += newAlph[alph.index(ch.upper())]
		else: newWord += ch
	return newWord

def generate_population():
	population = []
	while len(population) != POPULATION_SIZE:
		alph = list(letters)
		random.shuffle(alph)
		if alph not in population: population.append(alph)
	return population

def fitness(n, cipher, alph):
	word = decode(cipher, alph)
	total = 0
	for i in range(0, len(word)-n+1):
		if word[i:i+n] in freq.keys(): total += math.log(freq[word[i:i+n]], 2)
	return total

def store_fitness(n, encoded, generation):
	fitness_scores = {}
	avg = 0
	for parent in generation:
		fitness_scores[''.join(parent)] = sum([fitness(i, encoded, parent) for i in range(2, n+1)])
		avg += fitness_scores[''.join(parent)]
	return dict(sorted(fitness_scores.items(), key=lambda item: item[1], reverse=True)), avg/POPULATION_SIZE

def create_children(n, encoded, generation):
	current_fitness, avg = store_fitness(n, encoded, generation)
	next_generation = list(current_fitness.keys())[:NUM_CLONES]
	while len(next_generation) != POPULATION_SIZE:
		# SELECTION
		tournament = random.sample(list(current_fitness.keys()), 2*TOURNAMENT_SIZE)
		tournament = [(v, current_fitness[v]) for v in tournament]
		t1 = sorted(tournament[:TOURNAMENT_SIZE], key=lambda item:item[1], reverse=True)
		p1 = t1[-1][0]
		for i in range(TOURNAMENT_SIZE):
			if random.random() < TOURNAMENT_WIN_PROBABILITY:
				p1 = t1[i][0]
				break
		t2 = sorted(tournament[TOURNAMENT_SIZE:], key=lambda item:item[1], reverse=True)
		p2 = t2[-1][0]
		for i in range(TOURNAMENT_SIZE):
			if random.random() < TOURNAMENT_WIN_PROBABILITY:
				p2 = t2[i][0]
				break
		# BREEDING
		child = ['' for i in range(len(letters))]
		for v in random.sample(list([i for i in range(26)]), CROSSOVER_LOCATIONS):
			child[v] = p1[v]
		for v in p2:
			if v not in child: child[child.index('')] = v
		# MUTATION
		if random.random() < MUTATION_RATE:
			mutations = random.sample(list([i for i in range(26)]), 2)
			child[mutations[1]], child[mutations[0]] = child[mutations[0]], child[mutations[1]]
		if ''.join(child) not in next_generation: next_generation.append(''.join(child))
	return [list(v) for v in next_generation]

	
def hill_climb(encoded, n):
	alph = list(letters)
	random.shuffle(alph)
	currFitness = sum([fitness(i, encoded, alph) for i in range(1, n+1)])
	lastImprovement = 0
	while lastImprovement < 1000:
		child = alph.copy()
		pair = random.sample(child, 2)
		pair = [alph.index(i) for i in pair]
		temp = child[pair[0]]
		child[pair[0]] = child[pair[1]]
		child[pair[1]] = temp
		newFitness = sum([fitness(i, encoded, child) for i in range(1, n+1)])
		if newFitness > currFitness:
			print(decode(encoded, child), newFitness)
			currFitness = newFitness
			alph = child
			lastImprovement = 0
		else: lastImprovement += 1
	return alph

alph = list(letters)
random.shuffle(alph)
cipher = sys.argv[1]
w = encode(cipher, alph)
gen = create_children(3, w, generate_population())
for i in range(500):
	gen = create_children(3, w, gen)
	print(decode(w, gen[0]))