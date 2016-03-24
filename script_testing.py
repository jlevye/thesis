#!/usr/bin/python3

#Testing code, for debugging graph generating functions

from graph_tool.all import *
import numpy as np
import math
import os
from PIL import Image
import csv

os.chdir("/home/jen/Documents/School/GradSchool/Thesis/Code")
import scripts
os.chdir("/home/jen/Desktop")
filename = "LescaThreshold.png" #Change for whatever the file is

with open("points.csv","r") as f:
    pointread = csv.reader(f)
    points = list(pointread)

for point in points:
    point[0] = int(point[0])
    point[1] = int(point[1])

im = Image.open(filename).convert("L")
image = np.array(im)
scripts.invert(image)

g = scripts.initGraph(points, image, 45)
g.save("prelim.xml.gz")
graph_draw(g, pos = g.vp.coord, vertex_text = g.vertex_index)
