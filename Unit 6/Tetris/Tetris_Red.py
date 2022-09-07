import random, time

POPULATION_SIZE = 100
NUM_CLONES = 25
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = .75
MUTATION_RATE = 0.01

def difference(piece, size):
    net = []
    numR = size*((len(piece)//size)-1)
    for i in range(size):
        for j in range(i+numR, i, -size):
            if piece[j]=='*': 
                break
            if piece[j]==' ' and piece[j-size]!=' ':
                net += [-(i+numR+size-j)//size]
                break
        if len(net)!=i+1: net += [0]
    return net

pieces = {'I':{1:['****'], 4:['****']}, 
          'O':{2:['****']},
          'T':{2:['* *** ', ' *** *'], 3:[' * ***', '*** * ']},
          'S':{2:['* ** *'], 3:[' **** ']},
          'Z':{2:[' **** '], 3:['**  **']},
          'J':{2:['*** * ', ' * ***'], 3:['*  ***', '***  *']},
          'L':{2:['* * **', '** * *'], 3:['  ****', '****  ']}
          }
difs = {'I':{}, 'O':{}, 'T':{}, 'S':{}, 'Z':{}, 'J':{}, 'L':{}}

for type in pieces.keys():
    for size in pieces[type].keys():
        difs[type][size] = [difference(orientation, size) for orientation in pieces[type][size]]

def heuristic(board, strategy):
    a, b, c, d = strategy
    rows = [board[i:i+10].count('#') for i in range(0,200,10)]
    cols = [[board[j] for j in range(i, 200, 10)] for i in range(10)]
    tops = []
    for i in range(10): tops.append(20-cols[i].index('#')) if '#' in cols[i] else tops.append(0)
    holes = [1 for i in range(0,190) if board[i]=='#' and board[i+10]==' ']
    val = 0
    val += a * sum(tops) # sum col
    val += b * sum(holes) # sum holes 
    val += c * rows.count(10) # rows cleared
    val += d * sum([abs(tops[i]-tops[i+1]) for i in range(0,9)]) # bumpiness
    return val

def place(state, place, piece, difference, columns):
    numR = len(piece)//len(difference)
    calc = [columns[i+place]-difference[i]-numR for i in range(len(difference))]
    idx = min(calc)
    if idx < 0: return 'GAME OVER'
    temp = list(state)
    for i, v in enumerate(piece):
        if v == '*':
            temp[(idx+(i//len(difference)))*10+place+(i%len(difference))] = '#'
    state = ''.join(temp)
    return state

def play_game(strategy, forUI):
    board = ''.join([' ' for i in range(200)])
    points = 0
    while board != 'GAME OVER':
        can_move = False
        best = ('', -999999999)
        type = random.choice(list(pieces.keys()))
        columns = []
        for i in range(10):
            for j in range(i, 200, 10):
                if board[j]=='#': 
                    columns.append((j-i)//10)
                    break
            if len(columns)!=i+1: columns.append(20)
        for size in pieces[type].keys():
            for idx, piece in enumerate(pieces[type][size]):
                for i in range(0, 10-size+1):
                    pos_board = place(board, i, piece, difs[type][size][idx], columns)
                    if pos_board == 'GAME OVER': break
                    can_move = True
                    score = heuristic(pos_board, strategy)
                    if score > best[1]: best = (pos_board, score)
        if can_move == True:
            board = best[0]
            rows = [board[i:i+10].count('#') for i in range(0,200,10)]
            if 10 in rows:
                if rows.count(10)==1: points += 40
                elif rows.count(10)==2: points += 100
                elif rows.count(10)==3: points += 300
                else: points += 1200
                for i, v in enumerate(rows):
                    if v == 10:
                        board = '          ' + board[:i*10] + board[i*10+10:]
        if forUI:
            print("=======================")
            for count in range(20):
                print(' '.join(list(("|" + board[count * 10: (count + 1) * 10] + "|"))), " ", count)
            print("=======================")
            print("Current score:",points)
        if can_move==False: return points
    return points

def generate_population():
    population = []
    while len(population)!=POPULATION_SIZE:
        n = [random.uniform(-0.5, 0.5) for i in range(4)]           #
        if n not in population: population.append(n)
    return population

def fitness(strategy):
    game_scores = 0
    for i in range(5): game_scores += play_game(strategy, False)
    return game_scores/5

def store_fitness(generation):
    fitness_scores = {}
    avg = 0
    for i, strategy in enumerate(generation): 
        fitness_scores[str(strategy)] = fitness(strategy)
        avg += fitness_scores[str(strategy)]
        print("Evaluating strategy number",i, "-->", fitness_scores[str(strategy)])
    return dict(sorted(fitness_scores.items(), key=lambda item: item[1], reverse=True)), avg/POPULATION_SIZE

def create_children(generation, fitness):
    next_generation = []
    for child in list(fitness.keys())[:NUM_CLONES]: next_generation.append([float(v) for v in child[1:-1].split(', ')])
    while len(next_generation) != POPULATION_SIZE:
        # SELECTION
        tournament = random.sample(list(fitness.keys()), 2*TOURNAMENT_SIZE)
        tournament = [(v, fitness[v]) for v in tournament]
        t1 = sorted(tournament[:TOURNAMENT_SIZE], key=lambda item:item[1], reverse=True)
        p1 = t1[-1][0]
        for i in range(TOURNAMENT_SIZE):
            if random.random() < TOURNAMENT_WIN_PROBABILITY:
                p1 = t1[i][0][1:-1].split(', ')
                break
        t2 = sorted(tournament[TOURNAMENT_SIZE:], key=lambda item:item[1], reverse=True)
        p2 = t2[-1][0]
        for i in range(TOURNAMENT_SIZE):
            if random.random() < TOURNAMENT_WIN_PROBABILITY:
                p2 = t2[i][0][1:-1].split(', ')
                break
        # BREEDING
        child = []
        randIdx = random.sample([i for i in range(len(p1))], random.randint(1,len(p1)-1))
        for i in range(len(p1)): child.append(float(p1[i])) if i in randIdx else child.append(float(p2[i]))
        # MUTATION
        if random.random() < MUTATION_RATE: 
            temp = random.randint(0, len(child)-1)
            child[temp] += random.uniform(-child[temp], 1-child[temp])
        if child not in next_generation: next_generation.append(child)
    return next_generation

def simulate():
    choice1 = input("(N)ew process, or (L)oad saved process? ")
    gen_cnt = 0
    if choice1.lower() == 'l':
        gen_cnt += 1
        filename = input("What file? ")
        stratFile = open(filename, "r").read().split('\n')
        p = []
        fitness_scrs = {}
        for strat in stratFile:
            if strat != '': 
                tempStrat = strat.split('  ')
                p.append([float(i) for i in tempStrat[0][1:-1].split(', ')])
                fitness_scrs[tempStrat[0]] = float(tempStrat[1])
    elif choice1.lower() == 'n':
        p = generate_population()
        fitness_scrs, avg = store_fitness(p)
        print("Average:",avg)
    print("Generation:",gen_cnt)
    print("Best strategy so far:", list(fitness_scrs.keys())[0],"with score:",fitness_scrs[list(fitness_scrs.keys())[0]])
    choice = input("(P)lay a game with current best strategy, (S)ave current process, or (C)ontinue? ")
    while choice.lower()!='s':
        if choice.lower() == 'p':
            play_game([float(i) for i in list(fitness_scrs.keys())[0][1:-1].split(', ')], True)
        elif choice.lower() == 'c':
            gen_cnt += 1
            p = create_children(p, fitness_scrs)
            fitness_scrs, avg = store_fitness(p)
            print("Average:",avg)
            print("Generation:",gen_cnt)
            print("Best strategy so far:", list(fitness_scrs.keys())[0],"with score:",fitness_scrs[list(fitness_scrs.keys())[0]])
        choice = input("(P)lay a game with current best strategy, (S)ave current process, or (C)ontinue? ")
    filename = input("What filename? ") # use a .txt file
    f = open(filename, "w")
    for strat in list(fitness_scrs.keys()): f.write(str(strat)+'  '+str(fitness_scrs[strat])+'\n')
    f.close()

simulate()