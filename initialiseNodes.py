#Modification history:
#Date         Start time          End time
#4/11/2016    1.00pm              6.00pm
#5/11/2016    9.00am              12 noon
#5/11/2016    2.00pm              8.00pm
#6/11/2016    6.30pm              8.00pm
#6/11/2016    10.00pm             1.00am
#7/11/2016    10.30am             12.30pm
#7/11/2016    4.00pm              8.00pm
#8/11/2016    3.00pm              7.00pm
#9/11/2016    12 midnight         2.00am
#13/11/2016   4.00pm              6.30pm
#15/11/2016   1.00am              1.33am
#15/11/2016   4.20pm              5.00pm
#15/11/2016   7.18pm              9.30pm

# the code in this file is to create the data which is saved in the Nodesfile and neighbours file

import Tkinter

def getNodeCoord(node):# this function gets the x and y coordinates of each node in the neighbours file (the file only contains node numbers)
    global info # info from the Nodesfile - the x and y coordinates of each node
    impInfo = info[1:] # skip the 'nodes' title
    for j in impInfo:
        allDetails = j.strip() #removing the /n
        List = allDetails.split(",") #now we get a list with the information for each of the nodes
        if List[0] == node:
            xCoord = List[1]
            yCoord = List[2]
            return ((xCoord, yCoord)) #return a tuple with the x,y coordinates of the node

def getNode(x, y): # function that gives the node number, given the x and y coordinates selected
    global info
    nodeInfo = info[1:]
    for i in nodeInfo:
        allDetails = i.strip() #removing the /n
        List = allDetails.split(",") #now we get a list with the information for each of the nodes
        xCoord = int(float(List[1]))
        yCoord = int(float(List[2]))
        if (x == xCoord and y == yCoord): # looking for a match... when it's found, we return the node number itself
            return List[0] #the node number is at index 0 in the list that we just created

def drawCircle(x, y, colour): # function to draw a circle. Different colours mean different things, so pass the colour in as a parameter when calling the function
    global canvas
    c = canvas.create_oval(x-5, y-5, x+5, y+5, fill = colour) # draws a circle of diameter 10, with the center of the circle the coordinates of the node
    return c

def selectNode(event): #select the node that I will be choosing neighbours for. (Middle click)
    global canvas
    global info
    global listDone
    global listDoneC
    x = canvas.canvasx(event.x) # need the x and y coordinates relative to the canvas, not just what's within the frame
    y = canvas.canvasy(event.y)
    nodesList = info[1:]

    for node in nodesList: #for every node in the list, need to see if what we clicked was an actual node
        nodeData1 = node.strip()
        nodeData2 = nodeData1.split(",")
        xCoord = int(float(nodeData2[1]))
        yCoord = int(float(nodeData2[2]))
        if (abs(x - xCoord) < 10) and (abs(y - yCoord) < 10): #checks if within the size of the node (won't always click exactly in the middle), if it is, creates a green circle on top
            circle = drawCircle(xCoord, yCoord, "green")
            listDone.append((xCoord, yCoord)) # add the x and y coordinates to listDone
            listDoneC.append(circle) # add the circle itself to listDoneC (so can later delete all objects in the list when we refresh)

def getNeighbours(event): # select the neighbours of the node selected (green node)
    global canvas
    global info
    global listN
    global listNC
    x = canvas.canvasx(event.x) # need the x and y coordinates relative to the canvas, not just what's within the frame
    y = canvas.canvasy(event.y)
    nodesList = info[1:]
    for node in nodesList: #for every node in the list, need to see if what we clicked was an actual node
        nodeData1 = node.strip()
        nodeData2 = nodeData1.split(",")
        xCoord = int(float(nodeData2[1]))
        yCoord = int(float(nodeData2[2]))
        if (abs(x - xCoord) < 10) and (abs(y - yCoord) < 10): #checks if within the size of the node, if it is, makes a cyan circle on top of it
            circle = drawCircle(xCoord, yCoord, "cyan")
            listN.append((xCoord, yCoord)) # add the x and y coordinates to listN
            listNC.append(circle) # add the circle object itself to listNC

# this writes the information of the neighbours of each node into the neighbours file,  delete the list of neighbours and the cyan circles, turns main node purple
def refresh(event = None):
    global canvas
    global listN
    global listDone
    global listDoneC
    global listNC
    if len(listDone) >= 1:
        f3 = open("neighbours.txt", "a") # open for appending
        a = listDone[0] #this is a tuple with the x,y coordinates of the main node - so when we're done with a node, its saved into here, and a purple circle is drawn to indicate that this node has been done
        x = a[0]
        y = a[1]
        nodeNum = str(getNode(x,y)) #get back the node number itself.

        f3.write(nodeNum + ":") # write the node number of the main node (followed by :)
        for circle in listN: #for every tuple in the list of neighbours... get the x and y coordinates
            xCo = circle[0]
            yCo = circle[1]
            neighNum = str(getNode(xCo, yCo) + ",")
            f3.write(neighNum) # write the node numbers of the neighbours (followed by ,)
        f3.write("\n") # after done all the neighbours,
        f3.close() #done writing the relevant information to the file, so close it

