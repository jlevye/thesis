# coding: utf-8
p = [0,0]
import os
os.chdir("Documents/School/GradSchool/Thesis/Code
os.chdir("Documents/School/GradSchool/Thesis/Code")
import graph_scripts as gs
image = gs.read_image("Testing/testgraph.png")
image
points = gs.read_points("Testing/testgraph.csv")
import imp
imp.reload(gs)
points = gs.read_points("Testing/testgraph.csv")
imp.reload(gs)
points = gs.read_points("Testing/testgraph.csv")
import helper as h
points = h.read_points("Testing/testgraph.csv")
p = h.read_points("Testing/testgraph.csv")
imp.reload(h)
p = h.read_points("Testing/testgraph.csv")
p
points = p
p = [0,0]
s = points[0]
start = [s.x, s.y]
start
p
rules = [image[p[1]][p[0]] == 0, p in exclude, p == pred]
exclude = []
pred = None
rules = [image[p[1]][p[0]] == 0, p in exclude, p == pred]
ring = gs.dedup(gs.make_circle(start, 1))
ring
for p in ring:
    if any(rules): ring.remove(p)
    
ring
for p in ring:
    if p in [pixel for point in points for pixel in point.circle]:
        print([point.index for point in points if p in point.circle])
        exclude.append(p)
        
exclude
exclude.append(p)
exclude
ring.remove(start)
start
p
imp.reload(gs)
terminii = []
exclude = []
gs.step_forward(terminii, start, exclude, image, points)
ring
p
start
exclude.append(start)
pred = start
start = [42,0]
ring0 = ring
ring0
ring1 = gs.dedup(gs.make_circle(start,1))
ring1
for p in ring:
    if any(rules): ring.remove(p)
    
ring
for p in ring1:
    if any(rules): ring1.remove(p)
    
    
ring1
ring0
p
start
imp.reload(gs)
imp.reload(gs)
gs.step_forward(terminii, start, exclude, image, points)
imp.reload(gs)
gs.step_forward(terminii, start, exclude, image, points)
imp.reload(gs)
gs.step_forward(terminii, start, exclude, image, points)
exclude
p
p = [42,0]
p in exclude
exclude = []
imp.reload(gs)
gs.step_forward(terminii, start, exclude, image, points)
exclude
exclude = []
start
exclude.append(start)
exclude
p = [0,0]
rules
ring = gs.dedup(gs.make_circle(start,1))
ring
for p in ring:
    if any(rules):
        ring.remove(p)
        
ring
exclude
start
start in exclude
for p in rihg:
    if any(rules):
        ring.remove(p)
        
for p in ring:
    if any(rules):
        ring.remove(p)
        
ring
for p in ring:
    if any(rules):
        ring.remove(p)
        
ring
exclude
pred
ring = gs.dedup(gs.make_circle(start,1))
ring
for p in ring:
    print(any(rules))
    
for p in ring:
    print(rules))
for p in ring:
    print(rules)
    
exclude
ring
for p in ring:
    if p in exclude or image[p[1]][p[0]]==0:
            ring.remove(p)
        
ring
exclude
for p in ring:
    if p in exclude: ring.remove(p)
    
ring
image[1][41]
image[1][42]
imp.reload(gs)
exclude = []
gs.step_forward(terminii, start, exclude, image, points)
imp.reload(gs)
exclude = []
gs.step_forward(terminii, start, exclude, image, points)
image.shape
xmax = 50
ymax = 50
start
ring = gs.dedup(gs.make_circle(start,1))
ring
keep = []
exclude
exclude = []
exclude.append(start)
for p in ring:
        if all(p[0] < xmax, p[1] < ymax, p not in exclude, image[p[1]][p[0]] > 0):
            keep.append(p) 
        
for p in ring:
        if all([p[0] < xmax, p[1] < ymax, p not in exclude, image[p[1]][p[0]] > 0]):
            keep.append(p) 
            
        
