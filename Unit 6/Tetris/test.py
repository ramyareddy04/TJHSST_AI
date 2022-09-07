f = open("tetrisout.txt", "r")

for board in f:
    points = 0
    rows = [board[i:i+10].count('#') for i in range(0,200,10)]
    if 10 in rows:
        if rows.count(10)==1: points += 40
        elif rows.count(10)==2: points += 100 
        elif rows.count(10)==3: points += 300 
        else: points += 1200 
        for i, v in enumerate(rows): 
            if v == 10: board = '          ' + board[:i*10] + board[i*10+10:]
    print(points)