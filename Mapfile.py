#Modification history:
#Date          Start time           End time
#11/11/2016    3.00pm               5.30pm
#21/11/2016    8.30pm               1.20am
#22/11/2016    12.40pm              1.30pm
#22/11/2016    3.10pm               7.00pm
#22/11/2016    9.00pm               1.00am
#23/11/2016    11.10am              1.05pm
#23/11/2016    7.00pm               11.00pm
#24/11/2016    12.01am              3.18am
#24/11/2016    8.00pm               10.00pm
#25/11/2016    4.00pm               11.00pm
#26/11/2016    12.15am              12.59am

import Tkinter
import makeGraph as mG
import math

def errorMsg(message): # function to create the error message box if anything incorrect is done
    dialog = Tkinter.Tk()
    dialog.geometry("500x100")
    dialog.title("Error")
    dialog.configure(bg = "black")
    text = Tkinter.Label(dialog, text = message, font = "Calibri 11", foreground = "white", background = "black") #the error message is passes in as a parameter when this function is called
    text.pack()
    space = Tkinter.Label(dialog, text = '', background = "black") #just to space out
    space.pack()
    okButn = Tkinter.Button(dialog, text = "New Path", command = dialog.destroy, bg = "#cc2900", cursor = "hand2", padx = 4, pady = 4, font = "Futura 12 bold", activebackground = "white", foreground = "white", activeforeground = "red")
    okButn.pack()
    dialog.mainloop()

# lineInfo contains a list of the x and y coordinates of the nodes used to construct the line. The getDist function calculates the sum of the Euclidean distances between each adjacent node and returns it in metres
# structure of the list is [x1,y1,x2,y2,x3,y3 ....], and straight lines are made between each adjacent node, so can use recursion to find the length of each line made (in pixels), then convert that to metres
# recursive function that calculates the total length (in pixels) of the lines made
def getDist(lineInfo):
    if len(lineInfo) == 2:
        return 0
    else:
        x1 = lineInfo[0] # the x coordinate of the first node in the list
        y1 = lineInfo[1] # the y coordinate of the first node in the list
        x2 = lineInfo[2] # the x coordinate of the second node in the list
        y2 = lineInfo[3] # the y coordinate of the second node in the list
        dist = math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2)) #gets Euclidean distance between two consecutive nodes
        return dist + getDist(lineInfo[2:])

def getTime(lineInfo): # gets the approximate time taken to reach the destination as well as the distance in metres
    pix = getDist(lineInfo) #distance in pixels
    dist = int(pix/10) #scale is 1m = 10 pixels
    time = dist/1.4 #avg walking speed is 1.4 m/s. Use this to get time
    mins = int(time/60) #split the time into minutes...
    seconds = int(time%60) #...and seconds
    return [mins, seconds, dist] #return this so that we can then put this into the entry boxes

def newPath(): # function to 'refresh' so you can construct another path
    global toDelete # list of canvas objects to be deleted
    global canvas
    global timeBox
    global distBox
    global end
    global start # get rid of at the end
    global startClick
    global endClick
    global node1
    node1 = ""
# reset the count variables endClick and startClick to 0 when we want to make a new path
    endClick = 0
    startClick = 0
    if len(toDelete) >= 1: #making sure there are some objects on the canvas to be deleted
        for c in toDelete:
            canvas.delete(c)
        start = -1 #default values
        end = -1
#delete the text in the text-boxes
        timeBox.delete("1.0", Tkinter.END)
        distBox.delete("1.0", Tkinter.END)
        toDelete = [] #reset toDelete to an empty list for the next path

def drawPath(): #function that draws the shortest path on the map
    global start
    global end
    global canvas
    global toDelete
    global distBox
    global timeBox
    forLine = [] #an empty list in which to save the nodes that will be used to create the line
    f1 = open("Nodesfile.txt", "r")
    a = f1.readlines() #a is a list of the data in the Nodesfile
    data = a[1:] # the first item in the list is the title 'nodes', so the relevant data is at index 1 onwards
    nodes = mG.getPath(start, end) #list of the nodes visited. getPath is a function in the makeGraph file which returns the nodes visited (in the shortest path)
    for node in nodes: # we need to get the x and y coordinates of each of the nodes visited
        for i in data: # need to match it to the nodes we have in the list called data (loaded from text file)
            clean = i.strip() #remove \n
            List = clean.split(",") # creates a list
            if int(List[0]) == node: # matching the node to the nodes in the list, and getting its x and y coordinates
                x = int(float(List[1]))
                y = int(float(List[2]))
                # then put the x and y coordinates of the node into a list
                forLine.append(x)
                forLine.append(y)
    line = canvas.create_line(forLine, fill = "blue", arrow=Tkinter.LAST, width = 3) # draw the line with an arrow head pointing at the destination
    getInfo = getTime(forLine) # helper function which returns back the time taken and distance travelled
    mins = str(getInfo[0])
    seconds = str(getInfo[1])
    distance = str(getInfo[2])
    #insert the travel information calculated above into the relevant boxes
    distBox.insert(Tkinter.END, distance + "m")
    timeBox.insert(Tkinter.END, mins + " mins " + seconds + " s")
    toDelete.append(line) # put the line object into the list of things to be deleted upon refreshing

