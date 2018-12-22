# file: playlistmanager/main.py
from playlist import Playlist
from tkinter import *
from tkinter import ttk, filedialog
import subprocess
import threading, queue
import os

class Window:
    def __init__(self):
        self.playlist = Playlist() 
        self.root = Tk()
        #  Import widget style sheet.
        self.root.option_readfile('stylesheet.txt')
        #  Make window appear centered on screen.
        self.width, self.height = 800, 500
        x = (self.root.winfo_screenwidth() / 2) - (self.width /2)
        y = (self.root.winfo_screenheight() /2) - (self.height / 2)
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))
        ###
        self.root.title('Playlist Manager')
        #  Create frames.
        self.frames = ('self.mainframe', 'self.topframe', 'self.newframe', 'self.delframe', 'self.downframe')
        for f in self.frames:
            exec('{} = Frame(self.root)'.format(f))
        #  Create filemenu.
        self.menubar = Menu(self.root, activebackground='#555555', activeforeground='#FFFFFF')
        self.filemenu = Menu(self.menubar, tearoff=0, activebackground='#555555', activeforeground='#FFFFFF')
        self.filemenu.add_command(label='New playlist', command=self.new)
        self.filemenu.add_command(label='Download playlist', command=self.download)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.root.destroy)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.root.config(menu=self.menubar, background='#444444')

    def switchFrame(self):
        #  Destroy and recreate frames.
        for f in self.frames: 
            exec('{}.destroy()'.format(f))
            exec('{} = Frame(self.root)'.format(f))
        ###
        Grid.rowconfigure(self.mainframe, 1, weight=1)
        Grid.columnconfigure(self.mainframe, 0, weight=1)
        Grid.rowconfigure(self.newframe, 5, weight=1)
        Grid.columnconfigure(self.newframe, 1, weight=1)
        Grid.columnconfigure(self.topframe, 2, minsize=150)
        Grid.columnconfigure(self.newframe, 0, minsize=140)
        Grid.columnconfigure(self.downframe, 0, minsize=140)
        Grid.columnconfigure(self.downframe, 1, weight=1)
        Grid.rowconfigure(self.downframe, 2, weight=1)

    def player(self):
        '''   This is the main window.  '''
        self.switchFrame()
        self.topframe.pack(fill=BOTH)
        self.mainframe.pack(fill=BOTH, expand=True, padx=10)
        self.lplaylist = Label(self.topframe, text='Select a playlist:')
        self.lplaylist.grid(column=0, row=0, padx=10)
        self.cboxplayer_var = StringVar()
        self.cboxplayer = ttk.Combobox(self.topframe, textvariable=self.cboxplayer_var)
        self.cboxplayer.grid(column=1, row=0, sticky='w', pady=10)
        #  Populate combobox.
        self.cboxplayer['values'] = self.playlist.loadPlaylist()
        self.cboxplayer.bind('<<ComboboxSelected>>', self.initPlayer)
        #  Set combobox to read-only.
        self.cboxplayer.config(state='readonly', width=30)
        ###
        self.cbuttonresume_var = IntVar()
        self.cbuttonresume = Checkbutton(self.topframe, text='Resume playback',\
                variable=self.cbuttonresume_var, activebackground='#444444',\
                highlightbackground='#444444', foreground='#444444')
        self.cbuttonshuffle_var = IntVar()
        self.cbuttonshuffle = Checkbutton(self.topframe, text='Shuffle',\
                variable=self.cbuttonshuffle_var, activebackground='#444444',\
                highlightbackground='#444444', foreground='#444444')
        #  Hide 'resume' and 'shuffle' checkbuttons until a playlist is selected.
        self.cbuttonresume.grid_forget()
        self.cbuttonshuffle.grid_forget()
        ###
        scrollbar = Scrollbar(self.mainframe)
        scrollbar.grid(column=1, row=1, sticky='ns')
        self.tmain = Text(self.mainframe, width=70, height=15, relief='flat', yscrollcommand=scrollbar.set)
        self.tmain.delete(1.0, END)
        self.tmain.grid(column=0, row=1, sticky='nsew')
        scrollbar.config(command=self.tmain.yview)
        self.bdelete = Button(self.mainframe, text='Delete', command=self.delete,\
                activebackground='#333333', activeforeground='white')
        self.bdelete.grid(column=0, row=2, sticky='w', pady=5)
        self.bedit = Button(self.mainframe, text='Edit', command=lambda: self.new(mode='edit'),\
                activebackground='#333333', activeforeground='white')
        self.bedit.grid(column=0, row=2, sticky='w', padx=70)
        self.bplay = Button(self.mainframe, text='Play', command=self.play,\
                activebackground='#333333', activeforeground='white')
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

    def runloop(self, thread_queue, resume, shuffle):
        '''   Player runs in own thread. 
        Store output from player in thread queue.   '''
        #  Determine which player command to use; Twitch videos need 'streamlink' to play in mpv.
        #  Resume and shuffle not supported by Twitch streams.
        if 'twitch.tv' in self.url:
            playercmd, streamparm, streamopts = '/usr/bin/streamlink', '-p mpv', 'best'
            #  Enable fast-forward, seek etc.
            streamseek = '--player-passthrough=hls'
        else:
            playercmd = '/usr/bin/mpv'
            resumeopt = '--save-position-on-quit'
            shuffleopt = '--shuffle'
        #  Check for selected options.
        if resume and shuffle:
            self.process = subprocess.Popen([playercmd, resumeopt, shuffleopt, self.url], stdout=subprocess.PIPE)
        else:
            if resume:
                self.process = subprocess.Popen([playercmd, resumeopt, self.url], stdout=subprocess.PIPE)
            else:
                if shuffle:
                    self.process = subprocess.Popen([playercmd, shuffleopt, '--loop', self.url], stdout=subprocess.PIPE)
                else:
                    if 'twitch.tv' in self.url:
                        self.process = subprocess.Popen([playercmd, streamparm, streamseek, self.url, streamopts], stdout=subprocess.PIPE)
                    else:
                        self.process = subprocess.Popen([playercmd, self.url], stdout=subprocess.PIPE)

        #  Output is a continuous stream, so we need to loop.
        while True:
            output = self.process.stdout.readline()
            if not output:
                break
            else:
                #  Store output in thread queue
                thread_queue.put(output)

    def play(self):
        '''   Start player in separate thread.   '''
        value = (self.cboxplayer_var.get())
        #  Retrieve url or mediafile from selected playlist.
        self.url = self.playlist.selectPlaylist(value)
        #  Create thread queue to monitor output from thread.
        self.thread_queue = queue.Queue()
        #  Create thread and pass thread queue
        self.thread = threading.Thread(target=self.runloop, args=(self.thread_queue, self.resume, self.shuffle))
        self.thread.start()
        #  Disable buttons while playing.
        for button in self.bdelete, self.bplay, self.bedit:
            button.config(state=DISABLED)
        #  Call listener method.
        self.listen_for_result()

    def listen_for_result(self, mode=None):
        '''   Keep listening for updated output from player.   '''
        #  Monitor thread output; quit if thread has exited.
        self.thread.result_queue = self.thread_queue
        if 'stopped' in str(self.thread):
            if mode == 'download':
                print ('stopped')
                self.scanDownload()
            else:
                for button in self.bdelete, self.bplay, self.bedit:
                    button.config(state=NORMAL)
            return

        try:
            if mode == 'download':
                self.tdownload.config(state=NORMAL)
            else:
                self.tmain.config(state=NORMAL)
        except TclError:
            return
        try:
            #  Capturing an output stream, so we need to loop.
            while True:
                #  Retrieve the output from thread queue and insert into text widget.
                self.res = self.thread_queue.get(0)
                if mode == 'download':
                    self.tdownload.insert(END, self.res)
                    self.tdownload.see(END)
                else:
                    self.tmain.insert(END, self.res)
                    self.tmain.see(END)
        except queue.Empty:
            #  No updated output from stream, so keep looping.
            if mode == 'download':
                self.root.after(100, lambda: self.listen_for_result(mode='download'))
            else:
                self.root.after(100, self.listen_for_result)
        if mode == 'download':
            self.tdownload.config(state=DISABLED)
        else:
            self.tmain.config(state=DISABLED)

    def new(self, mode=None):
        '''   Create new playlist. 
        If mode = "edit" same window is used to edit existing playlist.   '''
        self.switchFrame()
        self.newframe.pack(fill=BOTH, expand=True, pady=10)
        for i in range(7):
            Grid.rowconfigure(self.newframe, i, pad=5)
        self.lname = Label(self.newframe, text='Name')
        self.lname.grid(column=0, row=1, padx=5, sticky='w')
        self.ename = Entry(self.newframe, highlightcolor='white', insertbackground='white')
        self.ename.grid(column=1, row=1, padx=7, sticky='ew')
        self.lurl = Label(self.newframe, text='URL or directory')
        self.lurl.grid(column=0, row=2, padx=5, sticky='w')
        self.eurl = Entry(self.newframe, highlightcolor='white', insertbackground='white')
        self.eurl.grid(column=1, row=2, padx=7, sticky='ew')
        self.lres = Label(self.newframe, text='Resume playback')
        self.lres.grid(column=0, row=3, padx=5, sticky='w')
        self.cbuttonresume_var = IntVar()
        self.cbuttonresume = Checkbutton(self.newframe, variable=self.cbuttonresume_var,\
                highlightcolor='white', activebackground='#444444',\
                highlightbackground='#444444', foreground='#444444')
        self.cbuttonresume.grid(column=1, row=3, sticky='nw')
        #  Messagelabel for resume not supported by Twitch. Hidden by default.
        self.lres_msg = Label(self.newframe, text='Resume not supported by Twitch streams!')
        self.lres_msg.grid_forget()
        ###
        self.lshuf = Label(self.newframe, text='Shuffle')
        self.lshuf.grid(column=0, row=4, padx=5, sticky='w')
        self.cbuttonshuffle_var = IntVar()
        self.cbuttonshuffle = Checkbutton(self.newframe, variable=self.cbuttonshuffle_var,\
                highlightcolor='white', activebackground='#444444',\
                highlightbackground='#444444', foreground='#444444')
        self.cbuttonshuffle.grid(column=1, row=4, sticky='w')
        self.lshuf_msg = Label(self.newframe, text='Shuffle not supported by Twitch streams!')
        self.lshuf_msg.grid_forget()
        self.ldesc = Label(self.newframe, text='Description')
        self.ldesc.grid(column=0, row=5, padx=5, pady=3, sticky='nw')
        self.tdesc = Text(self.newframe, width=55, height=10, relief='flat', highlightcolor='white', insertbackground='white')
        self.tdesc.grid(column=1, row=5, padx=7, sticky='nsew')
        self.bcancel = Button(self.newframe, text='Cancel', command=self.player, activebackground='#333333', activeforeground='white')
        self.bcancel.grid(column=1, row=6, padx=7, pady=5, sticky='w')
        if mode == 'edit':
            values = self.playlist.insertPlaylist(self.value)
            for pid, name, address, description, resume, shuffle in values:
                self.ename.insert(0, name)
                self.eurl.insert(0, address)
                self.cbuttonresume_var.set(resume)
                self.cbuttonshuffle_var.set(shuffle)
                self.tdesc.insert(1.0, description)
                self.bsave = Button(self.newframe, text='Save', command=self.update, activebackground='#333333', activeforeground='white')
        else:
            self.bsave = Button(self.newframe, text='Save', command=self.save, activebackground='#333333', activeforeground='white')
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
            self.root.after(100, self.scaninput)
        #  Suppress stderr when destroying frame.    
        except TclError:
            return

    def save(self):
        if 'twitch.tv' in self.eurl.get():
            self.cbuttonresume_var.set(0)
            self.cbuttonshuffle_var.set(0)
        playlist = Playlist(name=self.ename.get(), address=self.eurl.get(),\
                description=self.tdesc.get(1.0, END), resume=self.cbuttonresume_var.get(), shuffle=self.cbuttonshuffle_var.get())
        playlist.savePlaylist()
        self.player()
        
    def delete(self):
        self.playlist.deletePlaylist(self.cboxplayer_var.get())
        self.player()

    def update(self):
        playlist = Playlist(name=self.ename.get(), address=self.eurl.get(),\
                description=self.tdesc.get(1.0, END), resume=self.cbuttonresume_var.get(), shuffle=self.cbuttonshuffle_var.get())
        playlist.updatePlaylist(self.value)
        self.player()

    def download(self):
        self.switchFrame()
        self.downframe.pack(fill=BOTH, expand=True, padx=10, pady=5)
        for i in range(4):
            Grid.rowconfigure(self.downframe, i, pad=5)
        self.ldownload_url = Label(self.downframe, text='URL')
        self.ldownload_url.grid(column=0, row=0, sticky='w')
        self.edownload_url = Entry(self.downframe, highlightcolor='white', insertbackground='white')
        self.edownload_url.grid(column=1, row=0, sticky='ew')
        self.ldownload_dir = Label(self.downframe, text='Destination')
        self.ldownload_dir.grid(column=0, row=1, sticky='w')
        self.edownload_dir = Entry(self.downframe, highlightcolor='white', insertbackground='white')
        self.edownload_dir.grid(column=1, row=1, sticky='ew')
        scrollbar = Scrollbar(self.downframe)
        scrollbar.grid(column=2, row=2, pady=5, sticky='ns')
        self.tdownload = Text(self.downframe, width=55, height=10, relief='flat', highlightcolor='white',\
                insertbackground='white', yscrollcommand=scrollbar.set)
        self.tdownload.grid(column=0, row=2, columnspan=2, pady=5, sticky='nsew')
        scrollbar.config(command=self.tdownload.yview)
        self.bcancel_download = Button(self.downframe, text='Cancel', command=self.cancelDownload,\
                activebackground='#333333', activeforeground='white')
        self.bcancel_download.grid(column=0, row=3, sticky='w')
        self.bsave_download = Button(self.downframe, text='Download', command=self.saveDownload,\
                activebackground='#333333', activeforeground='white')
        self.bsave_download.grid(column=1, row=3, sticky='e')
        self.tdownload.config(state=DISABLED)
        self.scanDownload()

    def scanDownload(self, exit=False):
        try:
            state = str(self.bsave_download['state'])
        except TclError:
            return
        if not self.edownload_url.get() == '' and not self.edownload_dir.get() == '':
            if state == 'disabled':
                self.bsave_download.config(state=NORMAL)
        else:
            self.bsave_download.config(state=DISABLED)
        self.after_id = self.root.after(100, self.scanDownload)

    def saveDownload(self):
        '''   Start download in separate thread.   '''
        #  Create thread queue to monitor output from thread.
        self.thread_queue = queue.Queue()
        #  Create thread and pass thread queue.
        self.thread = threading.Thread(target=self.downloop, args=(self.thread_queue, self.edownload_url.get(), self.edownload_dir.get()))
        self.thread.start()
        #  Signal scanDownload to exit.
        self.root.after_cancel(self.after_id)
        #  Disable download button.
        self.bsave_download.config(state=DISABLED)
        #  Call listener method.
        self.listen_for_result(mode='download')

    def downloop(self, thread_queue, url, path):
        #  Remove trailing '/', if any.
        if '/' in (path[-1:]):
            path = path[:-1]
        #  Streamlink needs a filename; extract from URL.
        if 'twitch.tv' in url:
            filename = url.split('/')[-1]
            fullpath = '{}/{}.mp4'.format(path, filename)
            self.process = subprocess.Popen(['/usr/bin/streamlink', '-p mpv', '-f', url, 'best', '-o', fullpath], stdout=subprocess.PIPE)
        else:
            #  Youtube URL.
            fullpath = '{}/%(title)s.%(ext)s'.format(path)
            self.process = subprocess.Popen(['/usr/bin/youtube-dl', '-o', fullpath, url], stdout=subprocess.PIPE)

        #  Output is a continuous stream, so we need to loop.
        while True:
            output = self.process.stdout.readline()
            if not output:
                break
            else:
                #  Store output in thread queue.
                thread_queue.put(output)

    def cancelDownload(self):
        #  Signal scanDownload to exit.
        self.root.after_cancel(self.after_id)
        #  Suppress stderr and stdout to console.
        os.system('killall youtube-dl >/dev/null 2>&1')
        os.system('killall streamlink >/dev/null 2>&1')
        self.player()

if __name__ == '__main__':
    win = Window()
    win.player()
    mainloop()
