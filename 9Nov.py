import Tkinter
#import networkx as nx

#f = open("Nodesfile.txt", "a+") # a+ means can append and read open file for appending so doesn't delete old contents
#f.write("hi")
#global allNodes
#global Nodesfile

def getNodeCoord(node):
    global info
    impInfo = info[1:]
    for j in impInfo:
        allDetails = j.strip() #removing the /n
        List = allDetails.split(",") #now we get a list with the information for each of the nodes
        if List[0] == node:
            xCoord = List[1]
            yCoord = List[2]
            return ((xCoord, yCoord)) #return a tuple with the x,y coordinates


def getNode(x, y):
    global info
    nodeInfo = info[1:]
    for i in nodeInfo:
        allDetails = i.strip() #removing the /n
        List = allDetails.split(",") #now we get a list with the information for each of the nodes
        xCoord = int(float(List[1]))
        yCoord = int(float(List[2]))
        if (x == xCoord and y == yCoord):
            return List[0] #the node number is at index 0 in the list that we just created


def drawCircle(x, y, colour):
    global canvas
    c = canvas.create_oval(x-5, y-5, x+5, y+5, fill = colour) #should draw a circle of diameter 10, with the center of the circle the coordinates of the node
    return c #will this work to save the circle itself in the list??


def selectNode(event):
    global canvas
    global info
    global listDone
    global listDoneC
    x = canvas.canvasx(event.x) # need the x and y coordinates relative to the canvas, not just what's within the frame
    y = canvas.canvasy(event.y)
    nodesList = info[1:]

    #currNode = canvas.find_closest(x, y)
    #canvas.delete(currNode)

    for node in nodesList: #for every node in the list, need to see if what we clicked was an actual node
        nodeData1 = node.strip()
        nodeData2 = nodeData1.split(",")
        #print nodeData2
        xCoord = int(float(nodeData2[1]))
        yCoord = int(float(nodeData2[2]))
        if (abs(x - xCoord) < 10) and (abs(y - yCoord) < 10): #checks if within the size of the node, if it is, turns it green
            circle = drawCircle(xCoord, yCoord, "green") #this works!!
            listDone.append((xCoord, yCoord))
            listDoneC.append(circle)


def getNeighbours(event): #bind to spacebar?
    global canvas
    global info
    global listN
    global listNC
    x = canvas.canvasx(event.x) # need the x and y coordinates relative to the canvas, not just what's within the frame
    y = canvas.canvasy(event.y)
    nodesList = info[1:]
    #currNode = canvas.find_closest(x, y)
    #canvas.delete(currNode)
    for node in nodesList: #for every node in the list, need to see if what we clicked was an actual node
        nodeData1 = node.strip()
        nodeData2 = nodeData1.split(",")
        #print nodeData2
        xCoord = int(float(nodeData2[1]))
        yCoord = int(float(nodeData2[2]))
        if (abs(x - xCoord) < 10) and (abs(y - yCoord) < 10): #checks if within the size of the node, if it is, turns it green
            circle = drawCircle(xCoord, yCoord, "cyan")
            listN.append((xCoord, yCoord))
            listNC.append(circle)


def refresh(event = None): #write to file, delete the list of neighbours and the blue circles, turn main node yellow
    #print "this is coming here"
    global canvas
    global listN
    global listDone
    global listDoneC
    #print listN
    #print listDone
    #a = len(listDone)
    if len(listDone) >= 1:
        f3 = open("neighbours.txt", "a")
        #if a >= 1:
        #    workingNode = canvas.coords(listDone[a - 1]) #want the node at the last index since that's the one we're working on
        a = listDone[0] #this is a tuple with the x,y coordinates of the main node
        x = a[0]
        y = a[1]
        nodeNum = str(getNode(x,y)) #get back the node number itself

        #f3.write(x + "," + y + ":") #so now we've written the x,y coordinates of the selected node to the file
        f3.write(nodeNum + ":")
        for circle in listN: #for every tuple in the list of neighbours
            xCo = circle[0]
            yCo = circle[1]
            neighNum = str(getNode(xCo, yCo) + ",")
            #f3.write(xCo + "," + yCo + "/") #forward slash indicates the end of a node. Commas between x and y coordinates of each node
            f3.write(neighNum)
        f3.write("\n")
        f3.close() #done writing the relevant information to the file

