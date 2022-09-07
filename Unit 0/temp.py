import time
start_time = time.time()

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
print(curr)
print ("My program took", time.time() - start_time, "to run")