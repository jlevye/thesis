#!/usr/bin/python3
"""
A method for converting a CSV file of data from ImageJ - exported as a CSV using ImageJDataExport.py.
"""
#Module import
import pandas as pd
import numpy as np
import csv
import sys
import math
import graph_tool.all as gt
import tkinter as tk
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

    #Option one
    option1 = ["X","Y","Angle","Width","Height","LineWidth","Length"]
    #Option two
    option2 = ["x1","x2","y1","y2","Width","Length"]

    if all([name in names for name in option1]):
        data = boundbox_to_xy(data[opton1])
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

    return

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
            #TO DO: Add function that allows user to choose the formula used here! (Ie, make the resistance calculation a function depending on user input
            g.ep.res[new_e] = e.length/e.width**4
            g.ep.vol[new_e] = e.length*e.width**2

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

    #Create edge objects out of each row in the data frame & point objects out of each possible endpoint
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

    display = messagebox.askyesno("Draw Graph","Would you like to display the graph?")
    if display:
        gt.graph_draw(g, pos = g.vp.pos, edge_pen_width=g.ep.width)

    save_graph(g)
