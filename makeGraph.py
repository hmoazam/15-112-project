import networkx as nx

G=nx.Graph()
f = open("nodesfile.txt", "r")
allData = f.readlines()
nodes = allData[1:]

nodeList = []

for item in nodes:
    asList = item.split(",")
    num = int(asList[0])
    nodeList.append(num)

G.add_nodes_from(nodeList)

print G.number_of_nodes()