def drawCircle(x, y, colour): # function to draw a circle (duh)
    global canvas
    c = canvas.create_oval(x-5, y-5, x+5, y+5, fill = colour) # draws a circle of diameter 10, with the center of the circle the coordinates of the node
    return c

def begin(N): # this function is when the person uses the drop down menu to select their starting position. N is the node number of the room selected
    global start
    global node1
    node1 = N # this is to be used to check whether someone clicks on the same node for the start and end (error message will be generated)
    global info # data from the nodes file
    global canvas
    global toDelete
    global startClick
    nodeInfo = info[1:] # because at index 1 is the title 'nodes'
    for item in nodeInfo:
        nodeData1 = item.strip() #removing the /n
        nodeData2 = nodeData1.split(",") #now we get a list with the coordinate information for each of the nodes
        if N == nodeData2[0]:
            xCoord = int(float(nodeData2[1]))
            yCoord = int(float(nodeData2[2]))
            c = drawCircle(xCoord, yCoord, "green") # create a green circle at the starting point
            start = int(nodeData2[0]) #the node number of the starting node is at index 0 in the list that we just created
            toDelete.append(c)
    startClick = startClick + 1
    if startClick == 2: # user should only select one starting point, so this will create an error message
        newPath() # it will also reset the screen so the user can make a new path
        errorMsg("Please select one starting point")

def dest(N): # similarly, this function is for when the user uses the drop down menu to select their destination
    global end
    global startClick
    global endClick
    global info # data from the nodes file
    global canvas
    global toDelete

    if startClick != 1: # this checks to see if a starting point has been selected before the destination. If it hasn't, then that creates an error message
        errorMsg("Please select the starting point before the destination!")
        return # return to make sure the following code isn't executed in an error case

    if N == node1: # if the user chooses the destination to be the same as their starting point, that would be incorrect, so creates an error message
        newPath() # it also resets the screen so the user can start over
        errorMsg("Why would you want to go to where you already are?")
        return # return since if no start point has been selected, the following code would cause an error if executed

    nodeInfo = info[1:]
    for item in nodeInfo: #looping through all the nodes in the list
        nodeData1 = item.strip() #removing the /n
        nodeData2 = nodeData1.split(",") #now we get a list with the coordinate information for each of the nodes
        if N == nodeData2[0]: # when we find a match, we need to get the x and y coordinates of that node, and draw a cyan circle at that location
            xCoord = int(float(nodeData2[1]))
            yCoord = int(float(nodeData2[2]))
            c = drawCircle(xCoord, yCoord, "cyan")
            end = int(nodeData2[0]) #the node number is at index 0 in the list that we just created
            toDelete.append(c) # add the circle to the things that need to be deleted
            drawPath()
    endClick = endClick + 1 # counting the number of times a destination has been chosen
    if endClick == 2: # if two destinations picked then generate an error message and reset the canvas (newPath)
        newPath()
        errorMsg("Please select one destination!")

