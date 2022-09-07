from heapq import heappush, heappop, heapify
from collections import deque
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

with open("./north_america_boundaries.txt","r") as f:
    line_list = [line.strip() for line in f]    
    nodes2 = []
    temp = []
    for i, line in enumerate(line_list): 
        tempLine = line.split()
        if len(tempLine) != 0: temp.append([float(tempLine[0]), float(tempLine[1])])
        else:
            if len(temp)!=0:
                nodes2.append(temp)
                temp = []
    
root = tk.Tk() #creates the frame
root.title('Train Routes Black')

frm = tk.Frame(root)
frm.pack()
    
city_1 = tk.StringVar()
lbl_c1 = tk.Label(frm, text='CITY #1: ').pack(side=tk.LEFT)
ent_c1 = tk.Entry(frm, width=10, textvariable=city_1).pack(side=tk.LEFT)

city_2 = tk.StringVar()
lbl_c2 = tk.Label(frm, text='CITY #2: ').pack(side=tk.LEFT)
ent_c2 = tk.Entry(frm, width=10, textvariable=city_2).pack(side=tk.LEFT)

canvas = tk.Canvas(root, height=800, width=800, bg='white') #creates a canvas widget, which can be used for drawing lines and shapes

curr_spd = tk.DoubleVar()
lbl_scale = tk.Label(frm, text='SPEED: ').pack(side=tk.LEFT)
scale_interval = tk.Scale(frm, from_=0, to=1000, orient=tk.HORIZONTAL, width=6, length=250, variable=curr_spd).pack(side=tk.LEFT, pady=5)
visited = []

def dijkstra(canvas, r, start, goal):
    interval = curr_spd.get()
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
                    canvas.itemconfig(lines[v[1]][c[0]], fill="blue")
                    canvas.itemconfig(lines[c[0]][v[1]], fill="blue")
                else:
                    canvas.itemconfig(lines[v[1]][c[0]], fill="orange")
                    canvas.itemconfig(lines[c[0]][v[1]], fill="orange")
                visited.append([c[0], v[1]])
                visited.append([v[1], c[0]])
                if times%interval==0:
                    r.update()
    return None

def a_star(canvas, r, start, goal):
    interval = curr_spd.get()
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
                else:
                    canvas.itemconfig(lines[v[2]][c[0]], fill="orange")
                    canvas.itemconfig(lines[c[0]][v[2]], fill="orange")
                visited.append([c[0], v[2]])
                visited.append([v[2], c[0]])
                if times%interval==0:
                    r.update()
    return None

def DFS(canvas, r, start, goal):
    interval = curr_spd.get()
    fringe = deque([[start, [start]]])
    visited2 = set([start])
    times = 0
    while len(fringe)!=0:
        v = fringe.pop()
        times += 1
        if v[0]==goal:
            return v[1]
        for c in edges[v[0]]:
            if c[0] not in visited2:
                visited2.add(c[0])
                fringe.append([c[0], v[1] + [c[0]]])
                canvas.itemconfig(lines[v[0]][c[0]], fill="blue")
                canvas.itemconfig(lines[c[0]][v[0]], fill="blue")
            else:
                canvas.itemconfig(lines[v[0]][c[0]], fill="orange")
                canvas.itemconfig(lines[c[0]][v[0]], fill="orange")
            visited.append([c[0], v[0]])
            visited.append([v[0], c[0]])    
            if times%interval==0:
                r.update()
    return None

lines = {node : {} for node in edges} #list of all the lines created
def create_graph(c):
    scaleX = 11
    scaleY= 15
    dx = 1450
    dy = 895
    for node in edges:
        y1, x1 = nodes[node]
        for edge in edges[node]:
            y2, x2 = nodes[edge[0]]
            lines[node][edge[0]] = c.create_line([dx+x1*scaleX,dy-y1*scaleY], [dx+x2*scaleX,dy-y2*scaleY])

def create_map(c):
    scaleX = 11
    scaleY= 14.4
    dx = 1450
    dy = 875
    for node in nodes2:
        for i in range(1,len(node)):
            y1, x1 = node[i-1]
            y2, x2 = node[i]
            c.create_line([dx+x1*scaleX,dy-y1*scaleY], [dx+x2*scaleX,dy-y2*scaleY], fill='green')

def final_path(c, r, list, color):
    for i in range(1, len(list)-1):
        c.itemconfig(lines[list[i-1]][list[i]], fill=color)
        c.itemconfig(lines[list[i]][list[i-1]], fill=color)
        r.update()
    print("Found final path.")
    
def run_a_star():
    fin = a_star(canvas, root, names[city_1.get()], names[city_2.get()])
    final_path(canvas, root, fin, "red")

def run_dijkstra():
    fin = dijkstra(canvas, root, names[city_1.get()], names[city_2.get()])
    final_path(canvas, root, fin, "red")

def run_dfs():
    fin = DFS(canvas, root, names[city_1.get()], names[city_2.get()])
    final_path(canvas, root, fin, "red")

def reset():
    if len(visited)!=0:
        for i in visited:
            canvas.itemconfig(lines[i[0]][i[1]], fill='black')
            canvas.itemconfig(lines[i[1]][i[0]], fill='black')
        root.update()
        visited.clear()
    city_1.set("")
    city_2.set("")
    
btn_1 = tk.Button(frm, text='A*',command=run_a_star).pack(side=tk.LEFT, padx=10)
btn_2 = tk.Button(frm, text='DIJKSTRA',command=run_dijkstra).pack(side=tk.LEFT)
btn_3 = tk.Button(frm, text='DFS',command=run_dfs).pack(side=tk.LEFT, padx=10)

btn_reset = tk.Button(frm, text='RESET', command=reset).pack(side=tk.LEFT, padx=10)

create_graph(canvas)
create_map(canvas)
canvas.pack(expand=True) #packing widgets places them on sthe board

root.mainloop()
