#!/usr/bin/python3

import os
import statistics as stats
import graph_tool.all as gt

os.chdir("/home/jen/Documents/School/GradSchool/Thesis/Images/")

g_link = gt.load_graph("Examples/ToyLinked.xml.gz")
g_bran = gt.load_graph("Examples/ToyBranching.xml.gz")

#Misc Stats
link_deg_avg, link_deg_std = gt.vertex_average(g_link, deg="total")
bran_deg_avg, bran_deg_std = gt.vertex_average(g_bran, deg="total")

#Centrality
vp_btwn_link, ep_btwn_link = gt.betweenness(g_link)
link_btwn = [vp_btwn_link[v] for v in g_link.vertices()]
vp_btwn_bran, ep_btwn_bran = gt.betweenness(g_bran)
bran_btwn = [vp_btwn_bran[v] for v in g_bran.vertices()]

link_btwn_avg = stats.mean(link_btwn)
link_btwn_std = stats.stdev(link_btwn)

bran_btwn_avg = stats.mean(bran_btwn)
bran_btwn_std = stats.stdev(bran_btwn)

#Cost and efficiency
link_mst = gt.min_spanning_tree(g_link)
bran_mst = gt.min_spanning_tree(g_bran)
link_shortest = [x for vector in gt.shortest_distance(g_link) for x in vector]
bran_shortest = [x for vector in gt.shortest_distance(g_bran) for x in vector]

g_link.set_edge_filter(link_mst)
g_bran.set_edge_filter(bran_mst)
link_mst_shortest = [x for vector in gt.shortest_distance(g_link) for x in vector]
bran_mst_shortest = [x for vector in gt.shortest_distance(g_bran) for x in vector]

def efficiency(graph):
    all_shortest_paths = gt.shortest_distance(g_link)
    N = graph.num_vertices()
    path_list = [x for vector in all_shortest_paths for x in vector]
    inverse_sum = sum([1/x if x > 0 else x for x in path_list])
    efficiency = 1/(N*(N-1))*inverse_sum
    return efficiency

efficiency_link = efficiency(g_link)
efficiency_bran = efficiency(g_bran)

cost_link = g_link.num_edges(ignore_filter=True)/g_link.num_edges()
cost_bran = g_bran.num_edges(ignore_filter=True)/g_bran.num_edges()

perf_link = stats.mean(link_shortest)/stats.mean(link_mst_shortest)
perf_bran = stats.mean(bran_shortest)/stats.mean(bran_mst_shortest)

#Output
print(" & Linked & Branching")
print("\hline")
print("# vertices & {0} & {1}".format(g_link.num_vertices(ignore_filter=True),g_bran.num_vertices(ignore_filter=True)))
print("# edges & {0} & {1}".format(g_link.num_edges(ignore_filter=True),g_bran.num_edges(ignore_filter=True)))
print("Avg degree (std.) & {0:.2f} ({1:.2f}) & {2:.2f} ({3:.2f})".format(link_deg_avg,link_deg_std,bran_deg_avg,bran_deg_std))
print("Avg. betweenness centrality (std.) & {0:.2f} ({1:.2f}) & {2:.2f} ({3:.2f})".format(link_btwn_avg,link_btwn_std,bran_btwn_avg,bran_btwn_std))
print("Cost & {0:.2f} & {1:.2f}".format(cost_link, cost_bran))
print("Transport performance & {0:.2f} & {1:.2f}".format(perf_link,perf_bran))
print("Efficiency & {0:.2f} & {1:.2f}".format(efficiency_link,efficiency_bran))
