# file: playlistmanager/main.py
from playlist import Playlist
from tkinter import *
import subprocess

class Window:
    def __init__(self):
        self.playlist = Playlist()
        self.root = Tk()
        self.root.geometry('520x250')
        self.root.title('Playlist Manager')
        self.frame  = Frame(self.root)
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='New', command=self.new)
        self.filemenu.add_command(label='Delete', command=self.delete)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.root.destroy)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.root.config(menu=self.menubar)

    def switchFrame(self):
        self.frame.destroy()
        self.frame = Frame(self.root)
        self.frame.pack(fill=BOTH, expand=True)

    def player(self):
        self.switchFrame()
        self.var = StringVar()
        self.values = self.playlist.loadPlaylist()
        if not self.values:
            self.values = ['---',]
        self.label = Label(self.frame, text='Select a playlist:')
        self.label.grid(column=0, row=0)
        self.omenu = OptionMenu(self.frame, self.var, *self.values, command=self.insertDescription)
        self.omenu.config(width=30)
        self.omenu.grid(column=1, row=0, sticky='w', pady=10)
        self.otext = Text(self.frame, width=70, height=10)
        self.otext.delete(1.0, END)
        self.otext.grid(column=0, row=1, columnspan=2, padx=10)
        self.bclear = Button(self.frame, text='Clear', command=self.player)
        self.bclear.grid(column=0, row=2, sticky='w', pady=10, padx=10)
        self.bplay = Button(self.frame, text='Play', command=self.play)
        self.bplay.grid(column=1, row=2, sticky='e', pady=10, padx=10)

    def insertDescription(self, value):
        description = self.playlist.loadDescription(value)
        self.otext.delete(1.0, END)
        self.otext.insert(END, description)

    def play(self):
        value = (self.var.get())
        self.url = self.playlist.selectPlaylist(value)
        self.process = subprocess.Popen(['/usr/bin/mpv', '--save-position-on-quit', self.url], stdout=subprocess.PIPE)
        self.listOutput()
        
    def listOutput(self): #  print output of cmd to textfield
        output = self.process.stdout.readline()
        self.otext.insert(END, output)
        self.root.after(100, self.listOutput)

    def new(self):
        self.switchFrame()
        self.lname = Label(self.frame, text='Name')
        self.lname.grid(column=0, row=0, padx=10, pady=5, sticky='w')
        self.ename = Entry(self.frame)
        self.ename.grid(column=1, row=0, sticky='w')
        self.lurl = Label(self.frame, text='Url')
        self.lurl.grid(column=0, row=1, padx=10, sticky='w')
        self.eurl = Entry(self.frame)
        self.eurl.grid(column=1, row=1, sticky='w')
        self.ldesc = Label(self.frame, text='Description')
        self.ldesc.grid(column=0, row=2, sticky='n', padx=10, pady=5)
        self.tdesc = Text(self.frame, width=55, height=10)
        self.tdesc.grid(column=1, row=2, pady=5)
        self.bcancel = Button(self.frame, text='Cancel', command=self.player)
        self.bcancel.grid(column=1, row=3, sticky='w', pady=5)
        self.bsave = Button(self.frame, text='Save', command=self.save)
        self.bsave.grid(column=1, row=3, sticky='e', pady=5)

    def save(self):
        playlist = Playlist(name=self.ename.get(), address=self.eurl.get(), description=self.tdesc.get(1.0, END))
        playlist.savePlaylist()
        self.player()

    def delete(self):
        self.switchFrame()
        self.var = StringVar()
        self.values = self.playlist.loadPlaylist()
        self.lname = Label(self.frame, text='Name')
        self.lname.grid(column=0, row=0, padx=10, pady=10)
        self.omenu = OptionMenu(self.frame, self.var, *self.values)
        self.omenu.config(width='30')
        self.omenu.grid(column=1, row=0)
        self.bcancel = Button(self.frame, text='Cancel', command=self.player)
        self.bcancel.grid(column=1, row=1, sticky='w')
        self.bdelete = Button(self.frame, text='Delete', command=self.deleteRecord)
        self.bdelete.grid(column=1, row=1, sticky='e')
        
    def deleteRecord(self):
        self.playlist.deletePlaylist(self.var.get())
        self.player()
        
if __name__ == '__main__':
    win = Window()
    win.player()
    mainloop()
