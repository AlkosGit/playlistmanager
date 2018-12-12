# file: playlist.py
from dblib import Db

class Playlist:
    def __init__(self, name=None, address=None, description=None):
        self.name = name
        self.address = address
        self.description = description
        db = Db()
        self.conn = db.connection
        self.cur = db.cursor

    def createDB(self):
        self.cur.execute('create table url (id int(6) PRIMARY KEY, name varchar(64), address varchar(250), description varchar(250))')
        self.conn.commit()

    def savePlaylist(self):
        self.cur.execute('insert into url (name, address, description) values (?,?,?)', (self.name, self.address, self.description))
        self.conn.commit()

    def loadPlaylist(self):
        playlist = []
        values = self.cur.execute('select id, name from url')
        for pid, value in values:
            playlist.append(str(pid) + ' ' + value) #  return pid (db.id) as pk
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
        self.cur.execute('delete from url where id=' + playlist[0]) #  delete on pk
        self.conn.commit()
