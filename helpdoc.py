# file: playlistmanager/help.py
from tkinter import *
from style import *

helptext = """
### Playlistmanager ###
### Written in Python 3.X ###

This application can save playlists (e.g. Youtube) or 
local directories with media files, and play the content 
from those sources. It is also possible to download a 
playlist or media file to the local drive, for viewing off-line.

Playlistmanager uses mpv media player for 
playing media content. Note that mpv is not 
part of this package.

Also, the following third party applications are needed:
    - youtube-dl
    - streamlink

Usage:
The default player window is used to play a playlist.
Click the play button to play the playlist, or the edit
button to edit the playlist.

Click 'file -> new playlist' to create a new playlist.
Insert a name in the name field, and a URL
in the URL field.
The URL can be from a Youtube playlist or a Twitch video.
Note that the Twitch URL needs to be in the
form 'https://www.twitch.tv/video/....'
Optionally, check the resume checkbox to let the player
continue where it left of; check the shuffle checkbox
to shuffle the playlist.

Click 'file -> download playlist' to download a playlist, 
Youtube or Twitch video.
Videos will be saved with a default filename inferred
from the URL. 
"""

class Help:
    def __init__(self):
        self.top = Toplevel()
        self.top.title('Help')
        self.top.config(background='#444444')
        self.width, self.height = 450, 200
        x = (self.top.winfo_screenwidth() / 2) - (self.width /2)
        y = (self.top.winfo_screenheight() /2) - (self.height / 2)
        self.top.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))
        self.makewidgets()
    
    def makewidgets(self):
        self.helpframe = MyFrame(self.top)
        self.helpframe.pack(fill=BOTH, expand=True, pady=5, padx=5)
        self.thelp = MyScrolledText(self.helpframe, wrap=WORD, width=50, height=20, relief='flat')
        self.thelp.vbar.config(background='#444444', activebackground='#333333')
        self.thelp.pack(fill=BOTH, expand=True)
        self.thelp.insert(END, helptext)
        self.top.mainloop()

if __name__ == '__main__':
    Help()
