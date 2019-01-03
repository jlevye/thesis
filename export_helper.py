import os, csv
import string
import math
from operator import itemgetter 
from ij import IJ
import ij.gui
from java.awt import Color

#Source and target are lists or tuples
class LineSegment():
    def __init__(self, source, target):
       	self.s = source
        self.t = target
        self.length = 0
        self.width = 1

def distance(a,b):
	d = math.sqrt((a[0] - b[0])**2  + (a[1] - b[1])**2)
	return d
	
#Find the slope of a line defined by two x,y points
def slope(s,t):
	if t[0]-s[0] == 0:
		m = None
	else:
		m = float((t[1]-s[1]))/float((t[0]-s[0]))
	return m

#p is (x,y) coordinate, m is a slope
def intercept(p, m):
	if m is not None:
		b = -1*m*p[0] + p[1]
	else:
		b = None
	return b

#a and b are line segment objects
def intersection(a, b, fuzz=0):

	m1 = slope(a.s, a.t)
	m2 = slope(b.s, b.t)
	b1 = intercept(a.s, m1)
	b2 = intercept(b.s, m2)

	
    #Don't try to divide by 0 if lines are parallel
	if m1 == m2:
		return False
	#Check for vertical lines: 
	elif any([i is None for i in [m1,m2,b1,b2]]):
		if m1 is None:
			x = a.s[0]
			y = m2*x + b2
		elif m2 is None:
			x = b.s[0]
			y = m1*x + b1
	else:    
		x = (b2 - b1)/(m1 - m2)
		y = m1*x + b1

    #Define the bounds, xs and ys for redundancy
	X1s = sorted([a.s[0], a.t[0]])
	X2s = sorted([b.s[0], b.t[0]])

	lowerX1 = X1s[0] - fuzz
	upperX1 = X1s[1] + fuzz
	lowerX2 = X2s[0] - fuzz
	upperX2 = X2s[1] + fuzz

	Y1s = sorted([a.s[1], a.t[1]])
	Y2s = sorted([b.s[1], b.t[1]])

	lowerY1 = Y1s[0] - fuzz
	upperY1 = Y1s[1] + fuzz
	lowerY2 = Y2s[0] - fuzz
	upperY2 = Y2s[1] + fuzz


	if all([lowerX1 <= x <= upperX1,lowerX2 <= x <= upperX2,lowerY1 <= y <= upperY1,lowerY2 <= y <= upperY2]):
		return [x,y]
	else:
		return False

#a is a line, crosses are all the other lines
#Eventually returns a list of line segments correctly indicating breaks
def findSplits(a, crosses, fuzz=0): 
	width = a.width
	ends = [a.s]
	for cross in crosses:
		p = intersection(a, cross, fuzz)
		if p:
			ends.append(p)
	ends.append(a.t)

	
	ends.sort() #Sorts by the first element by default, so sorted by x value
	segments = []
	
	for i in range(len(ends)-1):
		a = ends[i]
		b = ends[i + 1]

		l = distance(a,b)
		if l > 1:
			newLine = LineSegment(a, b)
			newLine.length = l
			newLine.width = width
			segments.append(newLine)
	return segments
	

