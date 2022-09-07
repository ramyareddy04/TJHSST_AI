from heapq import heappush, heappop, heapify
import time
import sys
# code from distanceDemo.py
from math import pi , acos , sin , cos

def calcd(node1, node2):
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # all assumed to be in decimal degrees
   y1, x1 = node1
   y2, x2 = node2

   if x1==x2 and y1==y2:
       return 0

   R   = 3958.76 # miles = 6371 km
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0

   # approximate great circle distance with law of cosines
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

with open("./rrNodes.txt","r") as f:
    line_list = [line.strip() for line in f]    
    nodes = {f[:7] : [float(f[8:17]), float(f[18:])] for f in line_list}

s = time.perf_counter()

with open("./rrEdges.txt","r") as f:
    line_list = [line.strip() for line in f]
    edges = {node : [] for node in nodes}
    for line in line_list:
        temp = line.split()
        dist = calcd(nodes[temp[0]], nodes[temp[1]])
        edges[temp[0]] += [[temp[1], dist]]
        edges[temp[1]] += [[temp[0], dist]]

print('Time to create data structure: ',time.perf_counter()-s)

with open("./rrNodeCity.txt","r") as f:
    line_list = [line.strip() for line in f]
    names = {f[8:] : f[:7] for f in line_list}

def dijkstra(start, goal):
    closed = set()
    fringe = []
    start_node = (0, start)
    heappush(fringe, start_node)
    while len(fringe)!=0:
        v = heappop(fringe)
        if v[1]==goal:
            return v[0]
        if v[1] not in closed:
            closed.add(v[1])
            for c in edges[v[1]]:
                if c[0] not in closed:
                    temp = (v[0]+c[1], c[0])
                    heappush(fringe, temp)
    return None

def a_star(start, goal):
    closed = set()
    fringe = []
    start_node = (calcd(nodes[start], nodes[goal]),0, start)
    heappush(fringe, start_node)
    while len(fringe)!=0:
        v = heappop(fringe)
        if v[2]==goal:
            return v[1]
        if v[2] not in closed:
            closed.add(v[2])
            for c in edges[v[2]]:
                if c[0] not in closed:
                    depth = v[1]+c[1]
                    temp = (depth+calcd(nodes[c[0]], nodes[goal]),depth, c[0])
                    heappush(fringe, temp)
    return None

first = names[sys.argv[1]]
second = names[sys.argv[2]]

s = time.perf_counter()
d = dijkstra(first, second)
print(sys.argv[1], ' to ', sys.argv[2], ' with Dijkstra: ', d, ' in ',(time.perf_counter()-s),' seconds')
s = time.perf_counter()
a_s = a_star(first, second)
print(sys.argv[1], ' to ', sys.argv[2], ' with A*: ', a_s, ' in ',(time.perf_counter()-s),' seconds')
