#Script for testing fault tolerance metrics

#Load packages
import pandas as pd
import numpy as np
from random import shuffle
import csv
import sys
import math
import os
import graph_tool.all as gt
import statistics as stats

#definitions
def efficiency(graph):
    all_shortest_paths = gt.shortest_distance(graph)
    N = graph.num_vertices()
    path_list = [x for vector in all_shortest_paths for x in vector]
    inverse_sum = sum([1/x if x > 0 else x for x in path_list])
    try:
        efficiency = 1/(N*(N-1))*inverse_sum
    except ZeroDivisionError:
        efficiency = np.nan
    return efficiency

def cost_calc(graph):
    orig_filter = graph.get_edge_filter()
    n_orig = graph.num_edges()
    mst = gt.min_spanning_tree(graph)
    graph.set_edge_filter(mst)
    try:
        c = n_orig/graph.num_edges()
    except ZeroDivisionError:
        c = np.nan
    g.set_edge_filter(orig_filter[0])
    return c

def performance(graph):
    orig_filter = graph.get_edge_filter()

    mst = gt.min_spanning_tree(graph)
    g_shortest = [x for vector in gt.shortest_distance(graph) for x in vector]
    graph.set_edge_filter(mst)
    g_mst_shortest = [x for vector in gt.shortest_distance(graph) for x in vector]

    try:
        p = stats.mean(g_shortest)/stats.mean(g_mst_shortest)
    except ZeroDivisionError:
        p = np.nan
        
    graph.set_edge_filter(orig_filter[0])
    return p

def component_size(graph):
    map = gt.label_largest_component(graph)
    return sum(map.a[:])


#Set up a bunch of lists to store data
n_removed = []
largest = []
cost = []
perf = []
eff = []

#Generate random graph
g, pos = gt.triangulation(np.random.random((500, 2)) * 4, type="delaunay")
g.ep.weight = g.new_edge_property("float")
g.ep.btwn = g.new_edge_property("float")
g.ep.filter = g.new_edge_property("bool")
g.vp.btwn = g.new_vertex_property("float")


#Assign edge weights and calculate some stuff
for e in g.edges():
    g.ep.weight[e] = np.random.randint(0,5) + np.random.random()
    g.ep.filter[e] = 1
vp, ep = gt.betweenness(g, vprop = g.vp.btwn, eprop = g.ep.btwn, weight = g.ep.weight)

#Get initial values
n_removed.append(0)
largest.append(component_size(g))
cost.append(cost_calc(g))
perf.append(performance(g))
eff.append(efficiency(g))

#Random filtering
index = list(range(g.ep.filter.get_array().size - 1))
shuffle(index)
counter = 1
for i in index:
    g.ep.filter.get_array()[i,] = 0
    g.set_edge_filter(g.ep.filter)

    #Calculate some new stuff
    n_removed.append(counter)
    largest.append(component_size(g))
    cost.append(cost_calc(g))
    perf.append(performance(g))
    eff.append(efficiency(g))
    counter += 1


#Store data and stuff
d = {"Removed" : n_removed, "LargestConnected" : largest, "Cost": cost, "Performance" : perf, "Efficiency" : eff}
data_random = pd.DataFrame(d)

#Filter based on weight; resetting storage vectors
#reset edge filter
g.ep.filter.get_array()[:] = 1

#Set up a bunch of lists to store data
n_removed = []
largest = []
cost = []
perf = []
eff = []

n_removed.append(0)
largest.append(component_size(g))
cost.append(cost_calc(g))
perf.append(performance(g))
eff.append(efficiency(g))


weight_index = list(np.argsort(g.ep.weight.get_array()))
counter = 1
for i in weight_index:
    g.ep.filter.get_array()[i,] = 0
    g.set_edge_filter(g.ep.filter)

    #Calculate some new stuff
    n_removed.append(counter)
    largest.append(component_size(g))
    cost.append(cost_calc(g))
    perf.append(performance(g))
    eff.append(efficiency(g))
    counter += 1

d = {"Removed" : n_removed, "LargestConnected" : largest, "Cost": cost, "Performance" : perf, "Efficiency" : eff}
data_weight = pd.DataFrame(d)

#Filter based on centrality
#reset edge filter
g.ep.filter.get_array()[:] = 1

#Set up a bunch of lists to store data
n_removed = []
largest = []
cost = []
perf = []
eff = []

n_removed.append(0)
largest.append(component_size(g))
cost.append(cost_calc(g))
perf.append(performance(g))
eff.append(efficiency(g))


btwn_index = list(np.argsort(g.ep.btwn.get_array()))
counter = 1
for i in btwn_index:
    g.ep.filter.get_array()[i,] = 0
    g.set_edge_filter(g.ep.filter)

    #Calculate some new stuff
    n_removed.append(counter)
    largest.append(component_size(g))
    cost.append(cost_calc(g))
    perf.append(performance(g))
    eff.append(efficiency(g))
    counter += 1

d = {"Removed" : n_removed, "LargestConnected" : largest, "Cost": cost, "Performance" : perf, "Efficiency" : eff}
data_btwn = pd.DataFrame(d)
