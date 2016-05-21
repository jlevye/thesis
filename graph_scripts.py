#!/usr/bin/python3
"""Functions for generating a graph from images and points.

Points are drawn from a two-column csv in (x,y) pairs.
The image is a binary trace of a leaf, with veins as straight-line segments.
"""

#Modules required
import math
import csv
from operator import add
import copy

import numpy as np
import graph_tool.all as gt
from PIL import Image

#Utility/shorthand functions
def read_points(filename):
    """Read and convert to integers the points in a csv."""

    #TODO: handle if a file has headers.
    with open(filename,"r") as f:
        pointread = csv.reader(f)
        points = list(pointread)

    for point in points:
        point[0] = int(point[0])
        point[1] = int(point[1])
    return points

def read_image(filename):
    """Read an image into a numpy array, inverted for processing."""

    im = Image.open(filename).convert("L")
    image = np.array(im)
    invert(image)
    return image

def invert(imArray):
    """Invert a numpy array of a black and white image."""

    for x in np.nditer(imArray, op_flags=["readwrite"]):
        x[...] = (x - 255)*-1

#Graph functions
def init_graph(points, image, source=0):
    """Primary function: generates a graph object from the inputs."""

    #Initialize directed graph.
    g = gt.Graph()

    #Set some parameters.
    disp = 600 #px, a default square window size for graph_tool
    dim = [image.shape[1], image.shape[0]] #[width,height]

    #Initialize graph properties
    gen_graph_props(g)
    add_all_vertices(g, points, image, dim, disp)
    print("Vertices set.")

    circleList = make_all_circles(g, image)

    #Set up the edges
    edgePairs = edge_tester(points, image, circleList)
    edges_from_list(edgePairs, g, points)
    print("Edges set.")

    #Try edge widths
    for e in g.edges():
        percent = math.floor(g.edge_index[e]/g.num_edges()*100)
        if percent % 10 == 0:
            print("Processed {}%  possible starting edges.".format(percent))
        g.ep.width[e] = perp_width(g, e, image)

    print("Done!")
    return g

def gen_graph_props(graph):
    """Creates a set of internal property maps for a graph_tool graph."""

    g = graph

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

def add_all_vertices(graph, points, image, dim, disp):
    """Adds vertices and sets a number of their properties."""

    g = graph
    for point in points:
        v = g.add_vertex()
        g.vp.x[v] = point[0]
        g.vp.y[v] = point[1]
        g.vp.r[v] = biggest_circle(point, image)
        g.vp.linDist[v] = distance(points[g.gp.source], point)

        g.vp.coord[v] = [(x+1)*disp/y for x,y in zip(point,dim)]
        if g.vp.coord[v][0] == disp: g.vp.coord[v][0] = disp-1
        if g.vp.coord[v][1] == disp: g.vp.coord[v][1] = disp-1

#Edge-related scripts
def is_edge(a, b, im, points, cirDict, thresh=1):
    """Determines of an edge connects two points. Glitches on curves."""

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
       if distance(c, b) < minDist:
           minDist = distance(c,b)
           newpoint = c
    a = newpoint

    for item in cir.values():
        for point in item:
            if point[0] > width: point[0] = width
            if point[1] > height: point[1] = height
            p.append(point)


    endzone = full_circle(b, biggest_circle(b,im), im.shape)

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
    return True if end in endzone else False

#TODO: Improve speed of this process!
def edge_tester(points, image, circle):
    """Given a list of points, checks the possible edges between them. Slow!"""

    edges = []
    for start in points:
        for end in points:
            if start == end:
                continue
            else:
                try:
                    val = is_edge(start, end, image, points, circle)
                except IndexError:
                    print("Start = {}; End = {}".format(start, end))
                    print("Hit an out-of-bound index.")
                    continue
                except Exception as e:
                    print("Start = {}; End = {}".format(start, end))
                    print("Hit some other error: {}.".format(e))
                    continue
                else:
                    if val:
                        edges.append([points.index(start), points.index(end)])
    return edges

def edges_from_list(edges, graph, points):
    """Given a list of edges, sets direction and adds to graph."""

    for pair in edges:
        s = graph.vertex(pair[0])
        t = graph.vertex(pair[1])
        d = distance(points[int(s)], points[int(t)])
        if graph.vp.linDist[s] < graph.vp.linDist[t]:
            s = graph.vertex(pair[1])
            t = graph.vertex(pair[0])
        if graph.edge(s,t) == None:
            e = graph.add_edge(s,t)
            graph.ep.dist[e] = d
            graph.ep.mid[e] = midpoint([graph.vp.x[s], graph.vp.y[s]], [graph.vp.x[t], graph.vp.y[t]])

#Circle-related functions
def make_circle(center, radius, max=None):
    """Bresenham's circle algorithm to produce a circle of a given radius."""

    p = list()
    if radius == 0:
        p.append(list(center))
        return p

    if max is not None:
        x_max = max[0]
        y_max = max[1]

    x = center[0]
    y = center[1]
    r = radius
    i = 0
    decisionOver2 = 1 - r #Start for decision criteria for algorithm

    #Computes points
    while i < r:
        p.append([r + x,  i + y]) #Octant 1
        p.append([i + x,  r + y]) #Octant 2
        p.append([-r + x, i + y]) #Octant 3
        p.append([-i + x, r + y]) #Octant 4
        p.append([-r + x, -i + y]) #Octant 5
        p.append([-i + x, -r + y]) #Octant 6
        p.append([r + x, -i + y]) #Octant 7
        p.append([i + x, -r + y]) #Octant 8
        i += 1
        if decisionOver2 <= 0:
            decisionOver2 += 2*i+1
        else:
            r -= 1
            decisionOver2 += 2 *(i - r)+1

    #If this is being used in a bounded image, makes sure the circle is cut off at the corners.
    if max is not None:
        for point in p:
            if point[0] >= y_max:
                point[0] = y_max - 1
            if point[1] >= x_max:
                point[1] = x_max - 1

    return p

