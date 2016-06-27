#!/usr/bin/python3

#Makes a graph based on user input

import os
import graph_tool.all as gt

#Grab the needed script
os.chdir(
"/home/jen/Documents/School/GradSchool/Thesis/Code")
import graph_scripts as gs

imfile = input("Image file path:")
pointfile = input("Point file path:")
image = gs.read_image(imfile)
points = gs.read_points(pointfile)
source = input("Source point:")

g = gs.init_graph(points, image, source)
save = input("Save graph (Y/N):")
if save == "Y":
    savepath = input("Save file as ():")
    g.save(savepath)

gt.graph_draw(g, pos = g.vp.coord, vertex_text = g.vertex_index, edge_pen_width = g.ep.width)
