#!/usr/bin/python3

import os
import statistics as stats
import graph_tool.all as gt

os.chdir("/home/jen/Documents/School/GradSchool")

g_mel = gt.load_graph("MelastomeSketch.xml.gz")
g_gin = gt.load_graph("GinkgoSketch.xml.gz")

#Misc Stats
mel_deg_avg, mel_deg_std = gt.vertex_average(g_mel, deg="total")
gin_deg_avg, gin_deg_std = gt.vertex_average(g_gin, deg="total")

#Centrality
vp_btwn_mel, ep_btwn_mel = gt.betweenness(g_mel)
mel_btwn = [vp_btwn_mel[v] for v in g_mel.vertices()]
vp_btwn_gin, ep_btwn_gin = gt.betweenness(g_gin)
gin_btwn = [vp_btwn_gin[v] for v in g_gin.vertices()]

mel_btwn_avg = stats.mean(mel_btwn)
mel_btwn_std = stats.stdev(mel_btwn)

gin_btwn_avg = stats.mean(gin_btwn)
gin_btwn_std = stats.stdev(gin_btwn)

#Cost and efficiency
mel_mst = gt.min_spanning_tree(g_mel)
gin_mst = gt.min_spanning_tree(g_gin)
mel_shortest = [x for vector in gt.shortest_distance(g_mel) for x in vector]
gin_shortest = [x for vector in gt.shortest_distance(g_gin) for x in vector]

g_mel.set_edge_filter(mel_mst)
g_gin.set_edge_filter(gin_mst)
mel_mst_shortest = [x for vector in gt.shortest_distance(g_mel) for x in vector]
gin_mst_shortest = [x for vector in gt.shortest_distance(g_gin) for x in vector]

def efficiency(graph):
    all_shortest_paths = gt.shortest_distance(g_mel)
    N = graph.num_vertices()
    path_list = [x for vector in all_shortest_paths for x in vector]
    inverse_sum = sum([1/x if x > 0 else x for x in path_list])
    efficiency = 1/(N*(N-1))*inverse_sum
    return efficiency

efficiency_mel = efficiency(g_mel)
efficiency_gin = efficiency(g_gin)

cost_mel = g_mel.num_edges(ignore_filter=True)/g_mel.num_edges()
cost_gin = g_gin.num_edges(ignore_filter=True)/g_gin.num_edges()

perf_mel = stats.mean(mel_shortest)/stats.mean(mel_mst_shortest)
perf_gin = stats.mean(gin_shortest)/stats.mean(gin_mst_shortest)

#Output
print(" & Melastome & Ginkgo \\\\")
print("\hline")
print("No. vertices & {0} & {1} \\\\".format(g_mel.num_vertices(ignore_filter=True),g_gin.num_vertices(ignore_filter=True)))
print("No edges & {0} & {1} \\\\".format(g_mel.num_edges(ignore_filter=True),g_gin.num_edges(ignore_filter=True)))
print("Avg degree (std.) & {0:.2f} ({1:.2f}) & {2:.2f} ({3:.2f}) \\\\".format(mel_deg_avg,mel_deg_std,gin_deg_avg,gin_deg_std))
print("Avg. betweenness centrality (std.) & {0:.2f} ({1:.2f}) & {2:.2f} ({3:.2f}) \\\\".format(mel_btwn_avg,mel_btwn_std,gin_btwn_avg,gin_btwn_std))
print("Cost & {0:.2f} & {1:.2f} \\\\".format(cost_mel, cost_gin))
print("Transport performance & {0:.2f} & {1:.2f} \\\\".format(perf_mel,perf_gin))
print("Efficiency & {0:.2f} & {1:.2f} \\\\".format(efficiency_mel,efficiency_gin))
