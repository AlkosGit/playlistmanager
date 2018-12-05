# file: main.py
from playlist import Playlist
from tkinter import *

p=Playlist()
root = Tk()
root.geometry('200x200')
f = Frame(root)
f.pack()
var = StringVar()
values = p.loadPlaylist()
omenu = OptionMenu(f, var, *values)
omenu.pack()
mainloop()
