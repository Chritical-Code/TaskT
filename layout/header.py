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
        center = int((self.s.getmaxyx()[1] / 2) - (len(inTitle) / 2))
        self.s.addstr(1, center, inTitle)
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

        #level formatting
        level = userData[0][2] / 1000
        self.s.addstr(0, 1, f"Level: {1 + level:.0f}")

        #money formatting
        money = userData[0][3]
        moneyText = f"Money: {money}"
        right = (self.s.getmaxyx()[1]) - len(moneyText) - 1
        self.s.addstr(0, right, moneyText)

        self.userData = userData
        return