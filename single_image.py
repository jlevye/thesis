#!/usr/bin/python3

#Makes a graph based on user input

import os
import graph_tool.all as gt

#Grab location of where we're running now
cur_dir = os.getcwd()

#Grab the needed script
os.chdir(
"/home/jen/Documents/School/GradSchool/Thesis/Code")
import graph_scripts as gs

#Load in the required files
imfile = input("Image file path:")
try:
    if imfile[0] == "/":
        image = gs.read_image(cur_dir + imfile)
    else:
        image = gs.read_image(cur_dir + "/" + imfile)
except (IOError,FileNotFoundError):
    try:
        image = gs.read_image(imfile)
    except (IOError,FileNotFoundError):
        print("Bad image file name.")
        raise
pointfile = input("Point file path:")
try:
    if pointfile[0] == "/":
        points = gs.read_points(cur_dir + pointfile)
    else:
        points = gs.read_points(cur_dir + "/" + pointfile)
except (IOError,FileNotFoundError):
    try:
        points = gs.read_points(pointfile)
    except (IOError,FileNotFoundError):
        print("Bad image file name.")
        raise

source = input("Source point:")
percent_to_check = input("Percent of neighboring nodes to search for edges:")

g = gs.init_graph(points, image, source, int(percent_to_check), pct = True)
save = input("Save graph (Y/N):")
if save == "Y":
    savepath = input("Save file as ():")
    g.save(savepath)

gt.graph_draw(g, pos = g.vp.coord, vertex_text = g.vertex_index)
