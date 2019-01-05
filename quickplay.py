# file: playlistmanager/quickplay.py
from tkinter import *
from style import *
import queue

class QuickPlay(MyFrame):
    def __init__(self, parent, **config):
        MyFrame.__init__(self, parent, **config)
        self.topframe = MyFrame(self)
        self.mainframe = MyFrame(self)
        self.topframe.pack(fill=BOTH)
        self.mainframe.pack(fill=BOTH, expand=True, padx=10)
        Grid.columnconfigure(self.mainframe, 0, weight=1)
        Grid.columnconfigure(self.topframe, 1, weight=1)
        Grid.rowconfigure(self.topframe, 1, weight=1)
        self.lurl = MyLabel(self.topframe, text='Insert a URL or path:')
        self.lurl.grid(column=0, row=0, padx=5, pady=5)
        self.eurl = MyEntry(self.topframe)
        self.eurl.grid(column=1, row=0, padx=24, pady=5, sticky='ew')
        scrollbar = MyScrollbar(self.mainframe)
        scrollbar.grid(column=1, row=1, sticky='ns')
        self.tmain = MyText(self.mainframe, width=70, height=25, yscrollcommand=scrollbar.set)
        self.tmain.delete(1.0, END)
        self.tmain.grid(column=0, row=1, sticky='nsew')
        scrollbar.config(command=self.tmain.yview)
        self.bcancel = MyButton(self.mainframe, text='Cancel', command=self.destroy)
        self.bcancel.grid(column=0, row=2, sticky='w', pady=5)
        self.bplay = MyButton(self.mainframe, text='Play', command=self.play)
        self.bplay.grid(column=0, row=2, sticky='e', pady=5)
        self.tmain.config(state=DISABLED)
        self.bplay.config(state=DISABLED)
        self.scaninput()

    def scaninput(self):
        '''Continuously scan url entryfield for input 
        before enabling button.'''
        #  Wrap in try statement to suppress stderr when destroying frame.
        try:
            #  Get the state of play button. 
            state = str(self.bplay['state'])
        except TclError:
            return
        #  Start scanning of input.
        try:
            if not self.eurl.get() == '':
                #  If required field has input, enable the play button.
                #  When play button is active, stop scanning to prevent
                #  mouse-over event glitch.
                if state == 'disabled':
                    self.bplay.config(state=NORMAL)
            else:
                self.bplay.config(state=DISABLED)
            self.quickplay_id = self.after(100, self.scaninput)
        #  Suppress stderr when destroying frame.    
        except TclError:
            return

    def play(self):
        from play import Play
        self.value = self.eurl.get()
        self.player = Play(self.value, mode='quickplay')
        #  Stop scanning url field.
        self.after_cancel(self.quickplay_id)
        #  Disable play button while playing.
        self.bplay.config(state=DISABLED)
        #  Call listener method.
        self.listen_for_result()

    def listen_for_result(self):
        '''   Keep listening for updated output from player.   '''
        #  Monitor thread output; quit if thread has exited.
        self.player.thread.result_queue = self.player.thread_queue
        if 'stopped' in str(self.player.thread):
            self.bplay.config(state=NORMAL)
            self.scaninput()
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