# function that will find the node closest to the place selected on the map (from the ones I've initialised) and draw a cyan circle on it (for the end point, bound to right click)
def getNode2(event):
    global end
    global node1 # this is to see if a start node has been selected
    global info # data from the nodes file
    global canvas
    global toDelete
    global endClick
    global startClick

    if startClick != 1: # checking to make sure that a start point has actually been selected before the destination
        errorMsg("Please select the starting point before the destination!")
        return

    diff = [] # initialise the list of differences
    nodeInfo = info[1:] # again, just getting rid of 'node' at the start of the list
    x = canvas.canvasx(event.x) # need the x and y coordinates of where the user clicked relative to the canvas, not just what's within the frame
    y = canvas.canvasy(event.y)
    for node in nodeInfo:
        nodeData1 = node.strip() # removing the /n
        nodeData2 = nodeData1.split(",") # now we get a list with the information for each of the nodes
        nodeNum = nodeData2[0]
        xCoord = int(float(nodeData2[1]))
        yCoord = int(float(nodeData2[2]))
        # need to have a list with the difference in x and y coordinates for where the user clicked and all the nodes' x,y coordinates to find the closest
        absDiff = (abs(xCoord-x)) + (abs(yCoord-y)) #get the differences between the x and y coordinates of each node. Sum them, and add this to the list
        diff.append((nodeNum, absDiff)) # have a list of tuples

    tup = diff[0] # accessing the first tuple
    minD = tup[1] # initialise min difference as that for the first node
    minN = tup[0] # the node number of the node associated with minD

    for i in diff[1:]: # loop through the rest of the differences, find the smallest one
        n = i[0] # the node number
        d = i[1] # the difference
        if d < minD: # if find a difference smaller than what the minimum difference is, update minD and minN accordingly
            minD = d # the difference
            minN = n # the node number of the closest node

    for item in nodeInfo:
        nodeData1 = item.strip() # removing the /n from the end of each item in the list
        nodeData2 = nodeData1.split(",") # now we get a list with the information for each of the nodes
        nodeNum = nodeData2[0]

        if nodeNum == minN: # if the node number matches that of the closest difference
            if node1 == nodeNum: # if someone selects the same destination as their starting point this generates an error message
                newPath()
                errorMsg("Why would you want to go to where you already are?")
                return
            # otherwise ...
            closeX = int(float(nodeData2[1])) # the node's x coordinate
            closeY = int(float(nodeData2[2])) # the node's y coordinate
            c = drawCircle(closeX, closeY, "cyan") # draw a cyan circle at those coordinates
            end = int(nodeData2[0]) #the node number is at index 0 in the list that we just created
            toDelete.append(c) # put the circle into the list of objects to be deleted
            drawPath()

    endClick = endClick + 1 # increment endClick by 1, to check that someone doesn't select two end locations at one time

    if endClick == 2: # if two destinations selected, then this creates an error message
        newPath()
        errorMsg("Please select one destination!")

# function will find the node closest to the place selected on the map (from the ones I've initialised) and draw a green circle on it (for the starting point, bound to left click)
def getNode1(event): #
    global start
    global info # data from the nodes file
    global canvas
    global toDelete
    global node1
    global startClick

    diff = [] # same as for getting the destination, we first initialise an empty list in which we can save the distances to all the nodes from the point that we clicked
    nodeInfo = info[1:]

    x = canvas.canvasx(event.x) # need the x and y coordinates relative to the canvas, not just what's within the frame
    y = canvas.canvasy(event.y)
    for node in nodeInfo:
        nodeData1 = node.strip() #removing the /n
        nodeData2 = nodeData1.split(",") #now we get a list with the information for each of the nodes
        nodeNum = nodeData2[0]
        xCoord = int(float(nodeData2[1]))
        yCoord = int(float(nodeData2[2]))
    # have the list with the difference in x and y coordinates for where the user clicked and all the nodes' x,y coordinates to find the closest
        absDiff = (abs(xCoord-x)) + (abs(yCoord-y))
        diff.append((nodeNum, absDiff)) # save in a tuple
    # (this is exactly the same as what I did for clicking to select the destination)
    tup = diff[0]
    minD = tup[1] # initialise min difference as the first difference
    minN = tup[0] # initialise the min node as the first one
    for i in diff[1:]: # loop through the rest of the differences, find the smallest one
        n = i[0]
        d = i[1] # difference
        if d < minD:
            minD = d
            minN = n # have the node number of the closest node
    for item in nodeInfo:
        nodeData1 = item.strip() # removing the /n
        nodeData2 = nodeData1.split(",") # now we get a list with the information for each of the nodes
        nodeNum = nodeData2[0]
        if nodeNum == minN:
            node1 = nodeNum # setting the node1 to this node value - this is so later we can check the user hasn't selected the same destination as their start point
            closeX = int(float(nodeData2[1]))
            closeY = int(float(nodeData2[2]))
            c = drawCircle(closeX, closeY, "green")
            start = int(nodeData2[0]) #the node number of the start node is at index 0 in the list that we just created
            toDelete.append(c) # save the circle in the list of things to be deleted
    startClick = startClick + 1 # increment startClick by 1 - so we can check only one start position has been selected
    if startClick == 2: # if two start points selected, create error message and clear objects on the map
        newPath()
        errorMsg("Please select one starting point")

# initialising global variables (later assigned to objects/widgets)
canvas = ""
timeBox = ""
distBox = ""

