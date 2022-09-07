from collections import deque
import time
import sys

class Car:

    def __init__(self, label, currX, currY, dir, type):
        self.label = label
        self.x = currX
        self.y = currY
        self.dir = dir
        self.type = type

    def move(direction):
        if(self.dir == 'H'):
            self.x += direction
        else:
            self.y += direction

def print_puzzle(size=6, string=''):
    for i in range(0, len(string), size):
        print(' '.join(string[i:i+size])+' ')
    return ''

def find_goal(cars):
    for car in cars:
        if car.x == 4 and car.y == 2 and car.dir == 'H' and car.type == '2':
            return True
    return False

def find_cars(string):
    modStr = ''.join(sorted(string))
    maxCar = modStr[-1]
    allCars = []
    for i in range(int(maxCar)+1):
        count = string.count(str(i))
        temp = string.find(str(i))
        row = temp%6
        col = temp//6
        next = (string[temp+1:].find(str(i))+temp+1)%6
        if next==(temp%6):
            dir = 'V'
        else:
            dir = 'H'
        allCars.append(Car(str(i), row, col, dir, count))
    return allCars

def get_children_car(size=6, car = Car('', 0, 0, '', 0), string=''):
    idx = string.index(car.label)
    list = []

    if(car.dir == 'H'):
        c = ''.join([car.label for i in range(car.type)])
        neg_directions = [i for i in range(1,car.x+1)]
        pos_directions = [i for i in range(1, (size-car.x-car.type)+1)]
        for move in neg_directions:
            if string[idx-move]=='.':
                curr = string[:idx-move] + c + string[idx-move:idx] + string[idx+car.type:]
                list.append(curr)
            else:
                break
        for move in pos_directions:
            if string[idx+car.type+move-1]=='.':
                curr = string[:idx] + string[idx+move+car.type:idx+(2*move)+car.type] + c + string[idx+move+car.type:]
                list.append(curr)
            else:
                break
    else:
        print(string)
        c = ''.join([car.label for i in range(car.type)])
        neg_directions = [i for i in range(1, (car.y)+1)]
        pos_directions = [i for i in range(1,size-car.type-car.y+1)]
        for move in neg_directions:
            if string[idx-size*move]=='.':
                curr = (string[:idx-size*move])
                for i in range(0, move+1):
                    if i==move:
                        curr += string[idx-size*(move-i):]
                    else:
                        curr += str(car.label) + string[idx-size*(move-i):idx-size*(move-i-1)]
                    print(curr)
                #print(string[idx+size*car.type:])
                #print(curr)
                list.append(curr)
            else:
                break
        for move in pos_directions:
            if string[idx+car.type+move-1]=='.':
                curr = string[:idx] + string[idx+move+car.type:idx+(2*move)+car.type] + c + string[idx+move+car.type:]
                list.append(curr)
            else:
                break
    return list


def get_children(size=6, list=[], string=''):
    all_child = []
    for car in list:
        all_child += get_children_car(size, car, string)
    return all_child

def goal_test(string): # change
    return string == find_goal(string) # 1x2 car left (5,3)

def show_moves(length, path):
    print([move for move in path])

def BFS(string, printPath):
    fringe = deque([[string, [string]]])
    visited = set([string])
    length = int(len(string)**(1/2))
    
    while len(fringe)!=0:
        v = fringe.popleft()
        if goal_test(''.join(v[0])):
            if printPath:
                show_moves(length, v[1])
            return len(v[1])-1
        for c in get_children(length, v[0]):
            if c not in visited:
                visited.add(c)
                fringe.append([c, v[1] + [c]])
    return None

print_puzzle(string=sys.argv[1])
cars =  find_cars(sys.argv[1])
#print(cars[6].label, cars[6].x, cars[6].y, cars[6].dir, cars[6].type)
#print(get_children_car(car=cars[2], string=sys.argv[1]))
print(find_goal(cars))
#for car in cars:
#    print(car.label, car.x, car.y, car.dir, car.type)