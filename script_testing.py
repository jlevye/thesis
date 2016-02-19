#!/usr/bin/python3

#Testing code, for debugging graph generating functions

from graph_tool.all import *
import numpy as np
import math
import os
from PIL import Image


os.chdir("/home/jen/Documents/School/GradSchool/Thesis/Code/")
import scripts
filename = "wobblytest.png" #Change for whatever the file is

im = Image.open(filename).convert("L")
image = np.array(im)
scripts.invert(image)
points = [[26,176],[51,157],[107,104],[32,54],[101,7],[119,70],[150,38],[192,91]]
g = scripts.initGraph(points, image)
g.save("debuggraph.xml.gz")
graph_draw(g, pos = g.vp.coord, vertex_text = g.vertex_index, vertex_size = 3, edge_pen_width = g.ep.width)
