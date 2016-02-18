from graph_tool.all import *
import math
import numpy as np
from operator import add


#Points should be list; image is a numpy array
def initGraph(points, image):
    #g = Graph(directed=False) #For now; figure out directionality in future - v. important
    g = Graph() #Attempting directionality
    disp = 600 #Size of display; this is defualt for graph_draw
    dim = image.shape[0] #Currently assumes image is square; will adjust later

    #For debugging
    f = open("log.txt","w")

    #Set up properties
    vpropX = g.new_vertex_property("int") #x position
    vpropY = g.new_vertex_property("int") #y positon
    vpropR = g.new_vertex_property("int") #radius of largest circle that fit
    vpropBool = g.new_vertex_property("bool", vals = True) #Currently unused
    vpropCoord = g.new_vertex_property("vector<float>") #Coordinates for plotting
    g.vp.x = vpropX
    g.vp.y = vpropY
    g.vp.r = vpropR
    g.vp.keep = vpropBool
    g.vp.coord = vpropCoord

    epropFloat = g.new_edge_property("float")
    g.ep.dist = epropFloat

    #Other useful data containers, not attached as properties
    circleList = dict()

    #Assigning the vertices
    for point in points:
        v = g.add_vertex()
        g.vp.x[v] = point[0]
        g.vp.y[v] = point[1]
        g.vp.r[v] = biggestCircle(point, image)

        f.write("Vertex {v} at ({x},{y}); r = {r}\n".format(v = int(v), x = g.vp.x[v], y = g.vp.y[v], r = g.vp.r[v]))

        circleList.update({"({x},{y})".format(x = g.vp.x[v], y = g.vp.y[v]):makeCircle(point, g.vp.r[v], image.shape)})

        #Adjusts the coordinates to fit display size - for debugging
        g.vp.coord[v] = [(x+1)*disp/dim for x in point]
        if g.vp.coord[v][0] == disp: g.vp.coord[v][0] = disp-1
        if g.vp.coord[v][1] == disp: g.vp.coord[v][1] = disp-1

    #Set up edges
    N = g.num_vertices() #Adjust this as needed
    #N = 5
    #Start with a list of vertices you can pop from to only check pairs one at a time
    checkList = list(range(g.num_vertices())) #Duplicate for debugging purposes
    for i in range(g.num_vertices()):
        v = g.vertex(i)
        checkList.remove(i)
        near = neighbors(v, g, checkList, N)

        for n in near:
            u = g.vertex(n[1])
            d = n[0]
            if isEdge([g.vp.x[v],g.vp.y[v]], [g.vp.x[u],g.vp.y[u]], image, points, circleList):
                if g.vp.r[v] > g.vp.r[u]:
                    e = g.add_edge(v,u)
                    g.ep.dist[e] = d
                elif g.vp.r[v] < g.vp.r[u]:
                    e = g.add_edge(u,v)
                    g.ep.dist[e] = d
                else:
                    e = g.add_edge(u,v)
                    f = g.add_edge(v,u)
                    g.ep.dist[e] = d
                    g.ep.dist[f] = d

    return g, circleList

def distance(x, y):
    return math.sqrt((x[0] - y[0])**2 + (x[1]- y[1])**2)

#gets the N nearest neighbors around a point center from a list points; returns coordinates of those points
def neighbors(center, g, indices, N):
    #vertexList = find_vertex(g, g.vp.vertex_index in indices)
    d = [(distance([g.vp.x[center], g.vp.y[center]], [g.vp.x[i], g.vp.y[i]]), i) for i in indices]
    d.sort()
    nearest = d[0:N]
    return nearest

#Given an image and two coordinates, checks if edge between them
#Knowing direction to travel, if can find threshold path up to the target
#Note that np arrays are indexed as array[y][x] and bottom > top
#cir is a dictionary that matches a coordinate pair to the largest circle that surrounds it - to find the closest point around the center to the target point (ideally to solve problem of thick lines)
def isEdge(a, b, im, points, cirDict, thresh = 1):
    if a == b: return False
    #print("a = (%d, %d), b = (%d,%d)" % tuple([a[0],a[1] ,b[0],b[1]]))
    p = points[:]
    p.remove(a)
    #p.remove(b)

    cir = cirDict.copy() #To protect the other one for what we're about to do to it
    #Find the point on the circle around start that is closest to the target; reassign that to target
    keyA = "({x},{y})".format(x = a[0], y = a[1])
    keyB = "({x},{y})".format(x = b[0], y = b[1])
    circle = cir[keyA]

    endzone = fullCircle(b, biggestCircle(b,im), im.shape)

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

    h = -1 if a[0] > b[0] else 1 #Move left or right
    v = -1 if a[1] > b[1] else 1 #Move up or down
    maxx = im.shape[0]
    maxy = im.shape[1]
    end = a
    stop = 0
    while stop == 0:
        print("Current X = {x0}. Current Y = {y0}\n".format(x0 = end[0], y0 = end[1]))
        print("Target is ({x},{y})\n".format(x = b[0], y = b[1]))
        print("Value is {a}".format(a = im[end[1]][end[0]]))
        if end[0] != b[0] and end[0] + h < maxx and im[end[1]][end[0] + h] > thresh:
            end[0] += h
            if end in p:
                stop=1
                print("Moved horizontal by one; hide another point.")
        elif end[1] != b[1] and end[1] + v < maxy and im[end[1] + v][end[0]] > thresh:
            end[1] += v
            if end in p:
                stop=1
                print("Moved vertical by one, hit another point.")
        elif end != b and end[0] + h < maxx and end[1] + v < maxy and im[end[1]+v][end[0]+h] > thresh:
            end = list(map(add, end, [h,v]))
            if end in p:
                stop=1
                print("Moved diagonal, hit another point.")
        else:
            print("No conditions met?")
            stop = 1
        print(end)
    return True if end in endzone else False

#Quick function to invert an image, formatted as a numpy array
#Requires numpy to be imported as np
#Changes the array in place
def invert(imArray):
    for x in np.nditer(imArray, op_flags=["readwrite"]):
        x[...] = (x - 255)*-1

#Functions to identify area around a center point (attempting to identify diameter, for example)
#Identifying points on a circle based on Bresenham's Circle Algorithm; x0 is a pair of points (tuple or list), r is an integer,
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
    decisionOver2 = 1 - r

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

#Given a radius (integer), a midpoint (tuple or list), and an image array (np.array) see if all the points are under the threshold; currently hardcoded as 127
def isCircle(r, x, im):
    circlePoints = makeCircle(x, r, max = im.shape)
    for point in circlePoints:
        a = point[0]
        b = point[1]
        if im[b][a] == 0: #Currently hardcoding threshold for purely binary image - fix later!
            return False
    return True

#Uses the image and a point to find the radius of the biggest circle
def biggestCircle(x, im):
    r = 0
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
