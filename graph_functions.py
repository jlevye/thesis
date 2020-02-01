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
def get_batch_files(open_directory):
    csv_files = [open_directory + "/" + file for file in os.listdir(open_directory) if file.endswith(("CSV","csv"))]
    svg_files = [open_directory + "/" + file for file in os.listdir(open_directory) if file.endswith(("SVG","svg"))]

    #Also set the save location: creates a folder called "Graph" in the parent of the CSV folder.
    parent = os.path.dirname(open_directory)
    os.chdir(parent)

    try:
        os.mkdir("Graph")
        os.chdir("Graph")
    except FileExistsError:
        os.chdir("Graph")

    return csv_files, svg_files

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

##Functions for splititng intersections/processing image files
#s and t are tuples or lists x1,y1 and x2,y2
def slope(s,t):
    if t[0]-s[0] == 0:
        m = None
    else:
        m = float((t[1]-s[1]))/float((t[0]-s[0]))
    return m

def distance(s,t):
    d = math.sqrt((s[0]-t[0])**2 + (s[1]-t[1])**2)
    return d

#p is point, m is slope
def intercept(p, m):
    if m is not None:
        b = -1*m*p[0] + p[1]
    else:
        b = None
    return b

#a and b are pairs of tuples = coordinate pairs (ie: [(x1,y1),(x2,y2)])
def intersect(a, b, fuzz = 0):
    m1 = slope(a[0], a[1])
    m2 = slope(b[0], b[1])
    b1 = intercept(a[0], m1)
    b2 = intercept(b[0], m2)

     #Don't try to divide by 0 if lines are parallel
    if m1 == m2:
        return False
    #Check for vertical lines:
    elif any([i is None for i in [m1,m2,b1,b2]]):
        if m1 is None:
            x = a[0][0]
            y = m2*x + b2
        elif m2 is None:
            x = b[0][0]
            y = m1*x + b1
    else:
        x = (b2 - b1)/(m1 - m2)
        y = m1*x + b1

    #Define the bounds, xs and ys for redundancy
    X1s = sorted([a[0][0], a[1][0]])
    X2s = sorted([b[0][0], b[1][0]])

    lowerX1 = X1s[0] - fuzz
    upperX1 = X1s[1] + fuzz
    lowerX2 = X2s[0] - fuzz
    upperX2 = X2s[1] + fuzz

    Y1s = sorted([a[0][1], a[1][1]])
    Y2s = sorted([b[0][1], b[1][1]])

    lowerY1 = Y1s[0] - fuzz
    upperY1 = Y1s[1] + fuzz
    lowerY2 = Y2s[0] - fuzz
    upperY2 = Y2s[1] + fuzz

    if all([lowerX1 <= x <= upperX1,lowerX2 <= x <= upperX2,lowerY1 <= y <= upperY1,lowerY2 <= y <= upperY2]):
        return [x,y]
    else:
        return False

#a is a row in a dataframe, crosses are all the other rows
#Eventually returns a list of line segments correctly indicating breaks in a
#Uses 1/2 the width as the cut-off for intersections
def findSplits(row, crosses, minimum=1):
    width = row[4]
    a = [[row[0],row[1]],[row[2],row[3]]]
    ends = [a[0]]
    fuzz = 0.5*width
    for cross in crosses:
        b = [[cross[0],cross[1]],[cross[2],cross[3]]]
        p = intersect(a, b, fuzz)
        if p:
            ends.append(p)
    ends.append(a[1])

    ends.sort() #Sorts by the first element by default, so sorted by x value
    segments = []

    for i in range(len(ends)-1):
        a = ends[i]
        b = ends[i + 1]

        l = distance(a,b)
        if l >= minimum:
            newLine = [a[0],a[1],b[0],b[1],width,l]
            segments.append(newLine)

    new_segs = pd.DataFrame(segments, columns = ["x1","y1","x2","y2","Width","Length"])
    return new_segs

