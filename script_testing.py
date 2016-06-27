#!/usr/bin/python3

#Testing code, for debugging graph generating functions

import csv
import os
import graph_tool.all as gt
import numpy as np
from PIL import Image
import timeit

os.chdir("/home/jen/Documents/School/GradSchool/Thesis/Code")
import graph_scripts as gs
import edge_test2 as e

#Testing Variables

if __name__ == "__main__":
    imname = "Testing/LescaThresholdCrop.png"
    pointsname = "Testing/LescaPointsCrop.csv"
    source = 32

    image = gs.read_image(imname)
    points = gs.read_points(pointsname)

    #First few steps of init_graph function
    disp = 600
    dim = [image.shape[1], image.shape[0]]
    g = gt.Graph()

    gs.gen_graph_props(g)
    gs.add_all_vertices(g, points, image, dim, disp)

    circleList = gs.make_all_circles(g, image)

    #Some timing and validation tests
    start = timeit.default_timer()
    edgePairs1 = gs.edge_tester(points, image, circleList)
    elapsed = timeit.default_timer()-start
    print("Edge checking v1:")
    print("Time = {}".format(elapsed))
    print("Found {} edges.\n".format(len(edgePairs1)))

    # start = timeit.default_timer()
    # edgePairs2 = e.edge_tester2(points, image, circleList, 50, pct = True)
    # elapsed = timeit.default_timer()-start
    # print("Edge checking v2:")
    # print("Time = {}".format(elapsed))
    # print("Found {} edges.\n".format(len(edgePairs2)))

    gs.edges_from_list(edgePairs1, g, points)

    #Try edge widths
    start = timeit.default_timer()
    for e in g.edges():
        g.ep.width[e] = gs.perp_width(g, e, image)
    elapsed = timeit.default_timer() - start
    print("Width calc time: {}".format(elapsed))

    # g.save("lescacrop.xml.gz")
    gt.graph_draw(g, pos = g.vp.coord, vertex_text = g.vertex_index, edge_pen_width = g.ep.width)