def is_circle(radius, center, image, thresh=1):
    """Checks if a circle fits inside black pixels on an image."""

    circlePoints = make_circle(center, radius, image.shape)

    for point in circlePoints:
        x = point[0]
        y = point[1]
        if image[y][x] < thresh:
            return False

    #Returns true if never returned false
    return True

def biggest_circle(center, image):
    """Returns radius of largest circle around center that fits in image."""

    r = 0
    #Increments R until no longer possible to draw circle, then returns.
    while is_circle(r, center, image):
        r += 1
    else:
        return r

def make_all_circles(graph, image):
    """Makes a dictionary of circles around points."""

    g = graph
    circleList = dict()
    for v in g.vertices():
        x = g.vp.x[v]
        y = g.vp.y[v]
        key = "({x},{y})".format(x = x, y = y)
        value = make_circle([x,y], g.vp.r[v], image.shape)
        circleList[key] = value
    return circleList

def full_circle(center, radius, bound=None):
    """Produces all the points inside a given circle."""
    r = radius
    p = list()
    while r >= 0:
        ring = make_circle(center, radius, bound)
        for point in ring: p.append(point)
        r -= 1
    return p

#Functions about lines
def distance(start, end):
    """Euclidian distance formula between two coordinate points."""

    return math.sqrt((start[0] - end[0])**2 + (start[1]- end[1])**2)

def midpoint(start, end):
    """Midpoint between two coordinate points."""

    mid_x = int((start[0] + end[0])/2)
    mid_y = int((start[1] + end[1])/2)
    return [mid_x, mid_y]

def perp_width(graph, edge, image, thresh=1):
    """Measures the width across an edge, perpendicular to that edge."""

    s = edge.source()
    t = edge.target()
    d = graph.ep.dist[edge]
    p1 = list(graph.ep.mid[edge])
    p2 = list(graph.ep.mid[edge])

    rise = graph.vp.y[t] - graph.vp.y[s]
    run = graph.vp.x[t] - graph.vp.x[s]

    #Perpendicular slope
    if rise != 0: slope = -1 * (run/rise)

    counter = 1
    end1 = 0
    end2 = 0
    #Moving along the line, until both ends hit white
    while end1 == 0 or end2 == 0:
        if rise == 0: #Horizontal line, increment vertically
            p1[1] += 1
            p2[1] -= 1
        elif run == 0: #Vertical line, increment horizontally
            p1[0] += 1
            p2[0] -= 1
        else:
            #Four possible directions for p1 (p2 goes opposite)
            if 0 < slope < 1:
                line_inc(p1, 0, slope)
                line_inc(p2, 4, slope)

            elif slope >= 1:
                p1 = line_inc(p1, 1, slope)
                p2 = line_inc(p2, 5, slope)
            elif slope <= -1:
                line_inc(p1, 2, slope)
                line_inc(p2, 6, slope)
            elif -1 < slope < 0:
                line_inc(p1, 3, slope)
                line_inc(p2, 7, slope)

        #Set of conditions that need to be true.
        p1MaxEdge = p1[0] >= image.shape[1]-1 or p1[1] >= image.shape[0]-1
        p1MinEdge = p1[0] <= 0 or p1[1] <= 0
        p2MaxEdge = p2[0] >= image.shape[1]-1 or p2[1] >= image.shape[0]-1
        p2MinEdge = p2[0] <= 0 or p2[1] <= 0

        #Test p1
        if end1 == 0:
            if p1MaxEdge or p1MinEdge:
                end1 = 1
            elif image[p1[1]][p1[0]] < thresh:
                end1 = 1
            else:
                counter += 1
        #Test p2
        if end2 == 0:
            if p2MaxEdge or p2MinEdge:
                end2 = 1
            elif image[p2[1]][p2[0]] < thresh:
                end2 = 1
            else:
                counter += 1

        if counter > min(image.shape):
            counter = math.nan
            break
    return counter

def line_inc(p, oct, slope):
    """Increments a line in the correct direction, given a slope and octant."""

    slope = abs(slope)
    if oct in [0,3,4,7]:
        if oct in [0,7]:
            p[0] += 1
            if oct == 0:
                p[1] = round(p[1] + slope)
            else:
                p[1] = round(p[1] - slope)
        else:
            p[0] -= 1
            if oct == 3:
                p[1] = round(p[1] + slope)
            else:
                p[1] = round(p[1] - slope)
    else:
        if oct in [1,2]:
            p[1] += 1
            if oct == 1:
                p[0] = round(p[0] + slope)
            else:
                p[0] = round(p[0] - slope)
        else:
            p[1] -= 1
            if oct == 1:
                p[0] = round(p[0] + slope)
            else:
                p[0] = round(p[0] - slope)
    return p