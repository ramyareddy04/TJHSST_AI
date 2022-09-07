import sys

try:
    sys.argv[1] = int(sys.argv[1])
    print("is an integer")
    DFAS = [
        ['ab\n5\n3', '0\na 1', '1\na 2', '2\nb 3', '3', '4'],
        ['012\n2\n1', '0\n0 0\n1 1\n2 0', '1\n0 0\n1 1\n2 0'],
        ['abc\n2\n1', '0\na 0\nb 1\nc 0', '1\na 1\nb 1\nc 1'],
        ['01\n2\n0', '0\n0 1\n1 0', '1\n0 0\n1 1'],
        ['01\n4\n0', '0\n0 2\n1 1', '1\n0 3\n1 0', '2\n0 0\n1 3', '3\n0 1\n1 2'],
        ['abc\n4\n0 1 2', '0\na 1\nb 0\nc 0', '1\na 1\nb 2\nc 0', '2\na 0\nb 0\nc 3', '3'],
        ['01\n5\n4', '0\n0 0\n1 1', '1\n0 2\n1 1', '2\n0 2\n1 3', '3\n0 2\n1 4', '4\n0 4\n1 4']
        ]
    f = DFAS[sys.argv[1]-1]
except ValueError:
    f = open("./"+sys.argv[1],"r").read().split('\n\n')

alph, states, finStates = f[0].split('\n')
states = {i:{} for i in range(int(states))}
finStates = [int(i) for i in finStates.split()]
for i in range(1, len(f)):
    info = f[i].split('\n')
    for j in range(1, len(info)):
        info2 = info[j].split()
        states[int(info[0])][info2[0]] = int(info2[1])

string = '*\t'
for ch in alph: string += ch+'\t'
string += '\n'
for i, state in enumerate(states.keys()):
    string += str(state)+'\t'
    for ch in alph:
        string += '_\t' if ch not in states[state].keys() else str(states[state][ch])+'\t'
    string += '\n'
string += 'Final nodes: '+str(finStates)+'\n'

with open("./"+sys.argv[2],"r") as f:
    for line in f:
        curr = 0
        for ch in line.strip():
            if ch in states[curr]: curr = states[curr][ch]
            else: 
                curr = -1
                break
        string += 'True  ' if curr in finStates else 'False '
        string += line

print(string)