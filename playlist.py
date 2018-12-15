# file: playlist.py
from dblib import Db
import sqlite3

class Playlist:
    def __init__(self, name=None, address=None, description=None):
        self.name = name
        self.address = address
        self.description = description
        db = Db()
        self.conn = db.connection
        self.cur = db.cursor

    def savePlaylist(self):
        #  Youtube playlist url's need to be truncated for mpv.
        if 'youtube.com' and 'list' in self.address:
            url = self.address.rsplit('list=')
            self.address = 'https://www.youtube.com/watch?list={}'.format(url[1])
        self.cur.execute('insert into url (name, address, description) values (?,?,?)', (self.name, self.address, self.description))
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
        playlist = value.split()
        description = self.cur.execute('select description from url where id=' + playlist[0])
        for desc in description:
            return '{}'.format(desc[0])

    def selectPlaylist(self, value):
        playlist = value.split()
        self.address = self.cur.execute('select address from url where id=' + playlist[0]) #  select on pk
        for addr in self.address:
            return '{}'.format(addr[0])

    def deletePlaylist(self, value):
        playlist = value.split()
        try:
            self.cur.execute('delete from url where id=' + playlist[0]) #  delete on pk
        except (sqlite3.OperationalError, IndexError):
            pass
        self.conn.commit()
