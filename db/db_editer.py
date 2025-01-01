import curses
import sqlite3

class DBEditer:
    def __init__(self):
        self = self
        self.con  = sqlite3.connect("productivity.db")
        self.cur = self.con.cursor()
    

    def EditData(self, sql):
        string = f"UPDATE {sql['table']} SET {sql['set']} WHERE {sql['condition']}"
        self.cur.execute(string)
        self.con.commit()
        self.con.close()