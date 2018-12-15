# file: playlistmanager/main.py
from playlist import Playlist
from tkinter import *
import subprocess
import threading, queue

class Window:
    def __init__(self):
        self.playlist = Playlist() 
        self.root = Tk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_heigth = self.root.winfo_screenheight()
        self.width = 650
        self.height = 400
        x = (self.screen_width / 2) - (self.width /2)
        y = (self.screen_heigth /2) - (self.height / 2)
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))
        self.root.title('Playlist Manager')
        self.frame = Frame(self.root)
        self.topframe = Frame(self.root)
        self.newframe = Frame(self.root)
        self.delframe = Frame(self.root)
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='New', command=self.new)
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
        Grid.rowconfigure(self.newframe, 3, weight=1)
        Grid.columnconfigure(self.newframe, 1, weight=1)

    def player(self):
        self.switchFrame()
        self.topframe.pack()
        self.frame.pack(fill=BOTH, expand=True)
        self.listvar = StringVar()
        self.values = self.playlist.loadPlaylist()
        self.label = Label(self.topframe, text='Select a playlist:')
        self.label.grid(column=0, row=0)
        self.omenu = OptionMenu(self.topframe, self.listvar, *self.values, command=self.insertDescription)
        self.omenu.config(width=30)
        self.omenu.grid(column=1, row=0, sticky='w', pady=10)
        self.chkvar = IntVar()
        self.cbres = Checkbutton(self.topframe, text='Resume playback', variable=self.chkvar)
        self.cbres.grid(column=2, row=0)
        self.cbres.config(state=DISABLED)
        self.otext = Text(self.frame, width=70, height=15)
        self.otext.delete(1.0, END)
        self.otext.grid(column=0, row=1, columnspan=2, sticky='nsew', padx=10)
        self.otext.config(state=DISABLED)
        self.bdelete = Button(self.frame, text='Delete', command=self.delete)
        self.bdelete.grid(column=0, row=2, sticky='w', pady=10, padx=10)
        self.bdelete.config(state=DISABLED)
        self.bplay = Button(self.frame, text='Play', command=self.play)
        self.bplay.grid(column=1, row=2, sticky='e', pady=10, padx=10)
        self.bplay.config(state=DISABLED)
        
    def insertDescription(self, value):
        description = self.playlist.loadDescription(value)
        resume = self.playlist.resumePlaylist(value)
        self.cbres.config(state=NORMAL)
        self.chkvar.set(resume)
        self.cbres.config(state=DISABLED)
        self.otext.config(state=NORMAL)
        self.otext.delete(1.0, END)
        self.otext.insert(END, description)
        self.otext.config(state=DISABLED)
        if resume != None:
            self.bplay.config(state=NORMAL)
            self.bdelete.config(state=NORMAL)

    def runloop(self, thread_queue, resume):
        if resume:
            self.process = subprocess.Popen(['/usr/bin/mpv', '--save-position-on-quit', self.url], stdout=subprocess.PIPE)
        else:
            self.process = subprocess.Popen(['/usr/bin/mpv', self.url], stdout=subprocess.PIPE)

        #  output is a continuous stream, so we need to loop.
        while True:
            output = self.process.stdout.readline()
            if not output:
                break
            else:
                #  store output in thread queue
                thread_queue.put(output)

    def play(self):
        value = (self.listvar.get())
        self.url = self.playlist.selectPlaylist(value)
        resume = self.playlist.resumePlaylist(value)
        #  create thread queue to monitor updates from thread.
        self.thread_queue = queue.Queue()
        #  create thread and pass thread queue
        self.thread = threading.Thread(target=self.runloop, args=(self.thread_queue, resume))
        self.thread.start()
        #  call listener method every 100 msec.
        self.root.after(100, self.listen_for_result)

    def listen_for_result(self):
        self.otext.config(state=NORMAL)
        try:
            #  capturing an output stream, so we need a loop.
            while True:
                #  retrieve the output from thread queue and insert into text widget.
                self.res = self.thread_queue.get(0)
                self.otext.insert(END, self.res)
        except queue.Empty:
            #  no updated output from stream, so keep looping.
            self.root.after(100, self.listen_for_result)
        self.otext.config(state=DISABLED)

    def new(self):
        self.switchFrame()
        self.newframe.pack(fill=BOTH, expand=True)
        self.lname = Label(self.newframe, text='Name')
        self.lname.grid(column=0, row=0, padx=10, pady=5, sticky='w')
        self.ename = Entry(self.newframe)
        self.ename.grid(column=1, row=0, sticky='ew', padx=10)
        self.lurl = Label(self.newframe, text='URL')
        self.lurl.grid(column=0, row=1, padx=10, sticky='w')
        self.eurl = Entry(self.newframe)
        self.eurl.grid(column=1, row=1, sticky='ew', padx=10)
        self.lres = Label(self.newframe, text='Resume playback')
        self.lres.grid(column=0, row=2, padx=10, pady=5, sticky='w')
        self.chkvar = IntVar()
        self.cbres = Checkbutton(self.newframe, text='', variable=self.chkvar)
        self.cbres.grid(column=1, row=2, padx=3, sticky='w')
        self.ldesc = Label(self.newframe, text='Description')
        self.ldesc.grid(column=0, row=3, sticky='nw', padx=10, pady=5)
        self.tdesc = Text(self.newframe, width=55, height=10)
        self.tdesc.grid(column=1, row=3, sticky='nsew', padx=10, pady=5)
        self.bcancel = Button(self.newframe, text='Cancel', command=self.player)
        self.bcancel.grid(column=1, row=4, sticky='w', padx=10, pady=5)
        self.bsave = Button(self.newframe, text='Save', command=self.save)
        self.bsave.grid(column=1, row=4, sticky='e', padx=10, pady=5)

    def save(self):
        playlist = Playlist(name=self.ename.get(), address=self.eurl.get(), description=self.tdesc.get(1.0, END), resume=self.chkvar.get())
        playlist.savePlaylist()
        self.player()
        
    def delete(self):
        self.playlist.deletePlaylist(self.listvar.get())
        self.player()
        
if __name__ == '__main__':
    win = Window()
    win.player()
    mainloop()
