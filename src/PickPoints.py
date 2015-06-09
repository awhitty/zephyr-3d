from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image
from PIL import ImageOps
import ImageTk
import cv2, numpy as np
import argparse as ap

name= ''
f = None
# If the image is too large (doesn't fit on single screen), scale is used to unify point coordinates
scale = 2

# This script allows for simulation of car data to be used as center points in 
# later scripts. Pulls up an image and allows user to click where the car was
# and stores the points in order.
if __name__ == "__main__":
    root = Tk()
    parser = ap.ArgumentParser()
    parser.add_argument('im')
    parser.add_argument('name')

    args = parser.parse_args()

    global name 
    name = args.name
    global f
    f = open(name + 'CenterPoints.txt','w')
    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    #adding the image
    img = Image.open(args.im) 
    img = img.resize((int(img.size[0]/scale),int(img.size[1]/scale)), Image.ANTIALIAS)
    #img = ImageOps.mirror(img).transpose(2)
    img = ImageTk.PhotoImage(img)
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    #function to be called when mouse is clicked
    def printcoords(event):
        #outputting x and y coords to console
        f.write(str(int(event.x*scale))+"\t"+str(int(event.y*scale)) + "\t 0" + "\n")
    #mouseclick event
    canvas.bind("<Button 1>",printcoords)

    root.mainloop()