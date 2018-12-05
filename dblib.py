# file: dblib.py
import sqlite3

class Db:
    def __init__(self):
        self.connection = sqlite3.connect('playlist.db')
        self.cursor = self.connection.cursor()
        
