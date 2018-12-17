# file: playlistmanager/main.py
from playlist import Playlist
from tkinter import *
from tkinter import ttk
import subprocess
import threading, queue

class Window:
    def __init__(self):
        self.playlist = Playlist() 
        self.root = Tk()
        #  import widget style sheet.
        self.root.option_readfile('stylesheet.txt')
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
        self.menubar = Menu(self.root, activebackground='#555555', activeforeground='#FFFFFF')
        self.filemenu = Menu(self.menubar, tearoff=0, activebackground='#555555', activeforeground='#FFFFFF')
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
        Grid.rowconfigure(self.newframe, 4, weight=1)
        Grid.columnconfigure(self.newframe, 1, weight=1)
        Grid.columnconfigure(self.topframe, 2, minsize=150)

    def player(self):
        self.switchFrame()
        self.topframe.pack(fill=BOTH)
        self.frame.pack(fill=BOTH, expand=True)
        self.listvar = StringVar()
        self.label = Label(self.topframe, text='Select a playlist:')
        self.label.grid(column=0, row=0, padx=10)
        self.cbox = ttk.Combobox(self.topframe, textvariable=self.listvar)
        self.cbox.grid(column=1, row=0, sticky='w', pady=10)
        self.cbox['values'] = self.playlist.loadPlaylist()
        self.cbox.bind('<<ComboboxSelected>>', self.insertDescription)
        self.cbox.config(state='readonly', width=30)
        self.resvar = IntVar()
        self.cbres = Checkbutton(self.topframe, text='Resume playback',\
                variable=self.resvar, activebackground='#444444',\
                highlightbackground='#444444', foreground='#444444')
        self.cbres.config(state=DISABLED)
        #  Hide 'resume' checkbox until a playlist is selected.
        self.cbres.grid_forget()
        self.otext = Text(self.frame, width=70, height=15, relief='flat')
        self.otext.delete(1.0, END)
        self.otext.grid(column=0, row=1, columnspan=2, sticky='nsew', padx=10)
        self.otext.config(state=DISABLED)
        self.bdelete = Button(self.frame, text='Delete', command=self.delete, activebackground='#333333', activeforeground='white')
        self.bdelete.grid(column=0, row=2, sticky='w', pady=5, padx=10)
        self.bdelete.config(state=DISABLED)
        self.bplay = Button(self.frame, text='Play', command=self.play, activebackground='#333333', activeforeground='white')
        self.bplay.grid(column=1, row=2, sticky='e', pady=5, padx=10)
        self.bplay.config(state=DISABLED)
        
    def insertDescription(self, value):
        self.cbox.selection_clear()
        value = self.cbox.get()
        description = self.playlist.loadDescription(value)
        #  Get resume status.
        resume = self.playlist.resumePlaylist(value)
        self.otext.config(state=NORMAL)
        self.otext.delete(1.0, END)
        self.otext.insert(END, description)
        self.otext.config(state=DISABLED)
        #  Only enable buttons and show 'resume' checkbox when valid playlist is selected.
        if resume != None:
            self.bplay.config(state=NORMAL)
            self.bdelete.config(state=NORMAL)
            self.cbres.grid(column=2, row=0)
            self.cbres.config(state=NORMAL)
            self.resvar.set(resume)
            self.cbres.config(state=DISABLED)

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
        self.resvar = IntVar()
        self.shufvar = IntVar()
        for i in range(6):
            Grid.rowconfigure(self.newframe, i, pad=5)
        Grid.columnconfigure(self.newframe, 0, minsize=140)
        self.lname = Label(self.newframe, text='Name')
        self.lname.grid(column=0, row=0, padx=5, sticky='w')
        self.ename = Entry(self.newframe, highlightcolor='white', insertbackground='white')
        self.ename.grid(column=1, row=0, padx=7, sticky='ew')
        self.lurl = Label(self.newframe, text='URL')
        self.lurl.grid(column=0, row=1, padx=5, sticky='w')
        self.eurl = Entry(self.newframe, highlightcolor='white', insertbackground='white')
        self.eurl.grid(column=1, row=1, padx=7, sticky='ew')
        self.lres = Label(self.newframe, text='Resume playback')
        self.lres.grid(column=0, row=2, padx=5, sticky='w')
        self.cbres = Checkbutton(self.newframe, variable=self.resvar,\
                highlightcolor='white', activebackground='#444444',\
                highlightbackground='#444444', foreground='#444444')
        self.cbres.grid(column=1, row=2, sticky='nw')
        self.lshuf = Label(self.newframe, text='Shuffle')
        self.lshuf.grid(column=0, row=3, padx=5, sticky='w')
        self.cbshuf = Checkbutton(self.newframe, variable=self.shufvar,\
                highlightcolor='white', activebackground='#444444',\
                highlightbackground='#444444', foreground='#444444')
        self.cbshuf.grid(column=1, row=3, sticky='w')
        self.ldesc = Label(self.newframe, text='Description')
        self.ldesc.grid(column=0, row=4, padx=5, pady=3, sticky='nw')
        self.tdesc = Text(self.newframe, width=55, height=10, relief='flat', highlightcolor='white', insertbackground='white')
        self.tdesc.grid(column=1, row=4, padx=7, sticky='nsew')
        self.bcancel = Button(self.newframe, text='Cancel', command=self.player, activebackground='#333333', activeforeground='white')
        self.bcancel.grid(column=1, row=5, padx=7, pady=5, sticky='w')
        self.bsave = Button(self.newframe, text='Save', command=self.save, activebackground='#333333', activeforeground='white')
        self.bsave.grid(column=1, row=5, padx=7, pady=5, sticky='e')
        self.bsave.config(state=DISABLED)
        self.scaninput()

    def scaninput(self):
        '''Continuously scan "name" and "url" entryfields for input;
        these fields have to have data before saving to database.'''
        #  Get the state of 'save' button. Wrap in try statement to suppress stderr when destroying frame.
        try:
            state = str(self.bsave['state'])
        except TclError:
            return
        #  Start scanning of input. 
        try:
            if not self.ename.get() == '' and not self.eurl.get() == '':
                #  If required fields have input, stop scanning the button.
                if state == 'disabled':
                    self.bsave.config(state=NORMAL)
            else:
                self.bsave.config(state=DISABLED)
            self.root.after(100, self.scaninput)
        #  Suppress stderr when destroying frame.    
        except TclError:
            return

    def save(self):
        playlist = Playlist(name=self.ename.get(), address=self.eurl.get(), description=self.tdesc.get(1.0, END), resume=self.resvar.get())
        playlist.savePlaylist()
        self.player()
        
    def delete(self):
        self.playlist.deletePlaylist(self.listvar.get())
        self.player()
        
if __name__ == '__main__':
    win = Window()
    win.player()
    mainloop()