#now need to reconfigure the lists so we can do the neighbours for the next node
        for node in listNC:
            canvas.delete(node)
        for node in listDoneC:
            canvas.delete(node)
        b = listDone[0] #tuple with x and y
        #print b
        newX = b[0]
        newY = b[1]
        drawCircle(newX, newY, "purple")

        listN = []
        listDone = [] #check this logic later
        listDoneC = []
        #print listN
        #print listDone

def getCoord(event):#bind to single left click
    global count
    #global allNodes
    global f1
    global canvas
    count = count + 1
    #print canvas.canvasy(event.y)
    x = canvas.canvasx(event.x) # need the x and y coordinates relative to the canvas, not just what's within the frame
    y = canvas.canvasy(event.y) # ^^
    #print "y", y
    drawCircle(x, y, "red") #canvas.canvasy(event.y))
    Node = str(count) +"," + str(x) + "," + str(y) + "\n" #each node has a unique number, and x,y coordinates

    f1.write(Node)
    #f.close()
    #print "x", event.x
    #print "y", event.y

listN = [] #save neighbours' coordinates into this - delete each time
listNC = [] #save the nodes that are neighbours - the circles themselves

listDone = [] # save nodes' coordinates (I've done neighbours for these)
listDoneC = []
#listDoneBfr = [] # might not need this list....
#how about a dictionary with the node and its neighbours instead?? no need

wnd = Tkinter.Tk() #creating the main window
wnd.state("zoomed") #the window opens maximised

canvas = Tkinter.Canvas(wnd, bg = "white", width = 500, height = 500, scrollregion=(0,0,1750,2500))

refreshBtn = Tkinter.Button(wnd, text = "refresh", command = refresh)


#this works to make sure the size of the canvas changes as you change the size of the window, but I want some space/an empty column on the left where i will be able to display information
Vscrollbar = Tkinter.Scrollbar(wnd)
Vscrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
canvas.config(yscrollcommand = Vscrollbar.set)
Vscrollbar.config(command=canvas.yview)

Hscrollbar = Tkinter.Scrollbar(wnd, orient=Tkinter.HORIZONTAL)
Hscrollbar.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
canvas.config(xscrollcommand = Hscrollbar.set)
Hscrollbar.config(command=canvas.xview)

refreshBtn.pack()

canvas.pack(fill = Tkinter.BOTH, expand = Tkinter.YES)

photo = Tkinter.PhotoImage(file="map.gif")
canvas.create_image(0, 0, image = photo, anchor = "nw")

canvas.bind("<Button-1>", getCoord)
canvas.bind("<Button-3>", getNeighbours)
canvas.bind("<Button-2>", selectNode)
#canvas.bind("<Return>", refresh)

# drawing nodes already done onto the canvas
f = open("Nodesfile.txt", "r")
info = f.readlines()
# getting the value of the count. Will need to change this code once I start doing neighbours too since then the last line won't be the final node I made, it will be something else, unless I decide to make a completely separate file for the neighbours

if len(info) > 1:
    last = info[len(info)-1] #get what's at the last index - this is the node that was made last
    asList = last.split(",")
    count = int(asList[0])
else:
    count = 0

#print count

node = ""

length = len(info) #length of the list
#print length
if length > 1: #don't want to include nodes heading so want len>1
    for i in range (1,length):
        node = info[i]
        a = node.strip() #removes the "\n"
        b = a.split(",") #now have a list
        #print b[1]
        decimalx = float(b[1])
        x = int(decimalx) #can't directly turn a string that is a decimal into an integer
        decimaly = float(b[2])
        y = int(decimaly)
        drawCircle(x, y, "red") #issue with scrolling here or not? Nope!

f.close()
# done making the nodes that I've made previously

f1 = open("Nodesfile.txt", "a") #open the file a second time, now so that you can append to it

#working with the file to get the nodes already got the neighbours for

f2 = open("neighbours.txt", "r")
data = f2.readlines()
#print data
#print data
if len(data) >= 1:
    for i in data:
        firstN = i.split(":") #first node data ends with :
        #print list(firstN)
        nodeAsStr = firstN[0] #at index 0 of the list created above we now have the info for the first node
        #nodeAsInt = int(nodeAsStr)
        xy = getNodeCoord(nodeAsStr)

        #print list(nodeAsStr)
        #w = nodeAsStr.split(",") #gives us a list

        xOfN = int(float(xy[0]))
        yOfN = int(float(xy[1]))

        drawCircle(xOfN, yOfN, "purple")

f2.close()

wnd.mainloop()

f1.close() #write to the file only when we close the image that we're working on
