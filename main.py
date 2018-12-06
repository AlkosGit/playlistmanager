# file: main.py
from playlist import Playlist
from tkinter import *
import subprocess

class Window:
    def __init__(self):
        self.playlist = Playlist()
        self.root = Tk()
        self.root.geometry('300x250')
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
        self.omenu = OptionMenu(self.frame, self.var, *self.values)
        self.omenu.config(width=15)
        self.omenu.grid(column=1, row=0, sticky='e', pady=10)
        self.otext = Text(self.frame, width=40, height=10)
        self.otext.delete(1.0, END)
        self.otext.grid(column=0, row=1, columnspan=2)
        self.bclear = Button(self.frame, text='Clear', command=self.player)
        self.bclear.grid(column=0, row=2, sticky='w', pady=10)
        self.bplay = Button(self.frame, text='Play', command=self.play)
        self.bplay.grid(column=1, row=2, sticky='e', pady=10)

    def play(self):
        value = (self.var.get())
        self.url = self.playlist.selectPlaylist(value)
        self.process = subprocess.Popen(['/usr/bin/mpv', '--save-position-on-quit', self.url], stdout=subprocess.PIPE)
        self.listOutput()
        
    def listOutput(self):
        output = self.process.stdout.readline()
        self.otext.insert(END, output)
        self.root.after(100, self.listOutput)

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
        self.bcancel = Button(self.frame, text='Cancel', command=self.player)
        self.bcancel.grid(column=1, row=2, sticky='w')
        self.bsave = Button(self.frame, text='Save', command=self.save)
        self.bsave.grid(column=1, row=2, sticky='e')

    def save(self):
        playlist = Playlist(name=self.ename.get(), address=self.eurl.get())
        playlist.savePlaylist()
        self.player()

    def delete(self):
        self.playlist.deletePlaylist(self.var.get())
        




if __name__ == '__main__':
    win = Window()
    win.player()
    mainloop()
