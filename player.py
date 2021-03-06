# file: playlistmanager/player.py
from playlist import Playlist
from tkinter import *
from tkinter import ttk
from style import *
import queue

class Player(MyFrame):
    def __init__(self, parent, **config):
        self.playlist = Playlist()
        MyFrame.__init__(self, parent, **config)
        self.topframe = MyFrame(self)
        self.mainframe = MyFrame(self)
        self.topframe.pack(fill=BOTH)
        self.mainframe.pack(fill=BOTH, expand=True, padx=10)
        Grid.rowconfigure(self.mainframe, 1, weight=1)
        Grid.columnconfigure(self.mainframe, 0, weight=1)
        Grid.columnconfigure(self.topframe, 2, minsize=150)
        self.lplaylist = MyLabel(self.topframe, text='Select a playlist:')
        self.lplaylist.grid(column=0, row=0, padx=10)
        self.cboxplayer_var = StringVar()
        self.cboxplayer = MyCombobox(self.topframe, textvariable=self.cboxplayer_var)
        self.cboxplayer.grid(column=1, row=0, sticky='w', pady=10)
        #  Populate combobox.
        self.cboxplayer['values'] = self.playlist.loadPlaylist()
        self.cboxplayer.bind('<<ComboboxSelected>>', self.initPlayer)
        #  Set combobox to read-only.
        self.cboxplayer.config(state='readonly', width=50)
        ###
        self.cbuttonresume_var = IntVar()
        self.cbuttonresume = MyCheckbutton(self.topframe, text='Resume playback', variable=self.cbuttonresume_var)
        self.cbuttonshuffle_var = IntVar()
        self.cbuttonshuffle = MyCheckbutton(self.topframe, text='Shuffle', variable=self.cbuttonshuffle_var)
        #  Hide 'resume' and 'shuffle' checkbuttons until a playlist is selected.
        self.cbuttonresume.grid_forget()
        self.cbuttonshuffle.grid_forget()
        ###
        scrollbar = MyScrollbar(self.mainframe)
        scrollbar.grid(column=1, row=1, sticky='ns')
        self.tmain = MyText(self.mainframe, width=70, height=15, yscrollcommand=scrollbar.set)
        self.tmain.delete(1.0, END)
        self.tmain.grid(column=0, row=1, sticky='nsew')
        scrollbar.config(command=self.tmain.yview)
        self.bdelete = MyButton(self.mainframe, text='Delete', command=self.delete)
        self.bdelete.grid(column=0, row=2, sticky='w', pady=5)
        self.bedit = MyButton(self.mainframe, text='Edit', command=self.edit)
        self.bedit.grid(column=0, row=2, sticky='w', padx=70)
        self.bplay = MyButton(self.mainframe, text='Play', command=self.play)
        self.bplay.grid(column=0, row=2, sticky='e', pady=5)
        #  Disable text widget, checkbuttons and buttons until a playlist is selected.
        self.widget = (self.cbuttonresume, self.cbuttonshuffle, self.tmain, self.bdelete, self.bplay, self.bedit)
        for widget in self.widget:
            widget.config(state=DISABLED)

    def initPlayer(self, value):
        '''   Prepare to play selected playlist: fetch url/file, resume and shuffle options,
        and enable buttons.   '''
        #  Clear combobox after setting it to read-only to avoid artifacts.
        self.cboxplayer.selection_clear()
        #  Get selected playlist.
        self.value = self.cboxplayer.get()
        #  Get description.
        description = self.playlist.loadDescription(self.value)
        #  Get resume and shuffle status.
        self.resume = self.playlist.resumePlaylist(self.value)
        self.shuffle = self.playlist.shufflePlaylist(self.value)
        #  Insert description.
        self.tmain.config(state=NORMAL)
        self.tmain.delete(1.0, END)
        self.tmain.insert(END, description)
        #  Only enable buttons and show 'resume' and 'shuffle' checkbox when valid playlist is selected.
        #  resume = None when no database record is returned.
        if self.resume != None:
            for widget in self.widget: 
                widget.config(state=NORMAL)
            self.cbuttonresume.grid(column=2, row=0)
            self.cbuttonshuffle.grid(column=3, row=0)
            self.tmain.config(state=DISABLED)
            #  Toggle checkbuttons on or off.
            self.cbuttonresume_var.set(self.resume)
            self.cbuttonresume.config(state=DISABLED)
            self.cbuttonshuffle_var.set(self.shuffle)
            self.cbuttonshuffle.config(state=DISABLED)

    def play(self):
        from play import Play
        self.player = Play(self.value, self.resume, self.shuffle)
        #  Disable buttons while playing.
        for button in self.bdelete, self.bplay, self.bedit:
            button.config(state=DISABLED)
        #  Call listener method.
        self.listen_for_result()

    def listen_for_result(self):
        '''   Keep listening for updated output from player.   '''
        #  Monitor thread output; quit if thread has exited.
        self.player.thread.result_queue = self.player.thread_queue
        if 'stopped' in str(self.player.thread):
            for button in self.bdelete, self.bplay, self.bedit:
                button.config(state=NORMAL)
            return
        ###
        self.tmain.config(state=NORMAL)

        try:
            #  Capturing an output stream, so we need to loop.
            while True:
                #  Retrieve the output from thread queue and insert into text widget.
                self.res = self.player.thread_queue.get(0)
                self.tmain.insert(END, self.res)
                self.tmain.see(END)
        except queue.Empty:
            #  No updated output from stream, so keep looping.
            self.listen_id = self.after(100, self.listen_for_result)

    def delete(self):
        self.playlist.deletePlaylist(self.cboxplayer_var.get())
        self.destroy()

    def edit(self):
        self.topframe.destroy()
        self.mainframe.destroy()
        from edit import Edit
        e = Edit(self, value=self.value)
        e.pack()
        self.wait_window(e)
        self.destroy()