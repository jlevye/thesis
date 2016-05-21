#!/usr/bin/python3

import csv
import numpy as np
from operator import add
import copy
import graph_tool.all as gt
import scripts

def read_points(filename):
    with open(filename,"r") as f:
        pointread = csv.reader(f)
        points = list(pointread)

    for point in points:
        point[0] = int(point[0])
        point[1] = int(point[1])
    return points

def edge_tester(points, image, circle):
    edges = []
    error_count = 0
    point_pairs = len(points)*len(points) - len(points)
    for start in points:
        for end in points:
            if start == end:
                continue
            else:
                try:
                    val = isEdge_clean(start, end, image, points, circle)
                except IndexError:
                    print("Start = {}; End = {}".format(start, end))
                    print("Hit an out-of-bound index.")
                    error_count += 1
                    continue
                except:
                    print("Start = {}; End = {}".format(start, end))
                    print("Hit some other error.")
                    error_count += 1
                    continue
                else:
                    if val:
                        edges.append([points.index(start), points.index(end)])
    print("Hit errors in {} of {} possible edges.".format(error_count, point_pairs))
    return edges

def edges_from_list(edges, graph, points):
    for pair in edges:
        s = graph.vertex(pair[0])
        t = graph.vertex(pair[1])
        d = scripts.distance(points[int(s)], points[int(t)])
        if graph.vp.linDist[s] < graph.vp.linDist[t]:
            s = graph.vertex(pair[1])
            t = graph.vertex(pair[0])
        if graph.edge(s,t) == None:
            e = graph.add_edge(s,t)
            graph.ep.dist[e] = d
            graph.ep.mid[e] = scripts.midpoint([graph.vp.x[s], graph.vp.y[s]], [graph.vp.x[t], graph.vp.y[t]])

#Working version!
def isEdge(a, b, im, points, cirDict, thresh=1):
    if a == b:
        return False
    p = points[:]
    p.remove(a)

    height = im.shape[0] - 1
    width = im.shape[1] - 1

    cir = copy.deepcopy(cirDict)
    keyA = "({x},{y})".format(x = a[0], y = a[1])
    circle = cir[keyA]
    del cir[keyA]

    newpoint = a
    minDist = 999999
    for c in circle:
       if scripts.distance(c, b) < minDist:
           minDist = scripts.distance(c,b)
           newpoint = c
    a = newpoint

    for item in cir.values():
        for point in item:
            if point[0] > width: point[0] = width
            if point[1] > height: point[1] = height
            p.append(point)


    endzone = scripts.fullCircle(b, scripts.biggestCircle(b,im), im.shape)

    h = -1 if a[0] > b[0] else 1 #Move left or right
    v = -1 if a[1] > b[1] else 1 #Move up or down

    end = a
    stop = 0

    while stop == 0:
        #Have we hit b? Have we hit an edge?
        if end[0] == b[0] or end[0] == width: h = 0
        if end[1] == b[1] or end[1] == height: v = 0
        if [h,v] == [0,0]:
            stop = 1

        testX = end[0] + h
        testY = end[1] + v

        #Test the possible directions we can move.
        if h is not 0 and im[end[1]][testX] > thresh:
            end[0] = testX
            if end in p: stop=1
        elif v is not 0 and im[testY][end[0]] > thresh:
            end[1] = testY
            if end in p: stop=1
        elif im[testY][testX] > thresh:
            end = [testX,testY]
            if end in p: stop=1
        else:
            stop = 1
        step +=1
    return True if end in endzone else False

#The following functions pull out some of the key parts of init graph, to save typing later.
def genGraphProps(g):
    #Graph properties
    gpropS = g.new_graph_property("int")
    g.gp.source = gpropS

    #Vertex properties
    vpropX = g.new_vertex_property("int") #x position
    vpropY = g.new_vertex_property("int") #y positon
    vpropR = g.new_vertex_property("int") #radius of largest circle that fit
    vpropBool = g.new_vertex_property("bool", vals = True) #Currently unused
    vpropCoord = g.new_vertex_property("vector<float>") #Coordinates for plotting
    vpropLinDist = g.new_vertex_property("float")
    g.vp.x = vpropX
    g.vp.y = vpropY
    g.vp.r = vpropR
    g.vp.keep = vpropBool
    g.vp.coord = vpropCoord
    g.vp.linDist = vpropLinDist

    #Edge properties
    epropFloat = g.new_edge_property("float")
    epropDiam = g.new_edge_property("int")
    epropMid = g.new_edge_property("vector<int>")
    epropWidth = g.new_edge_property("int")
    g.ep.dist = epropFloat
    g.ep.d = epropDiam
    g.ep.mid = epropMid
    g.ep.width = epropWidth

def addAllVertices(g, points, image, dim, disp):
    for point in points:
        v = g.add_vertex()
        g.vp.x[v] = point[0]
        g.vp.y[v] = point[1]
        g.vp.r[v] = scripts.biggestCircle(point, image)
        g.vp.linDist[v] = scripts.distance(points[g.gp.source], point)

        g.vp.coord[v] = [(x+1)*disp/y for x,y in zip(point,dim)]
        if g.vp.coord[v][0] == disp: g.vp.coord[v][0] = disp-1
        if g.vp.coord[v][1] == disp: g.vp.coord[v][1] = disp-1

def genCircle(g, image):
    circleList = dict()
    for v in g.vertices():
        x = g.vp.x[v]
        y = g.vp.y[v]
        key = "({x},{y})".format(x = x, y = y)
        value = scripts.makeCircle([x,y], g.vp.r[v], image.shape)

        circleList[key] = value
    return circleList
