from graph_tool.all import *
import math
import numpy as np
from operator import add
import copy


#Points should be list; image is a numpy array; source is the index of the "source" point in the image
def initGraph(points, image, source = 0):
    g = Graph() #Attempting directionality
    disp = 600 #Size of display; this is defualt for graph_draw
    dim = image.shape[0] #Currently assumes image is square; will adjust later

    #Set up properties
    #Graph properties
    gpropS = g.new_graph_property("int")
    g.gp.source = gpropS

    g.gp.source = source

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

    #Other useful data containers, not attached as properties
    circleList = dict()

    #Assigning the vertices
    for point in points:
        v = g.add_vertex()
        g.vp.x[v] = point[0]
        g.vp.y[v] = point[1]
        g.vp.r[v] = biggestCircle(point, image)
        g.vp.linDist[v] = distance(points[source], point)

        circleList.update({"({x},{y})".format(x = g.vp.x[v], y = g.vp.y[v]):makeCircle(point, g.vp.r[v], image.shape)})

        #Adjusts the coordinates to fit display size - for debugging
        g.vp.coord[v] = [(x+1)*disp/dim for x in point]
        if g.vp.coord[v][0] == disp: g.vp.coord[v][0] = disp-1
        if g.vp.coord[v][1] == disp: g.vp.coord[v][1] = disp-1

    #Set up edges
    N = g.num_vertices() #Adjust this as needed
    #N = 5
    #Start with a list of vertices you can pop from to only check pairs one at a time
    checkList = list(range(g.num_vertices())) #List to remove from, possibly reduntant but fixes error from earlier.
    for i in range(g.num_vertices()):
        v = g.vertex(i)
        checkList.remove(i)
        near = neighbors(v, g, checkList, N)

        for n in near:
            u = g.vertex(n[1])
            d = n[0]
            if isEdge([g.vp.x[v],g.vp.y[v]], [g.vp.x[u],g.vp.y[u]], image, points, circleList):
                # #Three scenarios for option A of directionality.
                # if g.vp.r[v] > g.vp.r[u]:
                #     e = g.add_edge(v,u)
                #     g.ep.dist[e] = d
                #     g.ep.mid[e] = midpoint([g.vp.x[v],g.vp.y[v]], [g.vp.x[u],g.vp.y[u]])
                # elif g.vp.r[v] < g.vp.r[u]:
                #     e = g.add_edge(u,v)
                #     g.ep.dist[e] = d
                #     g.ep.mid[e] = midpoint([g.vp.x[v],g.vp.y[v]], [g.vp.x[u],g.vp.y[u]])
                # else:
                #     e1 = g.add_edge(u,v)
                #     e2 = g.add_edge(v,u)
                #     g.ep.dist[e1] = d
                #     g.ep.dist[e2] = d
                #     g.ep.mid[e1] = midpoint([g.vp.x[v],g.vp.y[v]], [g.vp.x[u],g.vp.y[u]])
                #     g.ep.mid[e2] = midpoint([g.vp.x[v],g.vp.y[v]], [g.vp.x[u],g.vp.y[u]])
                #Two scenarios for option B of directionality
                if g.vp.linDist[v] < g.vp.linDist[u]:
                    e = g.add_edge(v,u)
                else:
                    e = g.add_edge(u,v)
                g.ep.dist[e] = d
                g.ep.mid[e] = midpoint([g.vp.x[v],g.vp.y[v]], [g.vp.x[u],g.vp.y[u]])


    #Add edge widths
    for e in g.edges():
        g.ep.width[e] = perpWidth(g, e, image)

    return g

#Distance formula; x and y are lists or tuples
def distance(x, y):
    return math.sqrt((x[0] - y[0])**2 + (x[1]- y[1])**2)

#gets the N nearest neighbors around a point center from a list points; returns coordinates of those points
def neighbors(center, g, indices, N):
    d = [(distance([g.vp.x[center], g.vp.y[center]], [g.vp.x[i], g.vp.y[i]]), i) for i in indices]
    d.sort()
    nearest = d[0:N]
    return nearest

#Given an image and two coordinates, checks if edge between them
#
#Inputs
#a, b: coordinate points, lists preferred type
#im: a numpy array of an image.
#points: a list of coordinates of all nodes; will be copied to not change original
#cirDict: a dictionary, where key is coordinate pair from points and value is a list of the largest circle surrounding that point; will be copied to not change original
#thresh: include if there is a grayscale threshold
#
#Process
#
def isEdge(a, b, im, points, cirDict, thresh = 1):
    if a == b: return False

    p = points[:]
    p.remove(a) #Don't include starting point in list to test against

    #Find the point on the circle around start that is closest to the target; reassign that to target
    cir = copy.deepcopy(cirDict)#To protect the other one for what we're about to do to it
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

    #Add the rest of the circle points to p
    for item in cir.values():
        for point in item:
            p.append(point)

    #Create the target zone to check termination
    endzone = fullCircle(b, biggestCircle(b,im), im.shape)

    h = -1 if a[0] > b[0] else 1 #Move left or right
    v = -1 if a[1] > b[1] else 1 #Move up or down
    maxx = im.shape[0]
    maxy = im.shape[1]
    end = a
    stop = 0
    while stop == 0:
        if end[0] != b[0] and end[0] + h < maxx and im[end[1]][end[0] + h] > thresh:
            end[0] += h
            if end in p:
                stop=1
        elif end[1] != b[1] and end[1] + v < maxy and im[end[1] + v][end[0]] > thresh:
            end[1] += v
            if end in p:
                stop=1
        elif end != b and end[0] + h < maxx and end[1] + v < maxy and im[end[1]+v][end[0]+h] > thresh:
            end = list(map(add, end, [h,v]))
            if end in p:
                stop=1
        else:
            stop = 1
    return True if end in endzone else False

