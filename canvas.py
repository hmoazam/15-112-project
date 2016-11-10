import Tkinter
#import networkx as nx

#f = open("Nodesfile.txt", "a+") # a+ means can append and read open file for appending so doesn't delete old contents
#f.write("hi")
#global allNodes
#global Nodesfile

def drawCircle(x, y, colour):
    global canvas
    canvas.create_oval(x-5, y-5, x+5, y+5, fill = colour) #should draw a circle of diameter 10, with the center of the circle the coordinates of the node

def selectNode(x, y):
    neighbours = open("neighbours.txt", "a") #open the file when the button is clicked. When do I close it then?? Want to close it every time I'm done with a specific node
    global canvas
    global info
    x = canvas.canvasx(event.x) # need the x and y coordinates relative to the canvas, not just what's within the frame
    y = canvas.canvasy(event.y)
    for node in info: #for every node in the list, need to see if what we clicked was an actual node
        xCoord = int(float(node[1]))
        yCoord = int(float(node[2]))
        if (abs(x - xCoord) < 10) and (abs(y - yCoord) < 10): #checks if within the size of the node, if it is, turns it green
            drawCircle(xCoord, yCoord, "green")



def getNeighbours(x, y):
    global canvas
    global info
    x = canvas.canvasx(event.x) # need the x and y coordinates relative to the canvas, not just what's within the frame
    y = canvas.canvasy(event.y)
    for node in info:
        xCoord = int(float(node[1]))
        yCoord = int(float(node[2]))


def getCoord(event):#bind to double clicked
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

    f1.write(Node) #this doesn't work either
    #f.close()
    #print "x", event.x
    #print "y", event.y


wnd = Tkinter.Tk() #creating the main window
wnd.state("zoomed") #the window opens maximised

canvas = Tkinter.Canvas(wnd, bg = "white", width = 500, height = 500, scrollregion=(0,0,1750,2500))

randButn = Tkinter.Button(wnd, text = "testing")


#this works to make sure the size of the canvas changes as you change the size of the window, but I want some space/an empty column on the left where i will be able to display information
Vscrollbar = Tkinter.Scrollbar(wnd)
Vscrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
canvas.config(yscrollcommand = Vscrollbar.set)
Vscrollbar.config(command=canvas.yview)

Hscrollbar = Tkinter.Scrollbar(wnd, orient=Tkinter.HORIZONTAL)
Hscrollbar.pack(side=Tkinter.BOTTOM, fill=Tkinter.X)
canvas.config(xscrollcommand = Hscrollbar.set)
Hscrollbar.config(command=canvas.xview)

randButn.pack()

canvas.pack(fill = Tkinter.BOTH, expand = Tkinter.YES)

photo = Tkinter.PhotoImage(file="map.gif")
canvas.create_image(0, 0, image = photo, anchor = "nw")

canvas.bind("<Button-1>", getCoord)
canvas.bind("<Double-Button-1>", selectNode)
canvas.bind("Button-3", getNeighbours)

f = open("Nodesfile.txt", "r")
info = f.readlines()
# getting the value of the count. Will need to change this code once I start doing neighbours too
# since then the last line won't be the final node I made, it will be something else, unless I decide to make a completely separate file for the neighbours

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
if len(info) > 1: #don't want to include nodes heading so want len>1
    for i in range (1,len(info)):
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

#count = 0

#def closeFile():
#    global f
#    f.close()

wnd.mainloop()

f1.close() #write to the file only when we close the image that we're working on
