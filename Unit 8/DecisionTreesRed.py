import sys
import math
import random
import matplotlib.pyplot as plt

tree = {}
total = 0

def split_csv_line(x):
	x = x.split(',')
	if x[-1][-1] == '\n': x[-1] = x[-1][:-1]
	return x

def split_test_train(n, attrs):
	idxes = [i for i in range(total)]
	random.shuffle(idxes)
	train = {key:[attrs[key][i] for i in idxes[:-n]] for key in attrs.keys()}
	test = {key:[attrs[key][i] for i in idxes[-n:]] for key in attrs.keys()}
	return train, test

def calculate_entropy(idx, features, data):
	vals = set(data[features[idx]])
	entropy = 0
	for val in vals:
		idxes = [outcome for i, outcome in enumerate(data[features[-1]]) if data[features[idx]][i]==val]
		outcomes = list(set(idxes))
		if idx!=len(features)-1: 
			temp_e = 0
			for outcome in outcomes:
				if idxes.count(outcome)!=0: temp_e += (idxes.count(outcome)/len(idxes))*math.log(idxes.count(outcome)/len(idxes), 2)
		else:
			temp_e = math.log(len(idxes)/len(data[features[-1]]), 2)
		entropy -= (len(idxes)/len(data[features[-1]]))*(temp_e)
	return entropy

def make_new_split(features, idx, type, data):
	idxes = [i for i in range(len(data[idx])) if data[idx][i]==type]
	
	new_features = [feature for feature in features if feature!=idx]
	new_data = {}
	for feature in features:
		if feature!=idx: new_data[feature] = [data[feature][i] for i in idxes]
	return new_features, new_data

def make_ideal_tree(n, branch, curr, features, data):
	dE = [calculate_entropy(i, features, data) for i in range(0,len(features)-1)]
	if max(dE) == min(dE) and max(dE)!=0.0:
		branch[curr] = random.choice(list(set(data[features[-1]])))
		return
	next = features[dE.index(min(dE))] if max(dE)!=0.0 else ''
	if next!='' and min(dE)!=0.0:
		if n!=0: 
			branch[curr] = {next:{}}
			branch = branch[curr]
			curr = next
			n+=1 
		else:
			curr = next
		branch[curr] = {feature:{} for feature in set(data[next])}
	elif next!='':
		if n!=0: 
			branch[curr] = {next:{feature:'' for feature in set(data[next])}}
			for val in set(data[next]):
				branch[curr][next][val] = data[features[-1]][data[next].index(val)]
		else:
			branch[next] = {feature:'' for feature in data[next]}
			for val in set(data[next]):
				branch[next][val] = data[features[-1]][data[next].index(val)]
	else:
		branch[curr] = data[features[-1]][0]
	if min(dE) == 0.0: return
	vals = set(data[next])
	for val in vals:
		new_features, new_data = make_new_split(features, next, val, data)
		make_ideal_tree(n+1, branch[curr], val, new_features, new_data)


f = open(sys.argv[1], "r")
features = split_csv_line(f.readline())
nonmissing = {feature:[] for feature in features}
for line in f:
	x = split_csv_line(line)	
	for i, feature in enumerate(features): nonmissing[feature].append(x[i])
	total += 1
#opt1 = [{'y':0, 'n':0} for i in range(1, len(features)-1)]
#opt2 = [{'y':0, 'n':0} for i in range(1, len(features)-1)]
#idx = 0
#for line in f:
#	x = split_csv_line(line)	
#	total += 1
#	for i, feature, in enumerate(x[1:-1]):
#		if idx == 0: 
#			result = x[-1]
#			idx +=1 
#		if feature != '?': 
#			if x[-1]==result: opt1[i-1][feature] = opt1[i-1][feature]+1
#			else: opt2[i-1][feature] = opt2[i-1][feature]+1

#for i in range(len(opt1)):
#	opt1[i] = 'y' if opt1[i]['y'] > opt1[i]['n'] else 'n'
#	opt2[i] = 'y' if opt2[i]['y'] > opt2[i]['n'] else 'n'

#nonmissing = {feature:[] for feature in features}
#f = open("house-votes-84.csv", "r")
#_ = split_csv_line(f.readline())
#for line in f:
#	x = split_csv_line(line)
#	for i, feature in enumerate(features): 
#		if x[i]!='?': nonmissing[feature].append(x[i])
#		else: nonmissing[feature].append(opt1[i-1] if x[-1]==result else opt2[i-1])

train, test = split_test_train(int(sys.argv[2]), nonmissing)
accuracies =  []
for size in range(int(sys.argv[3]),int(sys.argv[4]), int(sys.argv[5])):
	temp_train = set()
	temp_train.add(random.randint(0, total-int(sys.argv[2])-1))
	outcome = train[features[-1]][list(temp_train)[0]]
	while len(temp_train)!=2:
		temp = random.randint(0, total-int(sys.argv[2])-1)
		if train[features[-1]][temp]!=outcome: temp_train.add(temp)
	while len(temp_train)!=size:
		temp_train.add(random.randint(0, total-int(sys.argv[2])-1))
	attrs = {feature:[train[feature][idx] for idx in temp_train] for feature in features}
	make_ideal_tree(0, tree, '', features, attrs)
	accuracy = 0
	for i in range(int(sys.argv[2])):
		branch = tree
		while type(branch) != str:
			key = list(branch.keys())[0]
			outcome = test[key][i]
			if outcome not in branch[key].keys(): 
				branch = random.choice(list(set(attrs[features[-1]])))
			else: branch = branch[key][outcome]
		if branch == test[features[-1]][i]: accuracy += 1
	accuracy*=100/int(sys.argv[2])
	accuracies.append(accuracy)
	tree = {}

plt.plot([idx for idx in range(int(sys.argv[3]),int(sys.argv[4]), int(sys.argv[5]))], accuracies)
plt.show()