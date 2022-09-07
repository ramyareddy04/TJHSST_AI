import sys

f = open("tetrisout.txt", "w")
test = sys.argv[1]

columns = []
for i in range(10):
    for j in range(i, 200, 10):
        if test[j]=='#': 
            columns.append((j-i)//10)
            break

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

def place(state, place, piece, difference):
    numR = len(piece)//len(difference)
    calc = [columns[i+place]-difference[i]-numR for i in range(len(difference))]
    idx = min(calc)

    if idx < 0: return 'GAME OVER'
    temp = list(state)
    for i, v in enumerate(piece):
        if v == '*':
            temp[(idx+(i//len(difference)))*10+place+(i%len(difference))] = '#'
    state = ''.join(temp)
    rows = [state[i:i+10].count('#') for i in range(0,200,10)]
    while 10 in rows:
        idx = rows.index(10)
        state = '          ' + state[:idx*10] + state[idx*10+10:]
        rows.remove(10)
        rows = [0] + rows
    return state

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

for type in pieces.keys():
    for size in pieces[type].keys():
        for idx, piece in enumerate(pieces[type][size]):
            for i in range(0, 10-size+1):
                f.write(place(test, i, piece, difs[type][size][idx])+'\n')
f.close()