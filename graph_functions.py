#!/usr/bin/python3
"""
Only the methods of Roi_to_graph, designed for use with GUI
"""
#Module import
import pandas as pd
import numpy as np
import scipy
import csv
import sys
import math
import os
import graph_tool.all as gt
import tkinter as tk
import statistics as stats
from random import shuffle
from tkinter import filedialog, messagebox

#Class definitions
class Edge():
    def __init__(self, id1, id2):
        self.id1 = id1
        self.id2 = id2
        self.length = 0 #Will be updated either from data or calculation
        self.width = 1 #As default; will be taken from data if given

class Point():
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.alias = id
        self.keep = True
        self.graph_index = None

##Function definitions
#Math and stuff
def vertex_distance_object(u, v):
    if not isinstance(u, Point) or not isinstance(v, Point):
        print("Needs point objects. Use another distance function if only using coordinates.")
        return

    dist = math.sqrt((u.x - v.x)**2 + (u.y - v.y)**2)
    return dist

#File I/O
def get_csv_files():
    open_directory = PARAMS["InFile"].value
    file_names = [open_directory + "/" + file for file in os.listdir(open_directory) if file.endswith(("CSV","csv"))]

    #Also set the save location: creates a folder called "Graph" in the parent of the CSV folder.
    parent = os.path.dirname(open_directory)
    os.chdir(parent)

    try:
        os.mkdir("Graph")
        os.chdir("Graph")
    except FileExistsError:
        os.chdir("Graph")

    return file_names

def check_csv(file_path):
    data = pd.read_csv(file_path)
    names = list(data)

    #Option one
    option1 = ["X","Y","Angle","Width","Height","LineWidth","Length"]
    #Option two
    option2 = ["x1","x2","y1","y2","Width","Length"]

    if all([name in names for name in option1]):
        data = boundbox_to_xy(data[option1])
        return data
    elif all([name in names for name in option2]):
        data = data[option2]
        data['id1'] = [i for i in range(len(data))]
        data['id2'] = [i for i in range(len(data), 2*len(data))]
        return data
    else:
        print("Please use data exported using ImageJDataExport.py")
        return

#If using output from measurements rather than straight xy endpoints
def boundbox_to_xy(df):
    #Note, edits df in place!

    df['case'] = np.where(np.logical_or(df['Angle'] >= 90, np.logical_and(np.greater(df['Angle'],-90),np.less(df['Angle'],0))), 1,2)

    df['x1'] = df['X']
    df['x2'] = df['X'] + df['Width']
    df['y1'] = np.where(df['case']==1, df['Y'],df['Y'] + df['Height'])
    df['y2'] = np.where(df['case']==2, df['Y'],df['Y'] + df['Height'])

    #make preliminary/initial IDs
    df['id1'] = [i for i in range(len(df))]
    df['id2'] = [i for i in range(len(df), 2*len(df))]

    #Drop extra columns
    to_drop = ["X","Y","Height","Width","Angle"]
    df.drop(to_drop, axis = 1, inplace = True)

    return df

#TODO
#Calculating approximate edge resistance - multiple options
def edge_resist(Diam, l, d = 0, n = 1, type = "const_n",alpha = 0.6, p = 1):
    area = (math.pi*(Diam/2)**2)*p

    #Correctly calculate d (hydralically weighted mean diameter)
    if type == "const_n": #How big can n circles be inside size Diam*p?
        small_area = area/n
        d = 2*math.sqrt(small_area/math.pi)
    elif type == "const_d": #How many circles of size d it inside Diam*p?
        small_area = math.pi*(d/2)**2
        n = floor(area/small_area)
    elif type == "taper": #How many circles of Diam^alpha fit in Diam*p?
        d = Diam**alpha
        small_area = math.pi*(d/2)**2
        n = floor(area/small_area)
    else:
        print("Incorrect mode.")
        return

    R = l/(n*d**4)
    return R

#Getting edges and vertices from a dataframe
def makeEV(segments):
    edges = []
    vertices = []
    for index, row in segments.iterrows():
        new_edge = Edge(row['id1'],row['id2'])
        if 'Length' in list(segments):
            new_edge.length = row['Length']
        else:
            new_edge.length = math.sqrt((row['x1'] - row['x2'])**2 + (row['y1']-row['y2'])**2)

        if 'LineWidth' in list(segments):
            new_edge.width = row['LineWidth']

        edges.append(new_edge)
        vertices = vertices + [Point(row['x1'],row['y1'], row['id1']), Point(row['x2'],row['y2'],row['id2'])]


    #Run through points and map ones that are
    ## TODO: Adjust the thresholding step; make sure to add edge weighting stuff
    thresh = 2*math.sqrt(2) #Will want mechanism for adjusting threshold to account for other cutoffs; or to refine sampling protocol

    for i in range(len(vertices)):
        for j in [index for index in range(len(vertices)) if index > i]:
            u = vertices[i]
            v = vertices[j]

            if vertex_distance_object(u, v) <= thresh:
                v.alias = u.alias
    for v in vertices:
        if v.id != v.alias:
            v.keep = False

    return vertices, edges

