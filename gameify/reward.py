import curses
from db.db_reader import DBReader
from db.db_editer import DBEditer

class Reward:
    def __init__(self, task, mode, header, body, footer, sound):
        self.task = task
        self.mode = mode
        
        #screens/windows
        self.header = header
        self.body = body
        self.footer = footer
        self.sound = sound

        self.items = self.ReadData()
        self.GiveRewards()

        #init funcs
        self.sound.PlaySound("com")
        self.InitScreen()
        self.MainLoop()

    #init screen
    def InitScreen(self):
        #header
        self.header.ChangeTitle(f"Rewards for {self.task[1]}:")

        #body
        self.body.s.clear()
        i = 0
        for item in self.items:
            string = f"{item[4]} {item[3]}"
            self.body.s.addstr(i, 1, string)
            i = i + 1
        self.body.s.move(0, 0)

        #footer
        self.footer.ChangeFooter("Back (Q)")
        
        self.body.s.refresh()

    
    def MainLoop(self):
        option = 0
        while True:
            input = self.body.s.getch()
            if input == ord('w'):
                option = option - 1
                self.sound.PlaySound("nav")
            elif input == ord('s'):
                option = option + 1
                self.sound.PlaySound("nav")
            elif input == 10: #enter
                self.sound.PlaySound("bac")
                break
            elif input == ord('q'):
                self.sound.PlaySound("bac")
                break
            
            #vertical bounds (zero friendly)
            if option >= len(self.items):
                option = len(self.items) - 1
            if option < 0:
                option = 0
            
            #move cursor
            self.body.s.move(option, 0)
            self.body.s.refresh()
    

    def ReadData(self):
        db = DBReader()

        condition = f"mode = '{self.mode}' AND taskID = {self.task[0]}"
        sql = {
            "table": "reward",
            "condition": condition
        }

        info = db.ReadData(sql)
        return info
    
    def GiveRewards(self):
        userdata = self.GetUserData()
        money = userdata[0][3]
        xp = userdata[0][2]
        
        for item in self.items:
            if item[3] == "xp":
                self.EditData("xp", xp + item[4])
            elif item[3] == "money":
                self.EditData("money", money + item[4])
        return
    
    def EditData(self, rType, amount):
        db = DBEditer()

        rSet = f"{rType} = {amount}"
        condition = f"id = 0"
        sql = {
            "table": "user",
            "set": rSet,
            "condition": condition
        }
        db.EditData(sql)
    
    def GetUserData(self):
        db = DBReader()

        condition = f"ID = 0"
        sql = {
            "table": "user",
            "condition": condition
        }

        info = db.ReadData(sql)
        return info