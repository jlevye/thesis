#!/usr/bin/python3

#Testing code, for debugging graph generating functions

import csv
import os
import graph_tool.all as gt
import numpy as np
from PIL import Image

os.chdir("/home/jen/Documents/School/GradSchool/Thesis/Code")
import graph_scripts

#Testing Variables

if __name__ == "__main__":
    imname = "Testing/LescaThresholdCrop.png"
    pointsname = "Testing/LescaPointsCrop.csv"
    source = 32

    image = graph_scripts.read_image(imname)
    points = graph_scripts.read_points(pointsname)

    g = graph_scripts.init_graph(points, image, source)
    g.save("lescacrop.xml.gz")
    gt.graph_draw(g, pos = g.vp.coord, vertex_text = g.vertex_index, edge_pen_width = g.ep.width)