def make_graph(vertices, edges):
    #Assumes GraphTool rather than GraphML or other light-weight option; add alternative for flexibility
    g = gt.Graph(directed = False)

    #Vertex properties
    g.vp.pos = g.new_vertex_property("vector<float>")

    #Edge properties
    g.ep.length = g.new_edge_property("float")
    g.ep.width = g.new_edge_property("int")
    g.ep.res = g.new_edge_property("float")
    g.ep.vol = g.new_edge_property("float")

    #Make vertices
    for v in vertices:
        if v.keep:
            new = g.add_vertex()
            g.vp.pos[new] = [v.x,v.y]

            v.graph_index = g.vertex_index[new]

    #Make edges:
    for e in edges:
        v1_orig = [v for v in vertices if v.id == e.id1][0]
        v1 = [v for v in vertices if v.id == v1_orig.alias][0]

        v2_orig = [v for v in vertices if v.id == e.id2][0]
        v2 = [v for v in vertices if v.id == v2_orig.alias][0]

        u1 = g.vertex(v1.graph_index)
        u2 = g.vertex(v2.graph_index)

        if u1 != u2:
            new_e = g.add_edge(u1, u2)
            g.ep.length[new_e] = e.length
            g.ep.width[new_e] = e.width
            ## TODO: Use function to calculate weight and volume
            g.ep.res[new_e] = e.length/e.width**4
            g.ep.vol[new_e] = e.width**2*e.length
    return g

#Includes option for printing metadata
def save_graph(g, orig_file_path, metadata = None):
    csv_name = orig_file_path.split("/")[-1]
    graph_name = csv_name.split(".")[0] + ".xml.gz"
    g.save(graph_name)

    if metadata:
        filename = csv_name.split(".")[0]+".txt"
        with open(filename, "w+") as f:
            print(metadata, file=f)
    return


def displayGraph(g):
    gt.graph_draw(g, pos = g.vp.pos, edge_pen_width=g.ep.width)
    return

def parse_name(filepath):
    filename = filepath.split("/")[-1]
    graphname = filename.split(".")[:-1]
    if len(graphname) > 1:
        return ".".join(graphname)
    else:
        return graphname

def parseHeader(path):
    try:
        data = pd.read_csv(path)
        return list(data)
    except pd.errors.ParserError:
        print("Can't read file. Please select another.")
        return

#Appends a row to a csv file. Assumes file path has already been validated, double checks that row is correct.
#Assumes the last line of the csv includes linebreak
def appendRow(path, row):
    if len(list(pd.read_csv(path))) != len(row):
        print("Bad row or incorrect file. Please try again.")
        return
    else:
        with open(path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)
        return

def functionLookup():
    lookup = {}

#Opens interactive window for selecting "source" node of graph. Source required for max flow calculations.
#Returns graph_tool vertex that was selected
def setSource(g):
    coord, filter = gt.interactive_window(g, pos = g.vp.pos)

    if sum(filter.get_array()) != 1:
        print("Select exactly one source node.")
        return
    else:
        index = np.where(filter.get_array()==1)[0][0]
        source = g.vertex(index)
        return source

## Graph Statistics/Analytics
def efficiency(graph, weight = None):
    all_shortest_paths = gt.shortest_distance(graph, weights = weight)
    N = graph.num_vertices()
    path_list = [x for vector in all_shortest_paths for x in vector]
    inverse_sum = sum([1/x if x > 0 else x for x in path_list])
    try:
        efficiency = 1/(N*(N-1))*inverse_sum
    except ZeroDivisionError:
        efficiency = np.nan
    return efficiency

## TODO: Verify weighting option
def cost_calc(graph, weight = None):
    orig_filter = graph.get_edge_filter()
    if weight is None:
        n_orig = graph.num_edges()
        mst = gt.min_spanning_tree(graph)
        graph.set_edge_filter(mst)
        try:
            c = n_orig/graph.num_edges()
        except ZeroDivisionError:
            c = np.nan
    else:
        n_orig = sum(weight.get_array()[:])
        mst = gt.min_splanning_tree(graph, weights = weight)
        graph.set_edge_filter(mst)
        n_new = sum(weight.get_array()[:])
        try:
            c = n_orig/n_new
        except ZeroDivisionError:
            c = np.nan
    graph.set_edge_filter(orig_filter[0])
    return c

