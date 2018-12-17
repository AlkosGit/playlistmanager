# file: playlist.py
from dblib import Db
import sqlite3

class Playlist:
    def __init__(self, name=None, address=None, description=None, resume=None, shuffle=None):
        self.name = name
        self.address = address
        self.description = description
        self.resume = resume
        self.shuffle = shuffle
        db = Db()
        self.conn = db.connection
        self.cur = db.cursor

    def savePlaylist(self):
        #  check for empty value
        if not self.address:
            pass
        else:
            #  Youtube playlist url's need to be truncated for mpv.
            if 'youtube.com' and 'list' in self.address:
                url = self.address.rsplit('list=')
                self.address = 'https://www.youtube.com/watch?list={}'.format(url[1])
            self.cur.execute('insert into url (name, address, description, resume, shuffle) values (?,?,?,?,?)',\
                    (self.name, self.address, self.description, self.resume, self.shuffle))
            self.conn.commit()

    def loadPlaylist(self):
        playlist = []
        values = self.cur.execute('select id, name from url')
        for pid, value in values:
            playlist.append(str(pid) + ' ' + value) #  return pid (db.id) as pk
        #  check for empty record.
        if not playlist:
            playlist.append('Database empty!')
        return playlist

    def loadDescription(self, value):
        #  extract pk from value
        playlist = value.split()
        try:
            description = self.cur.execute('select description from url where id=' + playlist[0]) #  select on pk
            for desc in description:
                return '{}'.format(desc[0])
        except sqlite3.OperationalError:
            return 'Please select a playlist, or add a new playlist with File -> New.'
           
    def selectPlaylist(self, value):
        playlist = value.split()
        self.address = self.cur.execute('select address from url where id=' + playlist[0])
        for addr in self.address:
            return '{}'.format(addr[0])

    def resumePlaylist(self, value):
        #  check if resume playback is enabled.
        playlist = value.split()
        try:
            self.resume = self.cur.execute('select resume from url where id=' + playlist[0])
            for resume in self.resume:
                return resume[0]
        except:
            pass
    
    def shufflePlaylist(self, value):
        #  check if shuffle playback is enabled.
        playlist = value.split()
        try:
            self.shuffle = self.cur.execute('select shuffle from url where id=' + playlist[0])
            for shuffle in self.shuffle:
                return shuffle[0]
        except:
            pass
    
    def deletePlaylist(self, value):
        playlist = value.split()
        try:
            self.cur.execute('delete from url where id=' + playlist[0])
        except (sqlite3.OperationalError, IndexError):
            pass
        self.conn.commit()
