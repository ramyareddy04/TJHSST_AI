# Question #102
def shoelace(points):
    return abs(points[0]*(points[3]-points[5])+points[2]*(points[5]-points[1])+points[4]*(points[1]-points[3]))/2
def contains_origin(points):
    points[0] = int(points[0])
    points[1] = int(points[1])
    points[2] = int(points[2])
    points[3] = int(points[3])
    points[4] = int(points[4])
    points[5] = int(points[5])
   
    tot = shoelace(points)
    a = shoelace([points[0], points[1], points[2], points[3], 0, 0])
    b = shoelace([points[0], points[1], points[4], points[5], 0, 0])
    c = shoelace([points[4], points[5], points[2], points[3], 0, 0])
    return a+b+c==tot
count = 0
with open("./p102_triangles.txt","r") as f:
    line = f.readline()
    while line:
        if contains_origin(line.split(',')):
            count += 1
        line = f.readline()
print("#102: ", count)

# Question #112
def isBouncy(num):
     s = repr(num)
     isIncreasing = False
     isDecreasing = False
     for i in range(1, len(s)):
        if s[i] > s[i-1]:
            isIncreasing = True
        elif s[i] < s[i-1]:
            isDecreasing = True
     return isIncreasing and isDecreasing
curr = 99 # no bouncy numbers before 100
count = 0
while (count != (curr*.99)):
    curr += 1
    if isBouncy(curr):
        count += 1
print("#112: ", curr)

# Question #145
def is_reversible(num):
    for ch in str(num):
        if ch in '02468':
            return False
    return True
count = 0
for i in range(10, 100000000, 2): # no reversible numbers before 10 or after 100000000 (I know, I checked :'))
    if i%10!=0 and is_reversible(i+int((repr(i))[::-1])):
        count+=2
print("#145: ", count)

# Question #206
concealed_square = '1_2_3_4_5_6_7_8_9_0'
upper_lim = str(int(concealed_square[0])+1)
lower_lim = concealed_square[0]
for i in range(1, len(concealed_square)):
    upper_lim += '0'
    lower_lim += '0'
upper_lim = int(int(upper_lim)**(1/2))
lower_lim = int(int(lower_lim)**(1/2))
for i in range(lower_lim, upper_lim, 10):
    temp = i**2
    s = str(temp)
    if(s[0]=='1' and s[2]=='2' and s[4]=='3' and s[6]=='4' and s[8]=='5' and s[10]=='6' and s[12]=='7' and s[14]=='8' and s[16]=='9' and s[18]=='0'):
        print("#206: ", i)
        break