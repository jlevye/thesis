#!/usr/bin/python3

#Version of key functions from scripts.py with debugging elements added.

from graph_tool.all import *
import math
import numpy as np
from operator import add
import copy
import itertools
import scripts

def isEdge(a, b, im, points, cirDict, thresh = 1):
    if a == b:
        print("Points are equal.")
        return False
    print("Start: {a}. End: {b}.".format(a = a, b = b))

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
        if scripts.distance(c, b) < minDist:
            minDist = scripts.distance(c,b)
            newpoint = c
    a = newpoint

    print("Start is now {a}".format(a = a))

    #Add the rest of the circle points to p
    for item in cir.values():
        for point in item:
            p.append(point)

    #Create the target zone to check termination
    endzone = scripts.fullCircle(b, scripts.biggestCircle(b,im), im.shape)

    h = -1 if a[0] > b[0] else 1 #Move left or right
    v = -1 if a[1] > b[1] else 1 #Move up or down
    maxx = im.shape[0]
    maxy = im.shape[1]
    end = a
    stop = 0
    step = 0
    while stop == 0:
        print("Step {counter}: testing point {x},{y}".format(counter = step,x= end[0], y = end[1]))

        if end[0] != b[0] and end[0] + h < maxy and im[end[1]][end[0] + h] > thresh:
            end[0] += h
            if end in p:
                stop=1
                print("moved up/down a row and stopped")
        elif end[1] != b[1] and end[1] + v < maxx and im[end[1] + v][end[0]] > thresh:
            end[1] += v
            if end in p:
                stop=1
                print("moved left/right a column and stopped")
        elif end != b and end[0] + h < maxx and end[1] + v < maxy and im[end[1]+v][end[0]+h] > thresh:
            end = list(map(add, end, [h,v]))
            if end in p:
                stop=1
                print("moved diagonal and stopped")
        else:
            stop = 1
            print("did not move; stopped")

        step += 1
    return True if end in endzone else False
