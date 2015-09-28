#! /usr/bin/env python

# Graph tool example
import sys, os
from pylab import *
from numpy.random import *
seed(42)

from graph_tool.all import *

#Open a new graph (directed)
g = Graph()

#Property maps
v_age = g.new_vertex_property("int")
e_age = g.new_edge_property("int")

#Size
N = 100000

#Start with one vertex
v = g.add_vertex()
v_age[v] = 0 #Sets the age for vertex V at 0

vlist = [v] #Make a list that has just v in it for now

#Build the whole graph
for i in range(1, N):
    v = g.add_vertex()
    v_age[v] = i

    #Finding a target from the list
    i = randint(0, len(vlist))
    target = vlist[i]

    e = g.add_edge(v, target)
    e_age[i] = i #Edge gets assigned the age of the random integer you picked

    vlist.append(target)
    vlist.append(v)

#Random walks through the graph and print out some information
v = g.vertex(randint(0, g.num_vertices()))
while True:
    print("vertex:", v, "in-degree:", v.in_degree(), "outdegree:", v.out_degree(), "age:", v_age[v])
    if v.out_degree() == 0:
        print("We found the main hub!")
        break
    n_list = []
    for w in v.out_neighbours():
        n_list.append(w)
    v = n_list[randint(0, len(n_list))]

#Saving a graph
g.vertex_properties["age"] = v_age
g.edge_properties["age"] = e_age
g.save("price.xml.gz")

#Draw it! First two lines commented b/c already loaded in this file
#g = load_graph("price.xlm.gz")
age = g.vertex_properties["age"]

pos = sfdp_layout(g) #This line is slow
graph_draw(g, pos, output_size = (1366, 768), vertex_color = [1,1,1,0], vertex_fill_color = age, vertex_size = 1, edge_pen_width = 1.2, vcmap = matplotlib.cm.summer, output = "price.png")

#vcmap picks the color maps from matplotlib; there are many and they are pretty, this does blues/greens/yellows
