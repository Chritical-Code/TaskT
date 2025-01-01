import curses
import sqlite3

class DBReader:
    def __init__(self):
        self = self
        self.con  = sqlite3.connect("productivity.db")
        self.cur = self.con.cursor()
    

    def ReadData(self, sql):
        string = "SELECT * FROM " + sql["table"] + " WHERE " + sql["condition"]
        records = self.cur.execute(string)
        
        info = []
        for record in records:
            info.append(record)
        
        self.con.close()
        return info