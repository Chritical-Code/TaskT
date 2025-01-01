import curses
import sqlite3

class DBAdder:
    def __init__(self):
        self = self
        self.con  = sqlite3.connect("productivity.db")
        self.cur = self.con.cursor()
    

    def AddData(self, sql):
        string = f"INSERT INTO {sql['table']} ({sql['columns']}) VALUES({sql['values']})"
        self.cur.execute(string)
        self.con.commit()
        self.con.close()