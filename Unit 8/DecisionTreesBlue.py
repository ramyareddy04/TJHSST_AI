import sys
import math

file = open("treeout.txt", "w") 
tree = {}

def split_csv_line(x):
	x = x.split(',')
	if x[-1][-1] == '\n': x[-1] = x[-1][:-1]
	return x

def calculate_entropy(idx, features, data):
	vals = set(data[features[idx]])
	entropy = 0
	for val in vals:
		idxes = [outcome for i, outcome in enumerate(data[features[-1]]) if data[features[idx]][i]==val]
		outcomes = list(set(idxes))
		bad = outcomes[0]
		good = outcomes[1] if len(outcomes)>1 else 0
		if idx!=len(features)-1: 
			temp_e = (idxes.count(bad)/len(idxes))*math.log(idxes.count(bad)/len(idxes),2) if idxes.count(bad) != 0 else 0
			temp_e += (idxes.count(good)/len(idxes))*math.log(idxes.count(good)/len(idxes),2) if idxes.count(good) != 0 else 0
		else:
			temp_e = math.log(len(idxes)/len(data[features[-1]]), 2)
		entropy -= (len(idxes)/len(data[features[-1]]))*(temp_e)
	return entropy

def entropy_gain(past, curr):
	return past-curr

def make_new_split(features, idx, type, data):
	idxes = [i for i in range(len(data[idx])) if data[idx][i]==type]
	
	new_features = [feature for feature in features if feature!=idx]
	new_data = {}
	for feature in features:
		if feature!=idx: new_data[feature] = [data[feature][i] for i in idxes]
	return new_features, new_data

def write_to_file(val):
	val = str(val+'\n')
	file.write(val)

def make_ideal_tree(n, branch, curr, features, data):
	dE = [calculate_entropy(i, features, data) for i in range(len(features)-1)]
	next = features[dE.index(min(dE))] if max(dE)!=0.0 else ''
	if next!='' and min(dE)!=0.0:
		if n!=0: 
			write_to_file(''.join('\t' for i in range(n))+'* '+curr)
			branch[curr] = {next:{}}
			branch = branch[curr]
			curr = next
			n+=1 
		else:
			curr = next
		write_to_file(''.join('\t' for i in range(n))+'* '+next)
		branch[curr] = {feature:{} for feature in set(data[next])}
	elif next!='':
		write_to_file(''.join('\t' for i in range(n))+'* '+curr)
		write_to_file(''.join('\t' for i in range(n+1))+'* '+next+'?')
		branch[curr] = {next:{feature:'' for feature in data[next]}}
		for val in set(data[next]):
			write_to_file(''.join('\t' for i in range(n+2))+'* '+val+' --> '+data[features[-1]][data[next].index(val)])
			branch[curr][next][val] = data[features[-1]][data[next].index(val)]
	else:
		write_to_file(''.join('\t' for i in range(n))+'* '+curr+' --> '+data[features[-1]][0])
		branch[curr] = data[features[-1]][0]
	if min(dE) == 0.0: return
	vals = set(data[next])
	for val in vals:
		new_features, new_data = make_new_split(features, next, val, data)
		make_ideal_tree(n+1, branch[curr], val, new_features, new_data)

f = open(sys.argv[1], "r")
features = split_csv_line(f.readline())
attrs = {feature:[] for feature in features}
for line in f:
	x = split_csv_line(line)	
	for i, feature in enumerate(features): attrs[feature].append(x[i])
make_ideal_tree(0, tree, '', features, attrs)
print(tree)