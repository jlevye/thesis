#Graph_tool code snippets and examples

g = Graph()
ug = Graph(directed=False)
#OR
ug = Graph()
ug.set_directed(False)

#Check with
g.is_directed()

#Copy by
g1 = Graph(g)

#Add vertices and edges; can add a number to create a list of multiple vertices and can remove them by name
v1 = g.add_vertex()
v2 = g.add_vertex()
e = g.add_edge(v1, v2)

#Iteration; can also iterate over neighbors, in or out edges, etc
for v in g.vertices():
    #do a thing
for e in g.edges():
    #do a different thing

#Property maps allow assigning extra information to an edge or vertex; define a property by its variable type; can be made a part of the graph, so when a saved graph is loaded the property will be stored

#Filtering - you can filter out edges/vertices to not include via properties in the maps - 1 is included, 0 is excluded

#Useful functions for properties of a graph g

tree = min_spanning_tree(g)
  # This gives you a bool of yes if belongs to tree, no if not

bv, be = betweenness(g)
  #Gives betweenness centrality for every edge/vertex

clust = local_clustering(g)
  #Clustering coefficient for every vertex - global and extended

graph_tool.flow
    #Library of modules for flow and cut snippets - source-target or general min cut of undrected graph

graph_tool.spectral
    #Library for getting the matrices, in particular the graph laplacian matrix

distance_histogram(g)
    #Removes shortest-distance histogram for every vertex pair
    
