# file: dblib.py
import sqlite3
import glob

class Db:
    def __init__(self):
        dbfile = [file for file in glob.glob('playlist.db')]
        if not dbfile:
            self.createDB() 
        else:
            self.connection = sqlite3.connect('playlist.db')
            self.cursor = self.connection.cursor()
        
    def createDB(self):
        self.connection = sqlite3.connect('playlist.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('create table url (id INTEGER PRIMARY KEY,'\
                'name varchar(64),'\
                'address varchar(250),'\
                'description varchar(250),'\
                'resume int,'\
                'shuffle int)')
        self.connection.commit()
