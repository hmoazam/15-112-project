#Modification history:
#Date          Start time           End time
#11/11/2016    3.00pm               5.30pm

import Tkinter
import makeGraph as mG

def newPath():
    global toDelete
    global canvas
    if len(toDelete)>=1:
        for c in toDelete:
            canvas.delete(c)
        start = -1 #default values
        end = -1

def drawPath():
    global start
    global end
    global canvas
    global toDelete
    forLine = []
    f1 = open("Nodesfile.txt", "r")
    a = f1.readlines()
    data = a[1:]
    #print data
    nodes = mG.getPath(start, end) #list of the nodes visite
    for node in nodes:
        for i in data:
            clean = i.strip() #remove \n
            List = clean.split(",")
            if int(List[0]) == node:
                x = int(float(List[1]))
                y = int(float(List[2]))
                forLine.append(x)
                forLine.append(y)
    line = canvas.create_line(forLine, fill = "black", arrow=Tkinter.LAST, width = 3) #smooth or not?
    toDelete.append(line)


def drawCircle(x, y, colour):
    global canvas
    c = canvas.create_oval(x-5, y-5, x+5, y+5, fill = colour) #should draw a circle of diameter 10, with the center of the circle the coordinates of the node
    return c #will this work to save the circle itself in the list??



def getNode2(event):
    global end
    end = -1
    global info # data from the nodes file
    global canvas
    global toDelete
    nodeInfo = info[1:]
    x = canvas.canvasx(event.x) # need the x and y coordinates relative to the canvas, not just what's within the frame
    y = canvas.canvasy(event.y)
    for node in nodeInfo:
        nodeData1 = node.strip() #removing the /n
        nodeData2 = nodeData1.split(",") #now we get a list with the information for each of the nodes
        xCoord = int(float(nodeData2[1]))
        yCoord = int(float(nodeData2[2]))
        if (abs(x - xCoord) < 10) and (abs(y - yCoord) < 10):
            c = drawCircle(xCoord, yCoord, "yellow")
            end = int(nodeData2[0]) #the node number is at index 0 in the list that we just created
            toDelete.append(c)
            drawPath()


def getNode1(event): # note this is different to the function made in the setup file
    global start
    start = -1
    global info # data from the nodes file
    global canvas
    global toDelete
    nodeInfo = info[1:]
    x = canvas.canvasx(event.x) # need the x and y coordinates relative to the canvas, not just what's within the frame
    y = canvas.canvasy(event.y)
    for node in nodeInfo:
        nodeData1 = node.strip() #removing the /n
        nodeData2 = nodeData1.split(",") #now we get a list with the information for each of the nodes
        xCoord = int(float(nodeData2[1]))
        yCoord = int(float(nodeData2[2]))
        if (abs(x - xCoord) < 10) and (abs(y - yCoord) < 10):
            c = drawCircle(xCoord, yCoord, "green")
            start = int(nodeData2[0]) #the node number is at index 0 in the list that we just created
            toDelete.append(c)


wnd = Tkinter.Tk() #creating the main window
wnd.state("zoomed") #the window opens maximised

canvas = Tkinter.Canvas(wnd, bg = "white", width = 500, height = 500, scrollregion=(0,0,1750,2500))

#this works to make sure the size of the canvas changes as you change the size of the window, but I want some space/an empty column on the left where i will be able to display information
Vscrollbar = Tkinter.Scrollbar(wnd)
Vscrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
canvas.config(yscrollcommand = Vscrollbar.set)
Vscrollbar.config(command=canvas.yview)

Hscrollbar = Tkinter.Scrollbar(wnd, orient=Tkinter.HORIZONTAL)
Hscrollbar.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
canvas.config(xscrollcommand = Hscrollbar.set)
Hscrollbar.config(command=canvas.xview)

newPathBtn = Tkinter.Button(wnd, text = "New Path", command = newPath)

newPathBtn.pack()

canvas.pack(fill = Tkinter.BOTH, expand = Tkinter.YES)

photo = Tkinter.PhotoImage(file="map.gif")
canvas.create_image(0, 0, image = photo, anchor = "nw")

def hello():
    print "hi"

menubar = Tkinter.Menu(wnd)
#menubar.pack()
menubar.add_command(label="Start")# command=hello)
menubar.add_command(label ="Destination")

wnd.config(menu=menubar)

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

toDelete = []

#constructing the actual path

canvas.bind("<Button-1>", getNode1)
canvas.bind("<Button-3>", getNode2)

wnd.mainloop()