keep
imp.reload(gs)
exclude = []
step_forward(terminii, start, exclude, image, points)
gs.step_forward(terminii, start, exclude, image, points)
imp.reload(gs)
gs.step_forward(terminii, start, exclude, image, points)
terminii
exclude
imp.reload(gs)
exclude = []
exclude
gs.step_forward(terminii, start, exclude, image, points)
exclude = []
imp.reload(gs)
gs.step_forward(terminii, start, exclude, image, points)
points[0].circle
points[1].circle
for p in points:
    p.r = gs.biggest_circle([p.x,p.y],image)
    p.circle = gs.full_circle([p.x,p.y],p.r, image.shape)
    
points[0].circle
points[1].circle
for p in points:
    p.r = gs.biggest_circle([p.x,p.y],image)
    p.circle = gs.full_circle([p.x,p.y],p.r+1, image.shape)
    
    
points[0].circle
exclude = []
terminii
gs.step_forward(terminii, start, exclude, image, points)
imp.reload(gs)
gs.step_forward(terminii, start, exclude, image, points)
terminii
terminii[0]
terminii[0][0]
point[0].index
points[0].index
points[0].i
imp.reload(gs)
imp.reload(h)
filename
points = h.read_points("Testing/testgraph.csv")
points[0].i
gs.step_forward(terminii, start, exclude, image, points)
terminii
gs.nodes_and_edges(images, points)
gs.nodes_and_edges(image, points)
imp.reload(gs)
gs.nodes_and_edges(image, points)
terminii
terminii = []
exclude = []
start
gs.step_forward(terminii, start, exclude, image, points)
terminii
tiny_xy = [[5,8],[5,5],[8,2],[2,2]]
tiny_image = h.read_image("Testing/smallest.png")
tiny_image
tiny_image[5][5]
tiny_points = [Point(tiny_xy.index(p), p[0],p[1]) for p in tiny_xy]
tiny_points = [h.Point(tiny_xy.index(p), p[0],p[1]) for p in tiny_xy]
tiny_points
tiny_points[0].i
gs.nodes_and_edges(tiny_image, tiny_points)
start = [5,8]
exclude = []
terminii = []
gs.step_foward(terminii, start, exclude, tiny_image, tiny_points)
gs.step_forward(terminii, start, exclude, tiny_image, tiny_points)
terminii
other = [point for point in tiny_points if point is not start]
other
gs.step_forward(terminii, start, exclude, tiny_image, other)
new_ring = gs.dedup(gs.make_circie(start,1))
new_ring = gs.dedup(gs.make_circle(start,1))
new_ring
keep = []
exclude = [start]
for p in ring:
    if all(p[0] < xmax, p[1] < ymax, p not in exclude, image[p[1][p[0]]>0]):
        keep.append(p)
        
o
p
ring
new_ring
start
exclude
for p in new_ring:
    if all([p[0] < xmax, p[1] < ymax, p not in exclude, image[p[1]][p[0]] > 0]):
        keep.append(p)
        
keep
xmax
ymax
tiny_image
tiny_image[8][4]
tiny_image[7][5]
p = [5,7]
all([p[0] < xmax, p[1] < ymax, p not in exclude, image[p[1]][p[0]] > 0])
p[0] < xmax
p[1] < ymax
p not in exclude
for p in new_ring:
    if all([p[0] < xmax, p[1] < ymax, p not in exclude, tiny_image[p[1]][p[0]] > 0]):
        keep.append(p)
        
        
keep
other
for point in other:
    print(point.x,point.y)
    
start.x
start
tiny_points
other = [point for point in tiny_points if point.x is not start[0] and point.y is not start[1]]
other
other = [point for point in tiny_points if [point.x,point.y] is not start]
other
start
for point in tiny_points
for point in tiny_points:
    [point.x,point.y] is start
    
for point in tiny_points:
    print([point.x,point.y] is start)
    
    
for point in tiny_points:
    print([point.x,point.y] == start)
    
    
    
