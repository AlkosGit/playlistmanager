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
        self.frame = Frame(self.root)
        self.topframe = Frame(self.root)
        self.newframe = Frame(self.root)
        self.delframe = Frame(self.root)
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
        self.topframe.destroy()
        self.newframe.destroy()
        self.delframe.destroy()
        self.frame = Frame(self.root)
        self.topframe = Frame(self.root)
        self.newframe = Frame(self.root) 
        self.delframe = Frame(self.root)
        Grid.rowconfigure(self.frame, 1, weight=1)
        Grid.columnconfigure(self.frame, 0, weight=1)
        Grid.rowconfigure(self.newframe, 2, weight=1)
        Grid.columnconfigure(self.newframe, 1, weight=1)

    def player(self):
        self.switchFrame()
        self.topframe.pack()
        self.frame.pack(fill=BOTH, expand=True)
        self.var = StringVar()
        self.values = self.playlist.loadPlaylist()
        if not self.values:
            self.values = ['---',]
        self.label = Label(self.topframe, text='Select a playlist:')
        self.label.grid(column=0, row=0)
        self.omenu = OptionMenu(self.topframe, self.var, *self.values, command=self.insertDescription)
        self.omenu.config(width=30)
        self.omenu.grid(column=1, row=0, sticky='w', pady=10)
        self.otext = Text(self.frame, width=70, height=15)
        self.otext.delete(1.0, END)
        self.otext.grid(column=0, row=1, columnspan=2, sticky='nsew', padx=10)
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
        self.newframe.pack(fill=BOTH, expand=True)
        self.lname = Label(self.newframe, text='Name')
        self.lname.grid(column=0, row=0, padx=10, pady=5, sticky='w')
        self.ename = Entry(self.newframe)
        self.ename.grid(column=1, row=0, sticky='ew', padx=10)
        self.lurl = Label(self.newframe, text='Url')
        self.lurl.grid(column=0, row=1, padx=10, sticky='w')
        self.eurl = Entry(self.newframe)
        self.eurl.grid(column=1, row=1, sticky='ew', padx=10)
        self.ldesc = Label(self.newframe, text='Description')
        self.ldesc.grid(column=0, row=2, sticky='n', padx=10, pady=5)
        self.tdesc = Text(self.newframe, width=55, height=10)
        self.tdesc.grid(column=1, row=2, sticky='nsew', padx=10, pady=5)
        self.bcancel = Button(self.newframe, text='Cancel', command=self.player)
        self.bcancel.grid(column=1, row=3, sticky='w', padx=10, pady=5)
        self.bsave = Button(self.newframe, text='Save', command=self.save)
        self.bsave.grid(column=1, row=3, sticky='e', padx=10, pady=5)

    def save(self):
        playlist = Playlist(name=self.ename.get(), address=self.eurl.get(), description=self.tdesc.get(1.0, END))
        playlist.savePlaylist()
        self.player()

    def delete(self):
        self.switchFrame()
        self.delframe.pack(anchor='w')
        self.var = StringVar()
        self.values = self.playlist.loadPlaylist()
        self.lname = Label(self.delframe, text='Name')
        self.lname.grid(column=0, row=0, padx=10, pady=20)
        self.omenu = OptionMenu(self.delframe, self.var, *self.values)
        self.omenu.config(width='30')
        self.omenu.grid(column=1, row=0)
        self.bcancel = Button(self.delframe, text='Cancel', command=self.player)
        self.bcancel.grid(column=1, row=1, sticky='w')
        self.bdelete = Button(self.delframe, text='Delete', command=self.deleteRecord)
        self.bdelete.grid(column=1, row=1, sticky='e')
        
    def deleteRecord(self):
        self.playlist.deletePlaylist(self.var.get())
        self.player()
        
if __name__ == '__main__':
    win = Window()
    win.player()
    mainloop()
