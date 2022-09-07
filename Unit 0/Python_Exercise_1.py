import sys

if(sys.argv[1]=="A"):
	print(int(sys.argv[2])+int(sys.argv[3])+int(sys.argv[4]))
if(sys.argv[1]=="B"):
	sum = 0
	for i in range(2, len(sys.argv)):
		sum += int(sys.argv[i])
	print(sum)
if(sys.argv[1]=="C"):
	output = []
	for i in range(2, len(sys.argv)):
		if int(sys.argv[i])%3==0:
			output.append(sys.argv[i])
	print(output)
if(sys.argv[1]=="D"):
	n = 0
	m = 1
	for i in range(0, int(sys.argv[2])):
		print(m)
		temp = n + m
		n = m
		m = temp
if(sys.argv[1]=="E"):
	for i in range(int(sys.argv[2]), int(sys.argv[3])+1):
		print((i**2)-(3*i)+2)
if(sys.argv[1]=="F"):
	p = (float(sys.argv[2])+float(sys.argv[3])+float(sys.argv[4]))/2.0
	area = p*(p-float(sys.argv[2]))*(p-float(sys.argv[3]))*(p-float(sys.argv[4]))
	if(area>0):
		print(area**(1/2))
	else:
		print("ERROR: SIDE LENGTHS DO NOT CREATE TRIANGLE")
if(sys.argv[1]=="G"):
	dict = {'a':0, 'e':0, 'i':0, 'o':0, 'u':0}
	for i in range(0, len(sys.argv[2])):
		if sys.argv[2].lower()[i] in 'aeiou':
			dict[sys.argv[2][i]]+=1
	print(dict)