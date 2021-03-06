#Setting up parameters

#@int(label="Segment length cut-off",value=0) min_length 
#@int(label="Intersection threshold",value=1) thresh 

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
    m = float((t[1]-s[1]))/float((t[0]-s[0]))
    return m

#p is (x,y) coordinate, m is a slope
def intercept(p, m):
    b = -1*m*p[0] + p[1]
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
	else:    
		x = (b2 - b1)/(m1 - m2)
		y = m1*x + b1

    #Define the bounds
	Xs = sorted([a.s[0], a.t[0], b.s[0], b.t[0]])
	Ys = sorted([a.s[1], a.t[1], b.s[1], b.t[1]])

	lowerX = Xs[1] - fuzz
	upperX = Xs[2] + fuzz
	lowerY = Ys[1] - fuzz
	upperY = Ys[2] + fuzz

	if lowerX <= x <= upperX and lowerY <= y <= upperY:
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
	
#Main method
imp = IJ.getImage()
overlay = imp.getOverlay()
rangeEnd = overlay.size()

lines = []

for index in range(rangeEnd):
	roi = overlay.get(index)
	if roi.isLine():
		s = [roi.x1, roi.y1]
		t = [roi.x2, roi.y2]
		length = roi.getLength()
		width = roi.getStrokeWidth()
		newLine = LineSegment(s,t)
		newLine.length = length
		newLine.width = width
		lines.append(newLine)
		m = slope(s, t)
		b = intercept(s, m)

#Sanity check
print len(lines)
fullSegments = []

for line in lines:
	crosses = [l for l in lines if l is not line]
	newSegments = findSplits(line, crosses, thresh)
	for seg in newSegments:
		if seg.length > min_length:
			fullSegments.append(seg)

print len(fullSegments)

newLayer = ij.gui.Overlay()

for line in fullSegments:
	toDraw = ij.gui.Line(line.s[0],line.s[1],line.t[0],line.t[1])
	toDraw.setStrokeWidth(line.width)
	toDraw.setStrokeColor(Color(0,255,0))
	newLayer.add(toDraw)

imp.setOverlay(newLayer)
newLayer.setLabelColor(Color(0,0,0))
newLayer.drawLabels(True)
imp.updateImage()