other = [point for point in tiny_points if [point.x,point.y] != start]
other
exclude = []
gs.step_forward(terminii, start, exclude, tiny_image, other)
terminii
imp.reload(gs)
imp.reload(gs)
gs.step_forward(terminii, start, exclude, tiny_image, other)
gs.nodes_and_edges(tiny_image, tiny_points)
imp.reload(gs)
gs.nodes_and_edges(tiny_image, tiny_points)
imp.reload(gs)
gs.nodes_and_edges(tiny_image, tiny_points)
gs.nodes_and_edges(image, points)
imp.reload(gs)
imp.reload(gs)
imp.reload(gs)
imp.reload(gs)
edges = gs.nodes_and_edges(tiny_points, tiny_image)
edges = gs.nodes_and_edges(tiny_image, tiny_points)
g = gs.init_graph(tiny_points, edges)
imp.reload(gs)
g = gs.init_graph(tiny_points, edges)
g = gs.init_graph(tiny_points, edges, tiny_image)
edges
import graph_tool.all as gt
g = gt.Graph(directed = False)
dim = [50,50]
disp = [600,600]
gs.gen_graph_props(g)
gs.points_to_vertices(g, points, dim, disp)
v = g.vertices[0]
v = g.vertices(0)
for pair in edges: 
    v = g.vertex(pair[0])
    u = g.vertex(pair[1])
    e = g.add_edge(u,v)
    
g
gt.graph_draw(g)
imp.reload(gs)
edges = gs.nodes_and_edges(image, points)
g = gs.init_graph(points, edges, image)
g
gt.graph_draw(g, pos = g.vp.coord, vertex_text = g.vertex_index)
image_lesca = gs.read_image("Testing/LescaThreshold.png")
points_lesca = gs.read_points("Testing/LescaPoints.csv")
edges_lesca = gs.nodes_and_edges(image_lesca, points_lesca)
lesca_image.size
image_lesca.shape
import sys
sys.setrecursionlimit(10000)
edges_lesca = gs.nodes_and_edges(image_lesca, points_lesca)
imp.reload(gs)
sys.setrecursionlimit(1000)
edges_lesca = gs.nodes_and_edges(image_lesca, points_lesca)
11 % 10
10 % 10 
0 % 10
1.1 % 10
11 / 100
print("1%")
print("1\%")
imp.reload(gs)
edges_lesca = gs.nodes_and_edges(image_lesca, points_lesca)
points_link = gs.read_points("Testing/ToyLinked.csv")
image_link = gs.read_image("Testing/ToyLinked.png")
edges_link = gs.nodes_and_edges(image_link, points_link)
points_spoke = gs.read_points("Testing/Spoke2px.csv")
image_spoke = gs.read_image("Testing/Spoke2px.png")
len(points_spoke)
image_spoke.shape
edges_spoke = gs.nodes_and_edges(image_spoke, points_spoke)
edges
edges_spoke
image_spoke1 = gs.read_image("Testing/Spoke1px.png")
point_spoke1 = gs.read_points("Testing/Spoke1px.png")
point_spoke1 = gs.read_points("Testing/Spoke1px.csv")
edges_spoke1 = gs.nodes_and_edges(image_spoke1, point_spoke1)
edges_spoke1
g_spoke1 = gs.init_graph(point_spoke1, eges_spoke1, image_spoke1)
g_spoke1 = gs.init_graph(point_spoke1, edges_spoke1, image_spoke1)
gt.graph_draw(g_spoke1, pos = g_spoke1.vp.coord, vertex_text = g_spoke1.vertex_index)
g_spoke2 = gs.init_graph(points_spoke, edges_spoke, image_spoke)
gt.graph_draw(g_spoke, pos = g_spoke.vp.coord, vertex_text = g_spoke.vertex_index)
gt.graph_draw(g_spoke2, pos = g_spoke2.vp.coord, vertex_text = g_spoke2.vertex_index)
points_spoke5 = gs.read_points("Testing/Spoke5px.csv")
image_spoke5 = gs.read_image("Testing/Spoke5px.png")
edges_spoke5 = gs.nodes_and_edges(image_spoke5, points_spoke5)
edges_spoke5
new_test_list = [[8,1],[5,5], [2,2], [5,8]]
test_points = [gs.Point(new_test_list.index(p), p[0],p[1]) for p in new_test_list]
test_points
test_image = gs.read_image("Testing/Tiny2px.png")
test_edges = gs.nodes_and_edges(test_image, test_points)
range(10)
[i for i in range(10)]
[[i,j] for i in range(10) for j in range(10)]
white = [[x,y] for x in range(10) for y in range(10) if test_image[y][x] == 0]
white
imp.reload(gs)
imp.reload(gs)
imp.reload(gs)
test_edges = gs.nodes_and_edges(test_image, test_points)
imp.reload(gs)
test_edges = gs.nodes_and_edges(test_image, test_points)
edges
test_edges
imp.reload(gs)
imp.reload(gs)
test_edges = gs.nodes_and_edges(test_image, test_points)
test_edges
test0_points = gs.read_points("Benchmark/Points/Test0.csv")
test0_image = gs.read_image("Benchmark/Traces/Test0.csv")
test0_image = gs.read_image("Benchmark/Traces/Test0.png")
test0_edges = gs.nodes_and_edges(test0_image, test0_points)
g0 = gs.init_graph(test0_points, test0_edges, test0_image)
gt.graph_draw(g0, pos = g0.vp.coord)
os.chdir("Benchmark")
p1 = gs.read_points("Points/Test1.png")
p1 = gs.read_points("Points/Test1.csv")
i1 = gs.read_image("Trace/Test1.png")
i1 = gs.read_image("Traces/Test1.png")
e1 = gs.nodes_and_edges(i1, p1)
g1 = gs.init_graph(p1, e1, i1)
def draw(g):
    gt.graph_draw(g, pos = g.vp.coord, vertex_text = g.vertex_index)
    
