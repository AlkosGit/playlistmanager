# file: playlistmanager/edit.py
from tkinter import *
from style import *
from playlist import Playlist

class Edit(MyFrame):
    def __init__(self, parent, value=None, **config):
        self.value = value
        self.playlist = Playlist()
        MyFrame.__init__(self, parent, **config)
        self.pack(fill=BOTH, expand=True, pady=10)
        for i in range(7):
            Grid.rowconfigure(self, i, pad=5)
        Grid.rowconfigure(self, 5, weight=1)
        Grid.columnconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, minsize=140)
        self.lname = MyLabel(self, text='Name')
        self.lname.grid(column=0, row=1, padx=5, sticky='w')
        self.ename = MyEntry(self)
        self.ename.grid(column=1, row=1, padx=7, sticky='ew')
        self.lurl = MyLabel(self, text='URL or directory')
        self.lurl.grid(column=0, row=2, padx=5, sticky='w')
        self.eurl = MyEntry(self)
        self.eurl.grid(column=1, row=2, padx=7, sticky='ew')
        self.lres = MyLabel(self, text='Resume playback')
        self.lres.grid(column=0, row=3, padx=5, sticky='w')
        self.cbuttonresume_var = IntVar()
        self.cbuttonresume = MyCheckbutton(self, variable=self.cbuttonresume_var)
        self.cbuttonresume.grid(column=1, row=3, sticky='nw')
        #  Messagelabel for resume not supported by Twitch. Hidden by default.
        self.lres_msg = MyLabel(self, text='Resume not supported by Twitch streams!')
        self.lres_msg.grid_forget()
        ###
        self.lshuf = MyLabel(self, text='Shuffle')
        self.lshuf.grid(column=0, row=4, padx=5, sticky='w')
        self.cbuttonshuffle_var = IntVar()
        self.cbuttonshuffle = MyCheckbutton(self, variable=self.cbuttonshuffle_var)
        self.cbuttonshuffle.grid(column=1, row=4, sticky='w')
        self.lshuf_msg = MyLabel(self, text='Shuffle not supported by Twitch streams!')
        self.lshuf_msg.grid_forget()
        self.ldesc = MyLabel(self, text='Description')
        self.ldesc.grid(column=0, row=5, padx=5, pady=3, sticky='nw')
        self.tdesc = MyText(self, width=55, height=10)
        self.tdesc.grid(column=1, row=5, padx=7, sticky='nsew')
        self.bcancel = MyButton(self, text='Cancel', command=self.destroy)
        self.bcancel.grid(column=1, row=6, padx=7, pady=5, sticky='w')
        values = self.playlist.insertPlaylist(self.value)
        for pid, name, address, description, resume, shuffle in values:
            self.ename.insert(0, name)
            self.eurl.insert(0, address)
            self.cbuttonresume_var.set(resume)
            self.cbuttonshuffle_var.set(shuffle)
            self.tdesc.insert(1.0, description)
            self.bsave = MyButton(self, text='Save', command=self.update)
        self.bsave.grid(column=1, row=6, padx=7, pady=5, sticky='e')
        self.bsave.config(state=DISABLED)
        self.scaninput()

    def scaninput(self):
        '''Continuously scan "name" and "url" entryfields for input, 
        before enabling buttons; these fields have to have data 
        before saving to database.'''
        ok = True
        #  Wrap in try statement to suppress stderr when destroying frame.
        try:
            #  Get the state of save button. 
            state = str(self.bsave['state'])
        except TclError:
            return
        #  Start scanning of input.
        try:
            if not self.ename.get() == '' and not self.eurl.get() == '':
                #  Scan checkbuttons state; resume and shuffle is not supported by Twitch streams.
                if 'twitch.tv' in self.eurl.get():
                    if self.cbuttonresume_var.get():
                        self.lres_msg.grid(column=1, row=3, padx=25, sticky='w')
                        ok = False
                        self.bsave.config(state=DISABLED)
                    else:
                        self.lres_msg.grid_forget()
                        ok = True
                    if self.cbuttonshuffle_var.get():
                        self.lshuf_msg.grid(column=1, row=4, padx=25, sticky='w')
                        ok = False
                        self.bsave.config(state=DISABLED)
                    else:
                        self.lshuf_msg.grid_forget()
                #  If required fields have input, enable the save button and checkbuttons.
                #  When save button is active, stop scanning to prevent
                #  mouse-over event glitch.
                if state == 'disabled' and ok:
                    self.bsave.config(state=NORMAL)
                    self.cbuttonresume.config(state=NORMAL)
                    self.cbuttonshuffle.config(state=NORMAL)
            else:
                self.bsave.config(state=DISABLED)
                self.cbuttonresume.deselect()
                self.cbuttonshuffle.deselect()
                self.cbuttonresume.config(state=DISABLED)
                self.cbuttonshuffle.config(state=DISABLED)
            self.after(100, self.scaninput)
        #  Suppress stderr when destroying frame.    
        except TclError:
            return

    def update(self):
        playlist = Playlist(name=self.ename.get(), address=self.eurl.get(),\
                description=self.tdesc.get(1.0, END), resume=self.cbuttonresume_var.get(), shuffle=self.cbuttonshuffle_var.get())
        playlist.updatePlaylist(self.value)
        self.destroy()