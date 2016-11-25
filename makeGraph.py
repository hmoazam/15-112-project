#Modification history:
#Date          Start time           End time
#10/11/2016    3.00pm               6.30pm
#10/11/2016    10.00pm              1.30am

#this file creates the graph itself, and is imported into the main file that is run, where the functions are used

import networkx as nx
import math

G=nx.Graph() # G is the graph

f = open("Nodesfile.txt", "r")
allData = f.readlines()
nodes = allData[1:] # list with the nodes data
f.close()

nodeList = []

for item in nodes:
    asList = item.split(",") #spit to get list with node number and x and y coordinates separated
    num = int(asList[0]) # the node number
    nodeList.append(num)

G.add_nodes_from(nodeList) # add the nodes to the graph


def getPath(start, end): # this function is called in the main file when we want to draw the line
     global G
     return nx.dijkstra_path(G, start, end) #returns the list of nodes visited in the order that they were visited. Uses dijkstra's shortest path algorithm

# getWeight is called by addEdge. Calculates the Euclidean distance between adjacent nodes and returns this to the addEdge function
def getWeight(main, node2):
    f1 = open("Nodesfile.txt", "r")
    a = f1.readlines()
    f1.close()
    coords = a[1:]
    for j in coords:
        b = j.strip() # remove /n
        c = b.split(",") # make a list
        if main == int(c[0]): # finding the node number in the list that matches. Once we find the match, we get its x and y coordinates
            x1 = float(c[1])
            y1 = float(c[2])
        if node2 == int(c[0]): # same process for the second node
            x2 = float(c[1])
            y2 = float(c[2])
    weight = math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2)) #Euclidean distance
    return weight

#function that creates the edges of the graph. Each edge is weighted, with the Euclidean distance (found in getWeight) being the weight. This weight is used to determine the shortest path
def addEdge(main, neighbours): #main = current node, neighbours is a list of the nodes' neighbours (strings)
    for i in neighbours:
        node2 = int(i)
        weight = getWeight(main, node2) # get the Euclidean distance
        G.add_edge(main, node2, weight = weight) # then add the weighted edge to the graph

fN = open("neighbours.txt", "r")
neighbours = fN.readlines() #list cintaining each node and its neighbours
fN.close()

for i in neighbours:
    clean = i.strip() #removes the \n character
    a = clean.split(":") # the node we are looking at is separated from the neighbours by a colon
    main = int(a[0]) # the node we will create edges from
    x = a[1:] # the neighbours
    adjStr = x[0] #the adjacent nodes, all in one string
    individual = adjStr.split(",") #neighbours are separated by commas
    List = individual[0:len(individual)-1]
    addEdge(main, List) # add edges from the current node to all its neighbours
