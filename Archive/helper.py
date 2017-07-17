#!/usr/bin/python3
"""Utility functions for use in graph_scripts.py

See that file for additional information.
"""

#Modules required
import math
import csv
from operator import add
import copy

import numpy as np
import graph_tool.all as gt
from PIL import Image

#Class Definitions
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class VertexError(Error):
    def __init__(self, message):
        self.message = message

class Point:
    def __init__(self, index, x, y):
        self.i = index
        self.x = x
        self.y = y
        self.r = 0 #Will be set separately
        self.circle = [] #Will be list of points, requires self.r
        self.d = 0 #Attribute for distance

    def distance(self, other):
        if isinstance(other, Point):
            return  math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

#File I/O and processing
def read_points(filename):
    """From a list of coordinates, produce a list of point objects."""

    pointValues = []
    with open(filename, "r") as f:
        headTF = csv.Sniffer().has_header(f.read(1024))
        #If it's not within the first KB of data, it's probably not there:
        if headTF:
            with open(filename, "r") as f:
                pointread = csv.reader(f)
                header = next(pointread)
                for s in header: lower(s)

                try:
                    x = header.index("x")
                    y = header.index("y")
                    for row in pointread():
                        pointValues.append([int(float(row[x])), int(float(row[y]))])
                except ValueError:
                    print("Double check column names")
        else:
            with open(filename, "r") as f:
                pointread = csv.reader(f)
                for row in pointread:
                    if len(row) is 2:
                        values = [int(float(i)) for i in row]
                        pointValues.append(values)
                    else:
                        print("There is an extra or missing column in this row:\n")
                        print(row)
    points = [Point(pointValues.index(p), p[0],p[1]) for p in pointValues]
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

def dedup(items):
    """Deduplicates a list of anything."""
    new_list = []
    for item in items:
        if item not in new_list:
            new_list.append(item)
    return new_list

def overlap(intersection, image):
    for p in intersection:
        if image[p[1]][p[0]] > 0:
            return True
        else:
            return False

#Circle functions
def make_circle(center, radius, max=None):
    """Bresenham's circle algorithm to produce a circle of a given radius, with special cases r = 0 and r = 1."""

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
    #special case
    if r == 1:
        p.append([x - r, y - r])
        p.append([x, y - r])
        p.append([x + r, y - r])
        p.append([x - r, y])
        p.append([x + r, y])
        p.append([x - r, y + r])
        p.append([x, y + r])
        p.append([x + r, y + r])
    #Computes points
    else:
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
    for point in p:
        if point[0] < 0:
            point[0] = 0
        if point[1] < 0:
            point[1] = 0
        if max is not None:
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

    r = -1
    #Increments R until no longer possible to draw circle, then returns.
    while is_circle(r + 1, center, image):
        r += 1
    else:
        if r == -1:
            raise VertexError("Misplaced vertex at {}".format(center))
        else:
            return r

def full_circle(center, radius, bound=None):
    """Produces all the points inside a given circle."""
    r = radius
    p = list()
    while r >= 0:
        ring = make_circle(center, r, bound)
        for point in ring: p.append(point)
        r -= 1
    return p

#Line functions
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

def octant(source, target):
    """Given two points, source and target, identifies the octant of a vector going from source to target. Returns nothing for horizontal or vertical lines, which require a special case."""

    rise = target[1] - source[1]
    run = target[0] - source[0]

    #Vertical line:
    if rise == 0 or run == 0:
        return
    else:
        if rise > 0:
            if run > 0:
                if abs(rise/run) < 1:
                    return 0
                elif abs(rise/run) >= 1:
                    return 1
            elif run < 0:
                if abs(rise/run) >= 1:
                    return 2
                elif abs(rise/run) < 1:
                    return 3
        elif rise < 0:
            if run > 0:
                if abs(rise/run) < 1:
                    return 4
                elif abs(rise/run) >= 1:
                    return 5
            elif run < 0:
                if abs(rise/run) >= 1:
                    return 6
                elif abs(rise/run) < 1:
                    return 7