# delete the circles that we've drawn
        for node in listNC:
            canvas.delete(node)
        for node in listDoneC:
            canvas.delete(node)

# make a purple circle so that we know that we've done the neighbours for this node
        b = listDone[0] #tuple with x and y coordinates of the node that we were working on
        newX = b[0]
        newY = b[1]
        drawCircle(newX, newY, "purple")

#now need to reconfigure the lists so we can do the neighbours for the next node
        listN = []
        listDone = []
        listDoneC = []
        listNC = []

def getCoord(event):#bind to single left click
    global count
    global f1
    global canvas
    count = count + 1
    x = canvas.canvasx(event.x) # need the x and y coordinates relative to the canvas, not just what's within the frame
    y = canvas.canvasy(event.y) # ^^
    drawCircle(x, y, "red") #canvas.canvasy(event.y))
    Node = str(count) +"," + str(x) + "," + str(y) + "\n" #each node has a unique number, and x,y coordinates

    f1.write(Node)

listN = [] #save neighbours' coordinates into this - delete each time
listNC = [] #save the nodes that are neighbours - the circle objects themselves saved, so then can delete them

listDone = [] # save nodes' coordinates when I've done the neighbours for them
listDoneC = [] # saves the circle objects themselves so then can delete


wnd = Tkinter.Tk() #creating the main window
wnd.state("zoomed") #the window opens maximised

canvas = Tkinter.Canvas(wnd, bg = "white", width = 500, height = 500, scrollregion = (0,0,1750,2500))

refreshBtn = Tkinter.Button(wnd, text = "refresh", command = refresh)

#setting up the canvas with the map (same as in the main code file)
Vscrollbar = Tkinter.Scrollbar(wnd)
Vscrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
canvas.config(yscrollcommand = Vscrollbar.set)
Vscrollbar.config(command=canvas.yview)

Hscrollbar = Tkinter.Scrollbar(wnd, orient=Tkinter.HORIZONTAL)
Hscrollbar.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
canvas.config(xscrollcommand = Hscrollbar.set)
Hscrollbar.config(command=canvas.xview)

refreshBtn.pack() # button that allows me to refresh each time I've done initialising the neighbours for a specific node

canvas.pack(fill = Tkinter.BOTH, expand = Tkinter.YES)

photo = Tkinter.PhotoImage(file = "map.gif")
canvas.create_image(0, 0, image = photo, anchor = "nw")

canvas.bind("<Button-1>", getCoord) # left click to create a node
canvas.bind("<Button-3>", getNeighbours) # right click to select the neighbours
canvas.bind("<Button-2>", selectNode) # middle click to select the node that I will be selecting neighbours for

f = open("Nodesfile.txt", "r")
info = f.readlines()
# getting the value of the count. This is the same as the node number of the last node in the text file
if len(info) > 1:
    last = info[len(info)-1] #get what's at the last index - this is the node that was made last
    asList = last.split(",")
    count = int(asList[0]) # the node number is at index 0
else:
    count = 0 # if the file is empty

node = ""

length = len(info) #length of the list
if length > 1: #don't want to include nodes heading so want len > 1
    for i in range (1,length):
        node = info[i]
        a = node.strip() #removes the "\n"
        b = a.split(",") #now have a list
        decimalx = float(b[1])
        x = int(decimalx) #can't directly turn a string that is a decimal into an integer. So do float, then int
        decimaly = float(b[2])
        y = int(decimaly)
        drawCircle(x, y, "red") #create a red circle for every node in the Nodesfile
f.close()
# done making circles for the nodes that I've made previously

f1 = open("Nodesfile.txt", "a") #open the file a second time, now so that you can append to it (if we add new nodes)

# working with the file to get the nodes for which neighbours already selected
# make a purple circle if the node in question's neigbours have been selected, i.e. if the node number is in the neighbours file
f2 = open("neighbours.txt", "r")
data = f2.readlines()
if len(data) >= 1:
    for i in data:
        firstN = i.split(":") #first node data ends with :
        nodeAsStr = firstN[0] #at index 0 of the list created above we now have the info for the first node
        xy = getNodeCoord(nodeAsStr) # the getNodeCoord returns the x and y coordinates of the node
        xOfN = int(float(xy[0]))
        yOfN = int(float(xy[1]))
        drawCircle(xOfN, yOfN, "purple")
f2.close()

wnd.mainloop()

f1.close() #close the file only when we close the window (exit the mainloop)
