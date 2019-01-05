# file: playlistmanager/play.py
from playlist import Playlist
import subprocess
import threading, queue

class Play:
    def __init__(self, value, resume=None, shuffle=None, mode=None):
        '''   Start player in separate thread.   '''
        self.value = value
        self.resume = resume
        self.shuffle = shuffle
        self.mode = mode
        self.playlist = Playlist()
        #  Retrieve url or mediafile from selected playlist.
        if self.mode == 'quickplay':
            self.url = self.value
        else:
            self.url = self.playlist.selectPlaylist(self.value)
        #  Create thread queue to monitor output from thread.
        self.thread_queue = queue.Queue()
        #  Create thread and pass thread queue
        self.thread = threading.Thread(target=self.runloop, args=(self.thread_queue, self.resume, self.shuffle))
        self.thread.start()

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
                self.thread_queue.put(output)