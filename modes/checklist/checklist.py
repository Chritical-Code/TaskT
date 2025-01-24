import curses
from db.db_reader import DBReader
from db.db_editer import DBEditer
from gameify.reward import Reward

class Checklist:
    
    def __init__(self, checklist, header, body, footer, sound):
        self.checklist = checklist
        
        #screens
        self.header = header
        self.body = body
        self.footer = footer
        self.sound = sound

        self.items = self.ReadData()
        
        #init
        self.InitScreen()
        self.MainLoop()

    #init screen
    def InitScreen(self):
        #header
        self.header.ChangeTitle(self.checklist[1])

        #body
        self.body.s.clear()
        i = 0
        for item in self.items:
            mark = " "
            if item[3]:
                mark = "X"
            self.body.s.addstr(i, 0, mark)
            self.body.s.addstr(i, 2, item[1])
            i = i + 1
        self.body.s.move(0, self.GetCursorPos(0))

        #footer
        self.footer.ChangeFooter("Back (Q) - Check (Enter)")
        
        #move cursor to 1
        self.body.s.refresh

    
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
                if len(self.items) > 0:
                    if self.items[option][3]:
                        self.EditData(self.items[option][0], False)
                        self.items = self.ReadData()
                        self.sound.PlaySound("bac")
                        self.body.s.addstr(option, 0, " ")
                    else:
                        self.EditData(self.items[option][0], True)
                        self.items = self.ReadData()
                        self.sound.PlaySound("com")
                        self.body.s.addstr(option, 0, "X")
            elif input == ord('q'):
                self.sound.PlaySound("bac")
                break

            #reward and close if list is complete
            complete = True
            for item in self.items:
                if not(item[3]):
                    complete = False
            if complete:
                self.GiveRewards(self.checklist) #give rewards
                break
            
            #vertical bounds (zero friendly)
            if option >= len(self.items):
                option = len(self.items) - 1
            if option < 0:
                option = 0
            
            #move cursor
            self.body.s.move(option, self.GetCursorPos(option))
            self.body.s.refresh()
    
    def ReadData(self):
        db = DBReader()

        condition = "checklistID = " + str(self.checklist[0])
        sql = {
            "table": "task",
            "condition": condition
        }

        info = db.ReadData(sql)
        return info
    
    def EditData(self, taskID, doneness):
        db = DBEditer()

        rSet = f"done = {doneness}"
        condition = f"id = {taskID}"
        sql = {
            "table": "task",
            "set": rSet,
            "condition": condition
        }
        db.EditData(sql)
    
    def GetCursorPos(self, option):
        if len(self.items) > 0:
            return len(self.items[option][1]) + 2
        else:
            return 2
        
    def GiveRewards(self, task):
        rw = Reward(task, "checklist", self.header, self.body, self.footer, self.sound)
        self.InitScreen()
    