draw(g1)
def test_file(filename):
    i = gs.read_image("Traces/{}.png".format(filename))
    p = gs.read_points("Points/{}.csv".format(filename))
    e = gs.nodes_and_edges(i, p)
    g = gs.init_graph(p, e, i)
    draw(g)
    
test_file("Test2")
test_file("Test3")
test_file("Test4")
test_file("Test5")
test_file("Test6")
test_file("Test7")
test_file("Test8")
test_file("Test9")
test_file("Test0")
test_file("Test3")
test_file("Test4")
test_file("Test4")
with open("Points/Test4.csv","r") as f:
    pointread = csv.reader(f)
    for row in pointread:
        print(row)
        
import csv
with open("Points/Test4.csv","r") as f:
    pointread = csv.reader(f)
    for row in pointread:
        print(row)
        
with open("Points/Test4.csv","r") as f:
    pointread = csv.reader(f)
    for row in pointread:
        print([int(float(row[x])), int(float(row[y]))])
        
        
with open("Points/Test4.csv","r") as f:
    pointread = csv.reader(f)
    for row in pointread:
        print([int(float(row[0])), int(float(row[1]))])
        
        
        
imp.reload(gs)
get_ipython().magic('cd ..')
imp.reload(gs)
get_ipython().magic('cd "Benchmark"')
test_file("Test1")
test_file("Test0")
test_file("Test4")
test_file("Test5")
get_ipython().magic('cd ..')
imp.reload(gs)
get_ipython().magic('cd "Benchmark/')
get_ipython().magic('cd "Benchmark/"')
test_file("Test0")
test_file("Test1")
test_file("Test2")
test_file("Test3")
test_file("Test4")
test_file("Test5")
test_file("Test6")
test_file("Test7")
test_file("Test8")
test_file("Test9")
[2,1].sort()
[2,1].sort
sort([2,1])
test = []
test.append([2,1].sort())
test
test.append([2,1].sort)
test
e = [2,1]
e.sort()
e
e = [2,1].sort()
e
e
get_ipython().magic('cd ..')
imp.reload(gs)
get_ipython().magic('cd Benchmark')
test_file("Test0")
test_file("Test1")
test_file("Test2")
test_file("Test3")
test_file("Test4")
test_file("Test5")
test_file("Test6")
test_file("Test8")
test_file("Test7")
test_file("Test9")
get_ipython().magic('cd ../Testing')
test_file("Spoke1px")
test_file("Spoke2px")
test_file("Spoke5px")
test_file("testgraph")
test_file("ToyBranching")
sort_test = [[[1,2,3],[2]],[[2,4,5],[1]]]
sort_test
sorted(sort_test, key=lambda x: x[1])
sorted(sort_test, key=lambda x: x[1], reverse=True)
get_ipython().magic('cd ..')
imp.reload(gs)
imp.reload(gs)
get_ipython().magic('cd Benchmark')
test_file("Test0")
test_file("Test1")
h.distance([1,2],[2,1])
get_ipython().magic('cd ..')
imp.reload(gs)
get_ipython().magic('cd Benchmark')
test_file("Test0")
test_file("Test1")
test_file("Test2")
test_file("Test3")
test_file("Test4")
test_file("Test5")
test_file("Test6")
test_file("Test7")
test_file("Test8")
test_file("Test9")
get_ipython().magic('cd ../Testing')
test_file("Spoke1px")
test_file("Spoke2px")
test_file("Spoke5px")
get_ipython().magic('cd ../../Images/Examples')
test_file("ToyLinked2")
get_ipython().magic('cd ../../Code')
imp.reload(gs)
get_ipython().magic('cd ../Images/Examples')
test_file("ToyLinked2")
list.files()
get_ipython().magic('ls ')
get_ipython().magic('cd Traces')
get_ipython().magic('ls ')
get_ipython().magic('cd ../../Code/Testing')
get_ipython().magic('ls ')
get_ipython().magic('cd ../..')
get_ipython().magic('ls ')
get_ipython().magic('cd ..')
get_ipython().magic('cd Code/Testing')
get_ipython().magic('ls ')
import pandas as pd
edgesDF = pd.read_csv("LinkTraceOverlay.csv")
edgesDF.head()
edgesDF = pd.read_csv("LinkTraceOverlay.csv")
edgesDF.head()
import numpy as np
edgesDF['case'] = np.where(edgesDF['Angle'] >= 90 or (edgesDF['Angle']> -90 and edgesDF['Angle'] <= 0), 1,2)
edgesDF['case'] = np.where(any([edgesDF['Angle'] >= 90, all([edgesDF['Angle']> -90, edgesDF['Angle'] <= 0])]), 1,2)
edgesDF['case'] = np.where(any([edgesDF['Angle'] >= 90, -90<edgesDF['Angle']<0]), 1,2)
x = 5
2 < x < 7
2 < x < 4
edgesDF['case'] = np.where(edgesDF['Angle'] >= 90 or -90<edgesDF['Angle']<0, 1,2)
edgesDF['case'] = np.where(edgesDF['Angle'] >= 90 | -90<edgesDF['Angle']<0, 1,2)
edgesDF['case'] = np.where(np.any([edgesDF['Angle'] >= 90, -90<edgesDF['Angle']<0]), 1,2)
edgesDF['case'] = np.where(np.logical_or(edgesDF['Angle'] >= 90, np.logical_and(np.greater(edgesDF['Angle'],-90),np.less(edgesDF['Angle'],0))), 1,2)
edgesDF.head()
edgesDF['x1'] = edgesDF['BX']
edgesDF['y1'] = np.where(edgesDF['case']==1, edgesDF['BY'],edgesDF['BY'] + edgesDF['Height'])
edgesDF['y2'] = np.where(edgesDF['case']==2, edgesDF['BY'],edgesDF['BY'] + edgesDF['Height'])
edgesDF['x2'] = edgesDF['BX'] + edgesDF['Width']
edgesDF.head()
class Edge():
    def __init__(self, index,df):
        self.index = index
        self.source = [df['x1'],df['y1']]
        self.target = [df['x2'],df['y2']]
        
class Edge():
    def __init__(self, index,df):
        self.index = index
        self.source = [df.x1[index],df.y1[index]]
        self.target = [df.x2[index],df.y2[index]]
        
edges = [Edge(i, edgesDF) for i in range(len(edgesDF))]
edges[0].source
min(edgeDF.Length)
min(edgesDF.Length)
