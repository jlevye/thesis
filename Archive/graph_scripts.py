#!/usr/bin/python3
"""Functions for generating a graph from images and points.

Points are drawn from a two-column csv in (x,y) pairs.
The image is a binary trace of a leaf, with veins as straight-line segments.

This version of this file is a major revision started 1/5/2017.
"""

#Modules required
import math
import csv
from operator import add
import copy

import numpy as np
import graph_tool.all as gt
from PIL import Image

import edge_test2 as et
from helper import *

#Master function for setting up vertices and edges, outside of graph.
#Image should be a numpy array; points is a list of Point objects.
#Returns a list of point objects and a list of tuples representing edges.
def nodes_and_edges(image, points):
    bounds = image.shape

    #Set up point attributes not automatically set.
    for p in points:
        try:
            p.r = biggest_circle([p.x, p.y], image)
            p.circle = full_circle([p.x,p.y], p.r+1, bounds)
        except VertexError:
            points.remove(p)
            print("Bad vertex removed.")

    #Set up edges
    edges = []
    exclude = [[x,y] for x in range(bounds[1]) for y in range(bounds[0]) if image[y][x] == 0]

    for start in points:
        new_points = [point for point in points if point is not start]
        terminii = []
        #Exclude all white pixels to start

        try:
            step_forward(terminii, [start.x, start.y], exclude, image, new_points)
            for t in terminii:
                e = [start.i, t]
                e.sort()
                if e not in edges:
                    edges.append(e)
        except RecursionError:
            print("Hit recursion depth at vertex {}".format(start.i))
        finally:
            pct = start.i/len(points) * 100
            if pct % 10 == 0:
                print("Through {}% of edges".format(pct))
    return edges

#Edge functions in progress
#Terminii should be a list (empty or not), that will be modified throughout this function and contain indices of edge end points for a given starting point.
#Exclude starts with all white pixels and is expanded to include pixels already tested.

#WHAT WORKS:
#If lines are 1px thick, seems to correctly identify all edges with no extras

#WHAT DOESN'T WORK:
#Lines thicker than 2px ...

def step_forward(terminii, start, exclude, image, points):
    exclude.append(start)
    ring = dedup(make_circle(start, 1))

    xmax = image.shape[1]
    ymax = image.shape[0]

    keep = []
    for p in ring:
        if all([p[0] < xmax, p[1] < ymax, p not in exclude]):
            keep.append([p, distance(p, start)])

    if keep == []:
        return
    else:
        keep = sorted(keep, key=lambda x: x[1], reverse= True)
        for value in keep:
            pt = value[0]
            if pt in [pixel for point in points for pixel in point.circle]:
                terminii.append([point.i for point in points if pt in point.circle][0])
                return
            else:
                exclude.append(pt)
                step_forward(terminii, pt, exclude, image, points)
        return

#Graph functions
#TODO: Update this with correct vertex assignment stuff and properties
def init_graph(points, edges, image, source=0):
    """Convert list of point objects and edges into graph, with graph properties."""

    #Initialize undirected graph.
    g = gt.Graph(directed=False)

    #Set some parameters.
    dim = [image.shape[1], image.shape[0]] #[width,height]
    disp = [int(600*dim[0]/dim[1]), 600]

    #Initialize graph properties
    gen_graph_props(g)
    points_to_vertices(g, points, dim, disp)

    for pair in edges:
        v = g.vertex(pair[0])
        u = g.vertex(pair[1])
        e = g.add_edge(u, v)

        #Assign edge properties here

    return g

def gen_graph_props(graph):
    """Creates a set of internal property maps for a graph_tool graph."""

    g = graph

    #Graph properties
    gpropS = g.new_graph_property("int")
    g.gp.source = gpropS

    #Vertex properties
    vpropX = g.new_vertex_property("int") #x position
    vpropY = g.new_vertex_property("int") #y positon
    vpropR = g.new_vertex_property("int") #radius of largest circle that fit
    vpropCoord = g.new_vertex_property("vector<float>") #Coordinates for plotting
    g.vp.x = vpropX
    g.vp.y = vpropY
    g.vp.r = vpropR
    g.vp.coord = vpropCoord

    #Edge properties
    epropFloat = g.new_edge_property("float")
    epropDiam = g.new_edge_property("int")
    epropMid = g.new_edge_property("vector<int>")
    epropWidth = g.new_edge_property("int")
    g.ep.dist = epropFloat
    g.ep.d = epropDiam
    g.ep.mid = epropMid
    g.ep.width = epropWidth

def points_to_vertices(graph, points, dim, disp):
    """Adds points, given in form of list of Point objects, as vertices to graph"""
    g = graph

    for point in points:
        v = g.add_vertex()
        g.vp.x[v] = point.x
        g.vp.y[v] = point.y
        g.vp.r[v] = point.r

        g.vp.coord[v] = [(x+1)*z/y for x,y,z in zip([point.x,point.y],dim,disp)]
        if g.vp.coord[v][0] == disp[0]:
            g.vp.coord[v][0] = disp[0]-1
        if g.vp.coord[v][1] == disp[1]:
            g.vp.coord[v][1] = disp[1]-1
