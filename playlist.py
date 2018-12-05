# file: playlist.py
from dblib import Db

class Playlist:
    def __init__(self, name=None, address=None):
        db = Db()
        self.conn = db.connection
        self.cur = db.cursor
        self.name = name
        self.address = address

    def savePlaylist(self):
        self.cur.execute('insert into url (name, address) values (?,?)', (self.name, self.address))
        self.conn.commit()

    def loadPlaylist(self):
        playlist = []
        values = self.cur.execute('select name from url')
        for value in values:
            playlist.append(value)
        return playlist

    def selectPlaylist(self, value):
        self.address = self.cur.execute('select address from url where name=?', value)
        for addr in self.address:
            return '{}'.format(addr[0])