#Quick function to invert an image, formatted as a numpy array
#Requires numpy to be imported as np
#Changes the array in place
def invert(imArray):
    for x in np.nditer(imArray, op_flags=["readwrite"]):
        x[...] = (x - 255)*-1

#Functions related to circles around a point

#Identifying points on a circle based on Bresenham's Circle Algorithm
#Inputs
#x0 is a coorinate pair (tuple or list)
#r is an integer
#max matters if corners might be a problem
def makeCircle(x0, r, max=None):
    p = list()
    if r == 0:
        p.append(list(x0))
        return p

    if max is not None:
        x_max = max[0]
        y_max = max[1]

    x = x0[0]
    y = x0[1]
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

#Determine if a circle of a given size can fall entirely above threshold in an image
#Inputs
#r: radius of circle, integer
#x: center of circle (tuple or list)
#im: image array (np.array)
#thresh: cut off point, defaults such that anything above 0 is included
def isCircle(r, x, im, thresh = 1):
    circlePoints = makeCircle(x, r, max = im.shape)
    for point in circlePoints:
        a = point[0]
        b = point[1]
        if im[b][a] < thresh:
            return False
    #Returns true if never returned false
    return True

#Find the biggest possible circle contained in target area around a point in an image. x is a center point (list or tuple); im is a numpy array.
#Potential issue: will never return for solid black image?
def biggestCircle(x, im):
    r = 0
    #Increments R until no longer possible to draw circle, then returns.
    while isCircle(r, x, im):
        r += 1
    else:
        return r

#Generate list of all the coordinates that would fall inside a circle
def fullCircle(x, r, m = None):
    p = list()
    while r >= 0:
        ring = makeCircle(x, r, max = m)
        for point in ring: p.append(point)
        r -= 1
    return p

#Perpendicular width
#Inputs - Edge object of interest, numpy image array
def perpWidth(g, e, im, thresh = 1):
    s = e.source()
    t = e.target()
    d = g.ep.dist[e]
    p1 = list(g.ep.mid[e])
    p2 = list(g.ep.mid[e])

    rise = g.vp.y[t] - g.vp.y[s]
    run = g.vp.x[t] - g.vp.x[s]

    #Perpendicular slope
    slope = -1 * (run/rise)

    print("Edge {index}: start = [{x1},{y1}]; end = [{x2},{y2}]; mid = [{x3},{y3}], slope = {slope}".format(index = g.edge_index[e], x1 = g.vp.x[s], y1 = g.vp.y[s], x2 = g.vp.x[t], y2 = g.vp.y[t], x3 = p1[0], y3 = p1[1], slope = slope))

    counter = 1
    end1 = 0
    end2 = 0

    #Moving along the line, until both ends hit white
    while end1 == 0 or end2 == 0:
        if rise == 0: #Horizontal line
            p1[0] += 1
            p2[0] -= 1
        elif run == 0: #Vertical line
            p1[1] += 1
            p2[1] -= 1
        else:
            #Four possible directions for p1 (p2 goes opposite)
            if 0 < slope < 1:
                lineInc(p1, 0, slope)
                lineInc(p2, 4, slope)
            elif slope >= 1:
                p1 = lineInc(p1, 1, slope)
                p2 = lineInc(p2, 4, slope)
            elif slope <= -1:
                lineInc(p1, 2, slope)
                lineInc(p2, 6, slope)
            elif -1 < slope < 0:
                lineInc(p1, 3, slope)
                lineInc(p2, 7, slope)
        print("({x1},{y1}); ({x2},{y2})".format(x1 = p1[0], y1 = p1[1], y2 = p2[1], x2 = p2[0]))
        #Test the points
        if im[p1[1]][p1[0]] < thresh:
            end1 = 1
        else:
            counter += 1
        if im[p2[1]][p2[0]] < thresh:
            end2 = 1
        else:
            counter += 1

    return counter

#Requires line is not vertical
def lineInc(p, oct, slope):
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

def midpoint(a,b):
    m0 = int((a[0] + b[0])/2)
    m1 = int((a[1] + b[1])/2)
    return [m0,m1]
