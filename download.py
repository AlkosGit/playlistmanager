# file: playlistmanager/download.py
from tkinter import *
from style import *
import threading, queue
import subprocess
import os

class Download(MyFrame):
    def __init__(self, parent, **config):
        MyFrame.__init__(self, parent, **config)
        self.pack(fill=BOTH, expand=True, padx=10, pady=5)
        for i in range(4):
            Grid.rowconfigure(self, i, pad=5)
        Grid.columnconfigure(self, 0, minsize=140)
        Grid.columnconfigure(self, 1, weight=1)
        Grid.rowconfigure(self, 2, weight=1)
        self.ldownload_url = MyLabel(self, text='URL')
        self.ldownload_url.grid(column=0, row=0, sticky='w')
        self.edownload_url = MyEntry(self)
        self.edownload_url.grid(column=1, row=0, columnspan=2, sticky='ew')
        self.ldownload_dir = MyLabel(self, text='Destination')
        self.ldownload_dir.grid(column=0, row=1, sticky='w')
        self.edownload_dir = MyEntry(self)
        self.edownload_dir.grid(column=1, row=1, columnspan=2, sticky='ew')
        scrollbar = MyScrollbar(self)
        scrollbar.grid(column=3, row=2, pady=5, sticky='ns')
        self.tdownload = MyText(self, width=55, height=10, yscrollcommand=scrollbar.set)
        self.tdownload.grid(column=0, row=2, columnspan=3, pady=5, sticky='nsew')
        scrollbar.config(command=self.tdownload.yview)
        self.bcancel_download = MyButton(self, text='Cancel', command=self.cancelDownload)
        self.bcancel_download.grid(column=0, row=3, sticky='w')
        self.lstatus = MyLabel(self)
        self.lstatus.grid(column=1, row=3)
        self.bsave_download = MyButton(self, text='Download', command=self.saveDownload)
        self.bsave_download.grid(column=2, row=3, sticky='e')
        self.tdownload.config(state=DISABLED)
        self.lstatus.grid_forget()
        self.scanDownload()

    def scanDownload(self):
        #  Scan input fields for data before enabling buttons.
        try:
            state = str(self.bsave_download['state'])
        except TclError:
            return
        if not self.edownload_url.get() == '' and not self.edownload_dir.get() == '':
            if state == 'disabled':
                self.bsave_download.config(state=NORMAL)
                self.edownload_url.config(state=NORMAL)
                self.edownload_dir.config(state=NORMAL)
        else:
            self.bsave_download.config(state=DISABLED)
        #  Create id for receiving kill signal.
        self.scan_id = self.after(100, self.scanDownload)

    def cancelDownload(self):
        #  Signal scanDownload and listen_for_result to exit.
        #  self.listen_id is only valid when a download has been started.
        self.after_cancel(self.scan_id)
        try:
            self.after_cancel(self.listen_id)
        #  User pressed cancel without starting a download.
        except AttributeError:
            pass
        #  Forcibly kill download processes; suppress stderr and stdout to console.
        os.system('killall youtube-dl >/dev/null 2>&1')
        os.system('killall streamlink >/dev/null 2>&1')
        self.destroy()

    def saveDownload(self):
        '''   Start download in separate thread.   '''
        #  Create thread queue to monitor output from thread.
        self.thread_queue = queue.Queue()
        #  Create thread and pass thread queue.
        self.thread = threading.Thread(target=self.downloop, args=(self.thread_queue, self.edownload_url.get(), self.edownload_dir.get()))
        self.thread.start()
        #  Signal scanDownload to exit.
        self.after_cancel(self.scan_id)
        #  Disable download button.
        self.bsave_download.config(state=DISABLED)
        #  Call listener method.
        self.listen_for_result()

    def downloop(self, thread_queue, url, path):
        '''   Download runs in own thread; output is appended to thread queue.   '''
        path = os.path.abspath(path)
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

    def listen_for_result(self):
        '''   Keep listening for updated output download process.   '''
        #  Monitor thread output; quit if thread has exited.
        self.thread.result_queue = self.thread_queue
        if 'stopped' in str(self.thread):
            self.lstatus.config(text='Download finished.')
            self.scanDownload()
            return
        ###
        self.tdownload.config(state=NORMAL)
        self.edownload_url.config(state=DISABLED)
        self.edownload_dir.config(state=DISABLED)
        self.lstatus.grid(column=1, row=3)
        self.lstatus.config(text='Downloading...')

        try:
            #  Capturing an output stream, so we need to loop.
            while True:
                #  Retrieve the output from thread queue and insert into text widget.
                self.res = self.thread_queue.get(0)
                self.tdownload.insert(END, self.res)
                self.tdownload.see(END)
        except queue.Empty:
            #  No updated output from stream, so keep looping.
            self.listen_id = self.after(100, self.listen_for_result)
    