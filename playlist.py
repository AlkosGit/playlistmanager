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
        values = self.cur.execute('select id, name from url')
        for pid, value in values:
            playlist.append(str(pid) + ' ' + value) #  return pid (db.id) as pk
        return playlist

    def selectPlaylist(self, value):
        playlist = value.split()
        self.address = self.cur.execute('select address from url where id=' + playlist[0]) #  select on pk
        for addr in self.address:
            return '{}'.format(addr[0])

    def deletePlaylist(self, value):
        playlist = value.split()
        self.cur.execute('delete from url where id=' + playlist[0]) #  delete on pk
        self.conn.commit()
