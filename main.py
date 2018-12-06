# file: main.py
from playlist import Playlist
from tkinter import *
import subprocess

class Window:
    def __init__(self):
        self.playlist = Playlist()
        self.root = Tk()
        self.root.geometry('200x200')
        self.frame  = Frame(self.root)
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='New', command=self.new)
        self.filemenu.add_command(label='Delete')
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.root.destroy)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.root.config(menu=self.menubar)

    def switchFrame(self):
        self.frame.destroy()
        self.frame = Frame(self.root)
        self.frame.pack()

    def player(self):
        self.switchFrame()
        self.var = StringVar()
        self.values = self.playlist.loadPlaylist()
        self.label = Label(self.frame, text='Select a video:')
        self.label.grid(column=0, row=0)
        self.omenu = OptionMenu(self.frame, self.var, *self.values, command=self.play)
        self.omenu.grid(column=1, row=0)

    def play(self, value):
        self.url = self.playlist.selectPlaylist(value)
        self.cmd = '/usr/bin/mpv --save-position-on-quit'
        #subprocess.call(['/usr/bin/mpv', '--save-position-on-quit', self.url])   

    def new(self):
        self.switchFrame()
        self.lname = Label(self.frame, text='Name')
        self.lname.grid(column=0, row=0)
        self.ename = Entry(self.frame)
        self.ename.grid(column=1, row=0)
        self.lurl = Label(self.frame, text='Url')
        self.lurl.grid(column=0, row=1)
        self.eurl = Entry(self.frame)
        self.eurl.grid(column=1, row=1)
        self.bsave = Button(self.frame, text='Save', command=self.save)
        self.bsave.grid(column=1, row=2)

    def save(self):
        playlist = Playlist(name=self.ename.get(), address=self.eurl.get())
        playlist.savePlaylist()

    def delete(self):
        self.playlist.deletePlaylist(self.var.get())
        




if __name__ == '__main__':
    win = Window()
    win.player()
    mainloop()
