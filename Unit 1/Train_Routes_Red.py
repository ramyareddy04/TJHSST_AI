from heapq import heappush, heappop, heapify
import tkinter as tk
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

with open("./rrEdges.txt","r") as f:
    line_list = [line.strip() for line in f]
    edges = {node : [] for node in nodes}
    for line in line_list:
        temp = line.split()
        dist = calcd(nodes[temp[0]], nodes[temp[1]])
        edges[temp[0]] += [[temp[1], dist]]
        edges[temp[1]] += [[temp[0], dist]]

with open("./rrNodeCity.txt","r") as f:
    line_list = [line.strip() for line in f]
    names = {f[8:] : f[:7] for f in line_list}

def dijkstra(canvas, r, start, goal):
    closed = set()
    fringe = []
    start_node = (0, start, [start])
    heappush(fringe, start_node)
    times = 0
    while len(fringe)!=0:
        v = heappop(fringe)
        times += 1
        if v[1]==goal:
            return v[2]
        if v[1] not in closed:
            closed.add(v[1])
            for c in edges[v[1]]:
                if c[0] not in closed:
                    temp = (v[0]+c[1], c[0], v[2]+[c[0]])
                    heappush(fringe, temp)
                    canvas.itemconfig(lines[v[1]][c[0]], fill="red")
                    canvas.itemconfig(lines[c[0]][v[1]], fill="red")
                    if times%800==0:
                        r.update()
    return None

def a_star(canvas, r, start, goal):
    closed = set()
    fringe = []
    start_node = (calcd(nodes[start], nodes[goal]),0, start, [start])
    heappush(fringe, start_node)
    times = 0
    while len(fringe)!=0:
        v = heappop(fringe)
        times += 1
        if v[2]==goal:
            return v[3]
        if v[2] not in closed:
            closed.add(v[2])
            for c in edges[v[2]]:
                if c[0] not in closed:
                    depth = v[1]+c[1]
                    temp = (depth+calcd(nodes[c[0]], nodes[goal]),depth, c[0], v[3]+[c[0]])
                    heappush(fringe, temp)
                    canvas.itemconfig(lines[v[2]][c[0]], fill="blue")
                    canvas.itemconfig(lines[c[0]][v[2]], fill="blue")
                    if times%350==0:
                        r.update()
    return None

lines = {node : {} for node in edges} #list of all the lines created
def create_graph(c):
    scaleX = 11.2
    scaleY= 14
    dx = 1465
    dy = 875
    for node in edges:
        y1, x1 = nodes[node]
        for edge in edges[node]:
            y2, x2 = nodes[edge[0]]
            lines[node][edge[0]] = c.create_line([dx+x1*scaleX,dy-y1*scaleY], [dx+x2*scaleX,dy-y2*scaleY])

def final_path(c, r, list, color):
    for i in range(1, len(list)-1):
        c.itemconfig(lines[list[i-1]][list[i]], fill=color)
        c.itemconfig(lines[list[i]][list[i-1]], fill=color)
        r.update()
    print("Found final path.")
    
def animation():
    root = tk.Tk() #creates the frame
    root.title('Dijkstra')
    canvas = tk.Canvas(root, height=800, width=800, bg='white') #creates a canvas widget, which can be used for drawing lines and shapes
    create_graph(canvas)
    canvas.pack(expand=True) #packing widgets places them on sthe board
    time.sleep(5)
    fin = dijkstra(canvas, root, first, second)
    final_path(canvas, root, fin, "green")
    root.mainloop()
    
    root2 = tk.Tk()
    root2.title('A*')
    canvas2 = tk.Canvas(root2, height=800, width=800, bg='white') #creates a canvas widget, which can be used for drawing lines and shapes
    create_graph(canvas2)
    canvas2.pack(expand=True) #packing widgets places them on sthe board
    fin2 = a_star(canvas2, root2, first, second)
    final_path(canvas2, root2, fin2, "orange")
    root2.mainloop()
    
first = names[sys.argv[1]]
second = names[sys.argv[2]]
animation()
