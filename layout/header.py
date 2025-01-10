import curses
from db.db_reader import DBReader

class Header:
    def __init__(self, s):
        #init
        self.s = s
        self.s.nodelay(True)
        self.s.timeout(100)
        self.s.keypad(True)

        #set user data
        self.userData = 0
        self.SetUserData()

        #set text
        self.ChangeTitle("=====Title=====")

    #change the title
    def ChangeTitle(self, inTitle):
        self.s.clear()
        self.SetUserData()
        self.s.addstr(1, 20, inTitle)
        self.s.refresh()

    #reread and set the user data
    def SetUserData(self):
        db = DBReader()
        condition = "ID = 0"
        sql = {
            "table": "user",
            "condition": condition
        }
        userData = db.ReadData(sql)

        level = userData[0][2] / 1000
        money = userData[0][3]
        self.s.addstr(0, 0, f"Level: {1 + level:.0f}")
        self.s.addstr(0, 40, f"Money: {money}")

        self.userData = userData
        return