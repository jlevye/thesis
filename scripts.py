from graph_tool.all import *
import math
import numpy as np
from operator import add


#Points should be list; image is a numpy array
def initGraph(points, image):
    g = Graph(directed=False) #For now; figure out directionality in future - v. important
    disp = 600 #Size of display; this is defualt for graph_draw
    dim = image.shape[0] #Currently assumes image is square; will adjust later

    #Set up properties
    vpropX = g.new_vertex_property("int")
    vpropY = g.new_vertex_property("int")
    vpropBool = g.new_vertex_property("bool", vals = True)
    vpropCoord = g.new_vertex_property("vector<float>")
    g.vp.x = vpropX
    g.vp.y = vpropY
    g.vp.keep = vpropBool
    g.vp.coord = vpropCoord

    epropFloat = g.new_edge_property("float")
    g.ep.dist = epropFloat

    #Assigning the vertices
    for point in points:
        v = g.add_vertex()
        g.vp.x[v] = point[0]
        g.vp.y[v] = point[1]

        #Adjusts the coordinates to fit display size - for debugging
        g.vp.coord[v] = [(x+1)*disp/dim for x in point]
        if g.vp.coord[v][0] == disp: g.vp.coord[v][0] = disp-1
        if g.vp.coord[v][1] == disp: g.vp.coord[v][1] = disp-1


    #Set up edges
    N = g.num_vertices() #Adjust this as needed
    for v in g.vertices():
        g.vp.keep[v] = False
        g.set_vertex_filter(g.vp.keep)
        near = neighbors(v, g, N)
        #print((int(v), near))
        g.vp.keep[v] = True
        g.set_vertex_filter(None)

        for i in near:
            u = g.vertex(i[1])
            d = i[0]
            if isEdge([g.vp.x[v],g.vp.y[v]], [g.vp.x[u],g.vp.y[u]], image, points):
                e = g.add_edge(v,u)
                g.ep.dist[e] = d
    return g

def distance(x, y):
    return math.sqrt((x[0] - y[0])**2 + (x[1]- y[1])**2)

#gets the N nearest neighbors around a point center from a list points; returns coordinates of those points
def neighbors(center, g, N):
    d = [(distance([g.vp.x[center], g.vp.y[center]], [g.vp.x[v], g.vp.y[v]]), int(v)) for v in g.vertices()]
    d.sort()
    nearest = d[0:N]
    return nearest

#Given an image and two coordinates, checks if edge between them
#Knowing direction to travel, if can find threshold path up to the target
#Note that np arrays are indexed as array[y][x] and bottom > top
def isEdge(a, b, im, points, thresh = 128):
    if a == b: return False
    #print("a = (%d, %d), b = (%d,%d)" % tuple([a[0],a[1] ,b[0],b[1]]))
    p = points[:]
    p.remove(a)
    p.remove(b)
    h = -1 if a[0] > b[0] else 1 #Move left or right
    v = -1 if a[1] > b[1] else 1 #Move up or down
    maxx = im.shape[0]
    maxy = im.shape[1]
    end = a
    stop = 0
    while stop == 0:
        if end[0] != b[0] and end[0] + h < maxx and im[end[1]][end[0] + h] > thresh:
            end[0] += h
            if end in p: stop=1
        elif end[1] != b[1] and end[1] + v < maxy and im[end[1] + v][end[0]] > thresh:
            end[1] += v
            if end in p: stop=1
        elif end != b and end[0] + h < maxx and end[1] + v < maxy and im[end[1]+v][end[0]+h] > thresh:
            end = list(map(add, end, [h,v]))
            if end in p: stop=1
        else:
            stop = 1
        #print(end)
    return True if end == b else False
