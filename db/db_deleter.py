import curses
import sqlite3

class DBDeleter:
    def __init__(self):
        self = self
        self.con  = sqlite3.connect("productivity.db")
        self.cur = self.con.cursor()
    

    def DeleteData(self, sql):
        string = f"DELETE FROM {sql['table']} WHERE {sql['condition']}"
        self.cur.execute(string)
        self.con.commit()
        self.con.close()