def split_data(data, minimum=1):
    minlength = min(data["Length"])
    segs = data.values.tolist()
    new_data = pd.DataFrame(columns = ["x1","y1","x2","y2","Width","Length"])

    if isinstance(minimum, int) or isinstance(minimum, float):
        minimum = minimum
    elif isinstance(minimum, str):
        if minimum.isnumeric():
            minimum = float(minimum)
        else:
            minimum = minlength

    for seg in segs:
        crosses = [s for s in segs if s is not seg]
        splits = findSplits(seg, crosses, minimum)
        new_data = new_data.append(splits, ignore_index = True)

    return new_data

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
    df.rename(columns={"LineWidth":"Width"},inplace = True)
    return df

#Calculating approximate edge resistance - multiple options
def edge_resist(Diam, l, d = 0, n = 1, type = "const_n",alpha = 0.6, p = 1):
    area = (math.pi*(Diam/2)**2)*p

    #Correctly calculate d (hydralically weighted mean diameter)
    if type == "const_n": #How big can n circles be inside size Diam*p?
        small_area = area/n
        d = 2*math.sqrt(small_area/math.pi)
    elif type == "const_d": #How many circles of size d it inside Diam*p? - must be at least 1
        small_area = math.pi*(d/2)**2
        n = max(1,math.floor(area/small_area))
    elif type == "taper": #How many circles of Diam^alpha fit in Diam*p? - must be at least 1
        d = Diam**alpha
        small_area = math.pi*(d/2)**2
        n = max(1,math.floor(area/small_area))
    else:
        print("Incorrect mode.")
        return

    R = l/(n*d**4)
    return R

#Getting edges and vertices from a dataframe
def makeEV(segments, thresh = 0):
    edges = []
    vertices = []
    for index, row in segments.iterrows():
        new_edge = Edge(row['id1'],row['id2'])
        if 'Length' in list(segments):
            new_edge.length = row['Length']
        else:
            new_edge.length = math.sqrt((row['x1'] - row['x2'])**2 + (row['y1']-row['y2'])**2)

        if 'Width' in list(segments):
            new_edge.width = row['Width']

        if new_edge.width != 0:
            edges.append(new_edge)
            vertices = vertices + [Point(row['x1'],row['y1'], row['id1']), Point(row['x2'],row['y2'],row['id2'])]


    #Run through points and map ones that are the same
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

#takes list of parameters as input; otherwise sets up defaults
#If params isn't none, has to be dict generated by function in GUI
def make_graph(vertices, edges, params = None):
    if params:
        try:
            thresh = params["thresh"].value
            d = params["d"].value
            n = params["n"].value
            mode = params["DiamMode"].value
            alpha = params["alpha"].value
            prop = params["prop"].value
        except KeyError:
            print("Invalid parameter set. Using defaults.")
            thresh = 0
            d = 0
            n = 1
            mode = "const_n"
            alpha = 0.6
            prop = 1
    else:
        thresh = 0
        d = 0
        n = 1
        mode = "const_n"
        alpha = 0.6
        prop = 1


    #Assumes GraphTool rather than GraphML or other light-weight option; add alternative for flexibility
    g = gt.Graph(directed = False)

    #Vertex properties
    g.vp.pos = g.new_vertex_property("vector<float>")

    #Edge properties
    g.ep.length = g.new_edge_property("float")
    g.ep.width = g.new_edge_property("float")
    g.ep.res = g.new_edge_property("float")
    g.ep.vol = g.new_edge_property("float")

    #Graph properties; set equal to "unset" default
    g.gp.source = g.new_graph_property("int")
    g.gp.source = -1

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
            g.ep.res[new_e] = edge_resist(e.width, e.length, d, n, mode, alpha, prop)
            g.ep.vol[new_e] = e.width**2*e.length
    return g

#Includes option for printing metadata
def save_graph(g, orig_file_path, outfolder = None, metadata = None):
    csv_name = orig_file_path.split("/")[-1]
    graph_name = csv_name.split(".")[0] + ".xml.gz"
    if outfolder is not None:
        os.chdir(outfolder)

    g.save(graph_name)

    if metadata:
        filename = csv_name.split(".")[0]+".txt"
        with open(filename, "w+") as f:
            print(metadata, file=f)
    return


