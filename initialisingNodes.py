import Tkinter
import networkx as nx

file1 = open("Nodesfile.txt", "a") #open file for appending so doesn't delete old contents
#file1.write("hi")
#global allNodes
#global Nodesfile
count = 0

#def closeFile():
#    global file1
#    file1.close()

def drawCircle(x, y):
    global canvas
    canvas.create_oval(x, y, x+10, y+10, fill = "red")


def getCoord(event):#bind to double clicked
    global count
    #global allNodes
    global file1
    count = count+1
    #print "x", event.x
    x = event.x
    y = event.y
    #print "y", event.y
    drawCircle(x, y)
    Node = str(count) +"," + str(x) + "," + str(y) + "\n"
    #a = "testing"
    #nodesFile.write("hello")
    file1.write(Node) #this doesn't work either
    #file1.close()
    #print "x", event.x
    #print "y", event.y


wnd = Tkinter.Tk() #creating the main window
wnd.state("zoomed") #the window opens maximised

canvas = Tkinter.Canvas(wnd, bg = "white", width = 1750, height = 2500, scrollregion=(0,0,1750,2500))

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

#canvas.bind("<Button-3>",closeFile)

wnd.mainloop()

file1.write(count)
file1.close()