## TODO: Add second weighting option - MST should use cost, shortest paths should use resistance
def performance(graph, weight = None):
    orig_filter = graph.get_edge_filter()

    mst = gt.min_spanning_tree(graph, weights =weight)
    g_shortest = [x for vector in gt.shortest_distance(graph, weights = weight) for x in vector]
    graph.set_edge_filter(mst)
    g_mst_shortest = [x for vector in gt.shortest_distance(graph, weights = weight) for x in vector]

    try:
        p = stats.mean(g_shortest)/stats.mean(g_mst_shortest)
    except ZeroDivisionError:
        p = np.nan

    graph.set_edge_filter(orig_filter[0])
    return p

def component_size(graph):
    map = gt.label_largest_component(graph)
    return sum(map.a[:])

def mean_btwn(graph,weight = None, mode = "edge"):
    vbtwn, ebtwn = gt.betweenness(graph, weight = weight)
    mean = stats.mean(ebtwn.get_array()[:])
    sd = stats.stdev(ebtwn.get_array()[:])
    return mean, sd

#Graph is a graph data structure
#Outfile is the path to save the output (as a text CSV)
#Mode is one of "random", "weighted", "betweenness"
#Weight is the graph EdgePropertyMap to sort by
#Ascending is low to high value (default)
#Root is a vertex, largest component set to root
def fault_tolerance(graph, outfile, mode = "random", weight = None, ascending=True):
    #Create a "filter" property to use with graph
    filter = graph.new_edge_property("bool")
    filter.get_array()[:] = 1

    #Create and sort a set of indices
    if mode == "random":
        index = list(range(filter.get_array().size -1))
        shuffle(index)
    elif mode == "weighted":
        if ascending:
            index = list(np.argsort(weight.get_array()))
        else:
            index = list(np.argsort(weight.get_array()))[::-1]
    elif mode == "betweenness":
        vbtwn, ebtwn = gt.betweenness(graph, weight = weight)
        if ascending:
            index = list(np.argsort(ebtwn.get_array()))
        else:
            index = list(np.argsort(ebtwn.get_array()))[::-1]
    else:
        print("invalid mode")
        return

    #Set up storage structure for data
    n_removed = []
    largest = []
    cost = []
    perf = []
    eff = []

    counter = 0
    for i in index:
        #Store prev. iteration data
        n_removed.append(counter)
        largest.append(component_size(graph))
        cost.append(cost_calc(graph))
        perf.append(performance(graph))
        eff.append(efficiency(graph))

        #Update everything
        counter += 1
        filter.get_array()[i,] = 0
        graph.set_edge_filter(filter)

    data = pd.DataFrame({"Removed" : n_removed, "LargestConnected" : largest, "Cost": cost, "Performance" : perf, "Efficiency" : eff})
    data.to_csv(outfile)

#Variant fault tolerence test - N runs of edge removal until component connected to source is chosen proportion of orig size
#Propmpts for a source node if none is given
def iterateFault(graph, source = None, N = 100, prop = 0.5):
    if source is None or source.is_valid() is False:
        source = setSource(graph)
    total = sum(gt.label_out_component(graph, source).a[:])
    stop = prop*total

    filter = graph.new_edge_property("bool")
    index = list(range(filter.get_array().size -1))
    results = [0]*N
    for i in range(N):
        filter.get_array()[:] = 1
        shuffle(index)
        count = 0
        for edge in index:
            filter.get_array()[edge,] = 0
            graph.set_edge_filter(filter)
            count += 1
            if sum(gt.label_out_component(graph, source).a[:]) < stop:
                break
        results[i] = count
    return results

#Returns a list, sorted largest to smallest, of real non-zero eigenvalues of the graph Laplacian
def spectra(graph, weight = None):
    l = gt.laplacian(graph, weight = weight)
    eigenval, eigenvec = scipy.sparse.linalg.eigs(l)
    real_eigen = [i.real for i in eigenval if i.imag == 0]
    return sorted(real_eigen, reverse = True)


def cheegerApprox(graph, weight = None):
        eigenval = spectra(graph, weight)
        sse = eigenval[-2]
        cheeger = math.sqrt(2*sse)
        return cheeger
