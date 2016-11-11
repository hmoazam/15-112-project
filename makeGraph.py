#Modification history:
#Date          Start time           End time
#10/11/2016    3.00pm               6.30pm
#10/11/2016    10.00pm              1.30am


import networkx as nx
import math
import matplotlib.pyplot as plt

G=nx.Graph()

f = open("Nodesfile.txt", "r")
allData = f.readlines()
nodes = allData[1:]
f.close()

nodeList = []

for item in nodes:
    asList = item.split(",")
    num = int(asList[0])
    nodeList.append(num)

G.add_nodes_from(nodeList)

#print G.nodes()
#print G.number_of_nodes()

# now need to create the edges, and these need to be weighted. The weight is the Euclidean distance between two nodes

def getPath(start, end):
     global G
     return nx.dijkstra_path(G, start, end) #returns the list of nodes visited in order

def getWeight(main, node2):
    #print "m", main
    #print node2
    f1 = open("Nodesfile.txt", "r")
    a = f1.readlines()
    f1.close()
    coords = a[1:]
    #print coords
    for j in coords:
        b = j.strip() #remove /n
        c = b.split(",")
        #print c
        if main == int(c[0]):
            x1 = float(c[1])
            y1 = float(c[2])
        if node2 == int(c[0]):
            x2 = float(c[1])
            y2 = float(c[2])
    weight = math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2))
    return weight

def addEdge(main, neighbours): #main = current node, neighbours is a list of neighbours(strings)
    for i in neighbours:
        node2 = int(i)
        weight = getWeight(main, node2)
        G.add_edge(main, node2, weight = weight) #should main and node2 be strings or integers?? Right now they're integers


fN = open("neighbours.txt", "r")
neighbours = fN.readlines()
#print neighbours
fN.close()

for i in neighbours:
    clean = i.strip() #removes the \n character
    a = clean.split(":")
    main = int(a[0]) #the node we will create edges from
    #print main
    x = a[1:]
    adjStr = x[0] #the adjacent nodes, all in one string
    individual = adjStr.split(",")
    #print individual
    List = individual[0:len(individual)-1]
    addEdge(main, List)


#testing

# print nx.dijkstra_path(G, 6, 32, weight = "weight")
# print nx.dijkstra_path(G, 58, 11, weight = "weight")
# print nx.dijkstra_path(G, 29, 45)
# print nx.dijkstra_path(G, 1, 8)
# print nx.dijkstra_path(G, 45, 29)

#print getPath(6,32)





#nx.draw(G)
