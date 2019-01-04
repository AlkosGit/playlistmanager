# file: playlistmanager/main.py
from tkinter import *
from style import *

class Window:
    def __init__(self):
        self.root = Tk(className='playlistmanager')
        self.root.protocol('WM_DELETE_WINDOW', self.root.quit())
        self.root.title('Playlist Manager')
        #  Make window appear centered on screen.
        self.width, self.height = 800, 500
        x = (self.root.winfo_screenwidth() / 2) - (self.width /2)
        y = (self.root.winfo_screenheight() /2) - (self.height / 2)
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))
        #  Create filemenu.
        self.menubar = MyMenu(self.root)
        self.filemenu = MyMenu(self.menubar)
        self.filemenu.add_command(label='New playlist', command=self.new)
        self.filemenu.add_command(label='Download playlist', command=self.download)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.root.destroy)
        self.aboutmenu = MyMenu(self.menubar) 
        self.aboutmenu.add_command(label='Help', command=self.showhelp)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.menubar.add_cascade(label='About', menu=self.aboutmenu)
        self.root.config(menu=self.menubar, background='#444444')
        #  Create mainframe.
        self.mainframe = MyFrame(self.root)
        #  Player is main window.
        self.player()

    def showhelp(self):
        import helpdoc
        helpdoc.Help()

    def switchFrame(self):
        #  Destroy and recreate mainframe.
        #  Wrap in try statement to suppress errormessages on application quit.
        try:
            self.mainframe.destroy()
            self.mainframe = MyFrame(self.root)
            self.mainframe.pack(fill=BOTH, expand=True)
        except TclError: return

    def player(self):
        '''   This is the main window.  '''
        self.switchFrame()
        from player import Player
        #  Wrap in try statement to suppress errormessages on application quit.
        try:
            p = Player(self.mainframe)
            p.pack(fill=BOTH, expand=True)
        except TclError: return
        self.root.wait_window(p)
        self.player()
        
    def new(self):
        '''   Create new playlist. 
        If mode = "edit" same window is used to edit existing playlist.   '''
        self.switchFrame()
        from new import New
        n = New(self.mainframe)
        n.pack(fill=BOTH, expand=True, padx=10, pady=5)
        self.root.wait_window(n)
        self.player()
        
    def download(self):
        self.switchFrame()
        from download import Download
        d = Download(self.mainframe)
        d.pack(fill=BOTH, expand=True, padx=10, pady=5)
        self.root.wait_window(d)
        self.player()

if __name__ == '__main__':
    Window()
    # mainloop()
    #  Wrap in try statement to suppress errormessages on application quit.
    # try:
    #     mainloop()
    # except AttributeError: pass
