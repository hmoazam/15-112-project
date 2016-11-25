#Modification history:
#Date          Start time           End time
#23/11/2016    10.40am              11.10am
#24/11/2016    7.00pm               8.00pm

# This is the file that creates the start window (which contains the instructions for the user). It has a button which allows you to open the map

import Tkinter as tk
import Mapfile as N

def openMap():
    N.run()

main = tk.Tk() #creating the main window
main.state("zoomed") #the window opens maximised
main.title("Find Your Way")
background_image = tk.PhotoImage(file = "bg2.gif") # load background image
background_label = tk.Label(main, image = background_image)
background_label.place(x=0, y=0, relwidth = 1, relheight = 1)
enter = tk.Button(main, text = "Open Map", command = openMap, overrelief = tk.RIDGE, cursor = "hand2", bg = "#ffffcc", padx = 4, pady = 4, font = "Futura 14 bold", borderwidth = 3, activebackground = "black", foreground = "black", activeforeground = "#ffffcc") # open map button

enter.place(relx=0.3, rely=0.92, anchor=tk.CENTER)

main.mainloop()

# images from:
#http://images.mentalfloss.com/sites/default/files/styles/article_640x430/public/istock_000035608838_small.jpg
#https://upload.wikimedia.org/wikipedia/en/thumb/b/bb/Carnegie_Mellon_University_seal.svg/1024px-Carnegie_Mellon_University_seal.svg.png
