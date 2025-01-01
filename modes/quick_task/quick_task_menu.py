import curses
import random
from db.db_reader import DBReader
from gameify.reward import Reward

class QuickTaskMenu:
    def __init__(self, header, body, footer, sound):
        self.items = ["Your task is..."]
        self.tasks = self.ReadData()
        self.completed = []

        #screens
        self.header = header
        self.body = body
        self.footer = footer
        self.sound = sound

        #init funcs
        self.InitScreen()
        self.MainLoop()

    #init screen
    def InitScreen(self):
        #header
        self.header.ChangeTitle("Quick Task")

        #body
        self.body.s.clear()
        i = 0
        for item in self.items:
            self.body.s.addstr(i, 1, item)
            i = i + 1
        self.body.s.move(0, 0)

        #footer
        self.footer.ChangeFooter("Back (Q) - Randomize (Spacebar) - Complete (Enter)")
        
        #move cursor to 1
        self.body.s.refresh()

    
    def MainLoop(self):
        option = 0
        currentTask = 999999999
        while True:
            input = self.body.s.getch()
            if input == ord('w'):
                option = option - 1
                self.sound.PlaySound("nav")
            elif input == ord('s'):
                option = option + 1
                self.sound.PlaySound("nav")
            elif input == 10: #enter
                if len(self.tasks) > currentTask and len(self.tasks) > 0:
                    self.GiveRewards(self.tasks[currentTask])
                    self.completed.append(self.tasks[currentTask])
                    self.tasks.pop(currentTask)
                    currentTask = 999999999
                    self.body.s.move(0, 0)
                    self.body.s.clrtoeol()
                    self.body.s.addstr(0, 1, "Task Complete!")
            elif input == 32: #spacebar
                self.sound.PlaySound("sel")
                self.body.s.move(0, 0)
                self.body.s.clrtoeol()
                if len(self.tasks) > 0:
                    currentTask = random.randint(0, len(self.tasks) - 1)
                    self.body.s.addstr(0, 1, self.tasks[currentTask][1])
                else:
                    self.body.s.addstr(0, 1, "All tasks complete :)")
            elif input == ord('q'):
                self.sound.PlaySound("bac")
                break
            
            #vertical bounds
            if option < 0:
                option = 0
            if option >= len(self.items):
                option = len(self.items) - 1
            
            #move cursor
            self.body.s.move(0, 0)
            self.body.s.refresh()
    

    def ReadData(self):
        db = DBReader()

        condition = "done = 0"
        sql = {
            "table": "quickTask",
            "condition": condition
        }

        info = db.ReadData(sql)
        return info
    
    def GiveRewards(self, task):
        rw = Reward(task, self.header, self.body, self.footer, self.sound)
        self.InitScreen()