# global variables (counters) that keep track of whether a start node or end node has been selected by the user - these are to prevent the program crashing, creating error messages if the user does anything incorrectly
startClick = 0
endClick = 0

f = open("Nodesfile.txt", "r")
info = f.readlines() # all the data saved in a list
f.close()

toDelete = [] # global list because needed in multiple functions

def run(): # function called when 'open map' button pressed in start.py. Sets up tkinter window with the canvas, map etc.
    global canvas
    global timeBox
    global distBox
    global wnd

    wnd = Tkinter.Toplevel() #creating the main window
    wnd.state("zoomed") #the window opens maximised
    wnd.title("CMUQ Ground Floor")

    background_image = Tkinter.PhotoImage(file = "tartan.gif") # load background image
    background_label = Tkinter.Label(wnd, image = background_image)
    background_label.place(x=0, y=0, relwidth = 1, relheight = 1)

    canvas = Tkinter.Canvas(wnd, bg = "white", width = 500, height = 500, scrollregion = (0,0,1750,2500)) # this makes sure the size of the canvas changes as you change the size of the window
    Vscrollbar = Tkinter.Scrollbar(wnd) # creating the vertical scroll bar
    Vscrollbar.pack(side = Tkinter.RIGHT, fill = Tkinter.Y)
    canvas.config(yscrollcommand = Vscrollbar.set)
    Vscrollbar.config(command = canvas.yview)

    Hscrollbar = Tkinter.Scrollbar(wnd, orient = Tkinter.HORIZONTAL) # creating the horizontal scroll bar
    Hscrollbar.pack(side = Tkinter.BOTTOM, fill = Tkinter.X)
    canvas.config(xscrollcommand = Hscrollbar.set)
    Hscrollbar.config(command = canvas.xview)

# create the text boxes that will contain the distance and time of travel
    title1 = Tkinter.Label(wnd, text = "Distance", font = ("Futura", "11", "bold"), foreground = "white", background = "black")
    title1.pack()
    distBox = Tkinter.Text(wnd, width = 15, height = 1)
    distBox.pack()

    title2 = Tkinter.Label(wnd, text = "Time Taken", font = ("Futura", "11", "bold"), foreground = "white", background = "black")
    title2.pack()
    timeBox = Tkinter.Text(wnd, width = 15, height = 1)
    timeBox.pack()

    title3 = Tkinter.Label(wnd, text = " ", background = "black") # just making an extra line with no text to space out the button from the text boxes
    title3.pack()

    newPathBtn = Tkinter.Button(wnd, text = "New Path", command = newPath, bg = "#cc2900", overrelief = Tkinter.RIDGE, cursor = "hand2", font = "Futura 12 bold", padx = 3, pady = 3, activebackground = "white", foreground = "white", activeforeground = "red")
    newPathBtn.pack() # the newPath button

    canvas.pack(fill = Tkinter.BOTH, expand = Tkinter.YES) # so the canvas fills the entire screen

    photo = Tkinter.PhotoImage(file="wLabels.gif") # loading the image of the map onto the canvas
    canvas.create_image(0, 0, image = photo, anchor = "nw")

# binding the left and right mouse-clicks to getting the start node and destination node, respectively
    canvas.bind("<Button-1>", getNode1)
    canvas.bind("<Button-3>", getNode2)

# creating the drop down menu
    menubar = Tkinter.Menu(wnd)
    subMenu1 = Tkinter.Menu(menubar, background = "black", foreground = "white", activebackground = "red")
    subMenu2 = Tkinter.Menu(menubar, background = "black", foreground = "white", activebackground = "red")
    menubar.add_cascade(label = "Start", menu = subMenu1)
    menubar.add_cascade(label = "Destination", menu = subMenu2)

    rooms = open("rooms.txt", "r")
    r = rooms.readlines() # list containing room numbers associated with node numbers

# the following two for loops add the room numbers to the drop down menus for the start and destination. When a certain room number is selected, its node number (N) is passed in, and this is then used by the relevant functions
    for i in r:
        info1 = i.strip()
        info2 = info1.split(",")
        room = info2[1]
        N = info2[0]
        subMenu1.add_command(label = room, command = lambda x = N: begin(x))

    for j in r:
        info1 = j.strip()
        info2 = info1.split(",")
        room = info2[1]
        N = info2[0]
        subMenu2.add_command(label = room, command = lambda x = N: dest(x))

    rooms.close()

    wnd.config(menu = menubar)
    wnd.mainloop()

# image from http://cdn.wallpapersafari.com/53/97/XW0wcr.jpg
# map from CMU facilities
