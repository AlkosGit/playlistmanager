# file: main.py
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
