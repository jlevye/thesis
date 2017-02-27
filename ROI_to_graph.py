#!/usr/bin/python3
"""
A method for converting a CSV file of data from ImageJ ROIs (with possible conversion to ImageJ plugin) into a graph object.
"""
#Module import
import pandas as pd
import numpy as np
import csv
import sys
import math
import graph_tool.all as gt
import tkinter as tk
from tkinter import filedialog

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

#Function definitions
def vertex_distance_object(u, v):
    if not isinstance(u, Point) or not isinstance(v, Point):
        print("Needs point objects. Use another distance function if only using coordinates.")
        return

    dist = math.sqrt((u.x - v.x)**2 + (u.y - v.y)**2)
    return dist

def open_check_csv():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    if not file_path.endswith(("csv","CSV")):
        print("Bad file type.")
        return

    data = pd.read_csv(file_path)
    names = list(data)

    required = ["BX","BY","Width","Height","Angle"]
    extra = ["Length","LWidth"]

    if not all([name in names for name in required]):
        print("Needs angle and bounding box measurement output.")
        return
    elif all([name in names for name in extra]):
        keep = required + extra
        data = data[keep]
        return data
    else:
        data = data[required]
        return data

def boundbox_to_xy(df):
    #Note, edits df in place!

    df['case'] = np.where(np.logical_or(df['Angle'] >= 90, np.logical_and(np.greater(df['Angle'],-90),np.less(df['Angle'],0))), 1,2)

    df['x1'] = df['BX']
    df['x2'] = df['BX'] + df['Width']
    df['y1'] = np.where(df['case']==1, df['BY'],df['BY'] + df['Height'])
    df['y2'] = np.where(df['case']==2, df['BY'],df['BY'] + df['Height'])

    #make preliminary/initial IDs
    df['id1'] = [i for i in range(len(df))]
    df['id2'] = [i for i in range(len(df), 2*len(df))]

    #Drop extra columns
    to_drop = ["BX","BY","Height","Width","Angle"]
    df.drop(to_drop, axis = 1, inplace = True)

    return

def make_graph(vertices, edges):
    #Assumes GraphTool rather than GraphML or other light-weight option; add alternative for flexibility
    g = gt.Graph(directed = False)

    #Vertex properties
    g.vp.pos = g.new_vertex_property("vector<float>")

    #Edge properties
    g.ep.length = g.new_edge_property("float")
    g.ep.width = g.new_edge_property("int")

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

        new_e = g.add_edge(u1, u2)
        new_e.length = e.length
        new_e.width = e.width

    return g

def save_graph(g):
    filename = filedialog.asksaveasfilename(defaultextension=".xml.gz")
    if filename is None:
        return
    g.save(filename)
    return


#Main method
if __name__ == "__main__":

    #Load in dataset of line segment information
    segments = open_check_csv()

    #Bounding box to x,y coordinate pairs
    boundbox_to_xy(segments)

    #Create edge objects out of each row in the data frame & point objects out of each possible endpoint
    edges = []
    vertices = []
    for index, row in segments.iterrows():
        new_edge = Edge(row['id1'],row['id2'])
        if 'Length' in list(segments):
            new_edge.length = row['Length']
        else:
            new_edge.length = math.sqrt((row['x1'] - row['x2'])**2 + (row['y1']-row['y2'])**2)

        if 'LWidth' in list(segments):
            new_edge.width = row['LWidth']

        edges.append(new_edge)
        vertices = vertices + [Point(row['x1'],row['y1'], row['id1']), Point(row['x2'],row['y2'],row['id2'])]


    #Run through points and map ones that are
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

    g = make_graph(vertices, edges)