def displayGraph(g):
    gt.graph_draw(g, pos = g.vp.pos, edge_pen_width=gt.prop_to_size(g.ep.width, mi = 1, ma = 10, power = 1))
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
#Takes a list of header names from parseHeader and returns a list with the function name and weight
def headerFormatter(header):
    names = ["GraphID", "FIlepath","NVertices","AvgDegree","NEdges","TotalLength","MaxWidth","AvgWidth","Cost","Efficiency","TransportPerformance","LaPlacianSpectra","EdgeBetweennessMean","EdgeBetweennessSD","CheegerLimit","MinCut"]
    req_weight = ["Cost","Efficiency","TransportPerformance","LaPlacianSpectra","EdgeBetweennessMean", "CheegerLimit","MinCut"]

    out = []
    excluded = []
    for col in header:
        parts = col.split(".",maxsplit=1)
        name = parts[0]
        weight = parts[1]

        if name in names:
            if name in req_weight:
                out.append([name, weight])
            else:
                out.append([name])
        else:
            excluded.append(col)

    if len(excluded) > 0:
        print("The following columns were excluded:\n")
        for c in excluded:
            print(c)

    return out



#Opens interactive window for selecting "source" node of graph. Source required for max flow calculations.
#Returns graph_tool vertex that was selected
#Also saves as a graph property for future use
def setSource(g):
    coord, filter = gt.interactive_window(g, pos = g.vp.pos, edge_pen_width=gt.prop_to_size(g.ep.width, mi = 1, ma = 10, power = 1))

    if sum(filter.get_array()) != 1:
        print("Select exactly one source node.")
        return
    else:
        index = np.where(filter.get_array()==1)[0][0]
        g.gp.source = index
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
        mst = gt.min_spanning_tree(graph, weights = weight)
        graph.set_edge_filter(mst)
        n_new = sum(weight.get_array()[mst.get_array().astype("bool")])
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
    root = graph.gp.source
    if root >= 0:
        map = gt.label_out_component(graph, root)
    else:
        map = gt.label_largest_component(graph)
    return sum(map.a[:])

def mean_btwn(graph,weight = None, mode = "edge"):
    vbtwn, ebtwn = gt.betweenness(graph, weight = weight)
    mean = stats.mean(ebtwn.get_array()[:])
    sd = stats.stdev(ebtwn.get_array()[:])
    return mean, sd

def widest(g):
    return max(g.ep.width.get_array()[:])

def avgwidth(g):
    total_vol = sum(g.ep.vol.get_array()[:])
    total_len = sum(g.ep.length.get_array()[:])
    return total_vol/total_len

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
def iterateFault(graph, N = 100, prop = 0.5):
    if graph.gp.source = -1:
        source = setSource(graph)
    else:
        try:
            source = graph.vertex(g.gp.source)
        except ValueError:
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

#Returns a list, sorted largest to smallest, of "return" non-zero eigenvalues of the graph Laplacian (default= 100 values)
#Requires g to be undirected, else L is not symmetrical
#Can also return Cheeger Approx
def spectra(graph, numout = 100, weight = None, descending = True):
    l = gt.laplacian(graph, weight = weight)
    n = graph.num_vertices()
    eigenval = scipy.sparse.linalg.eigsh(l, k = n-1, which = "BE", )
    #All will be real for symmetrical graph; instead rounding to 6 decimal places
    eigen_out = [round(i, 6) for i in eigenval]
    #Make sure lambda_0 = 0
    #If it isn't, ask if user wants to continue TODO - error handling
    # if eigen_out[0] != 0:
    #     response = messagebox.askokcancel(message="Smallest eigenvalue is non-zero. This indicates a potential problem with the data. Generate output anyway?")
    #
    #TODO uncomment after deciding if keeping
    idx = np.round(np.linspace(0, n-2, 100)).astype(int)
    #Replace real_eigen with real_eigen(idx)


def cheegerApprox(graph, weight = None):
        eigenval = scipy
        sse = eigenval[-2]
        cheeger = math.sqrt(2*sse)
        return cheeger
