#!/usr/bin/python3

#For efficiency and accuracy testing

#Iterate through graphs with known numbers of edges, etc and determine where the edge detecting script is failing.

import os
import graph_tool.all as gt

os.chdir("/home/jen/Documents/School/GradSchool/Thesis/Code")

import graph_scripts as gs

image_names = ["Benchmark/Traces/Test{}.png".format(i) for i in range(10)]
point_names = ["Benchmark/Points/Test{}.csv".format(i) for i in range(10)]

true_edges = [12, 4, 4, 8, 8, 8, 14, 22, 11, 15]
calc_edges = []
result = []

for i in range(10):
    image = gs.read_image(image_names[i])
    points = gs.read_points(point_names[i])

    g = gs.init_graph(points, image, N = 100, pct = True)
    calc_edges.append(g.num_edges())

    if calc_edges[i] == true_edges[i]:
        print("Test {} passed.".format(i))
    else:
        print("Test {} failed.".format(i))
        #g.save("Benchmark/Test{}.xml.gz".format(i))
        if calc_edges[i] > true_edges[i]:
            print("Generated {} extra edges.".format(calc_edges[i] - true_edges[i]))
        else:
            print("Missed {} edges.".format(true_edges[i] - calc_edges[i]))
