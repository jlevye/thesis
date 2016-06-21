#!/usr/bin/python3

#Single image processing using graph init functions.

import os
import sys
import graph_tool.all as gt

#Grab the needed script
os.chdir(
"/home/jen/Documents/School/GradSchool/Thesis/Code")
import graph_scripts as gs

os.chdir("/home/jen/Documents/School/GradSchool/Thesis/Images/")
imfile = "Examples/Traces/ToyLinked.png"
pointfile = "Examples/Points/ToyLinked.csv"

image = gs.read_image(imfile)
points = gs.read_points(pointfile)
source = 91

g = gs.init_graph(points, image, source)
g.save("Examples/ToyLinked.xml.gz")
gt.graph_draw(g, pos = g.vp.coord, vertex_text = g.vertex_index, edge_pen_width = g.ep.width)
