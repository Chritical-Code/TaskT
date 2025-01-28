import curses
import time
from db.db_editer import DBEditer
from gameify.reward import Reward

class TimedTask:
    def __init__(self, task, header, body, footer, sound):
        self.task = task
        self.items = ["Start", "Stop", "Finish"]

        #screens
        self.header = header
        self.body = body
        self.footer = footer
        self.sound = sound

        #timer
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.timer = ""
        self.doTimer = False
        self.InitSeconds()

        #init
        self.InitScreen()
        self.MainLoop()

    #init screen
    def InitScreen(self):
        #header
        self.header.ChangeTitle(self.task[1])

        #body
        self.body.s.clear()
        i = 0
        for item in self.items:
            self.body.s.addstr(i, 0, item)
            i = i + 1
        self.body.s.move(0, (len(self.items[0])))

        #timer
        self.body.s.addstr(len(self.items) + 1, 0, self.GetTimer())

        #footer
        self.footer.ChangeFooter("Back (Q) - Select (Enter)")
        
        self.body.s.refresh()

    
    def MainLoop(self):
        option = 0
        counter = 0
        lastTime = time.time()
        thisTime = time.time()

        while True:
            input = self.body.s.getch()
            if input == ord('w'):
                option = option - 1
                self.sound.PlaySound("nav")
            elif input == ord('s'):
                option = option + 1
                self.sound.PlaySound("nav")
            elif input == 10: #enter
                if option == 0: #start
                    self.doTimer = True
                    self.sound.PlaySound("sel")
                elif option == 1: #stop
                    self.doTimer = False
                    self.DB_SaveTimer()
                    self.sound.PlaySound("sel")
                elif option == 2: #finish
                    self.DB_SaveTimer()
                    self.DB_FinishTask()
                    self.GiveRewards(self.task)
                    break
            elif input == ord('q'):
                self.DB_SaveTimer()
                self.sound.PlaySound("bac")
                break
            
            #vertical bounds
            if option < 0:
                option = 0
            if option >= len(self.items):
                option = len(self.items) - 1

            #timer
            lastTime = thisTime
            thisTime = time.time()
            counter = counter + (thisTime - lastTime)
            if self.doTimer:
                if counter >= 1:
                    counter = counter - 1
                    self.SubtractSecond()
                self.body.s.addstr(len(self.items) + 1, 0, self.GetTimer())
            else:
                counter = 0
            
            #move cursor
            self.body.s.move(option, (len(self.items[option])))
            self.body.s.refresh()

            if self.doTimer:
                time.sleep(.01)
            

    def GetTimer(self):
        if self.seconds < 10:
            seconds = "0" + str(self.seconds)
        else:
            seconds = str(self.seconds)

        if self.minutes < 10:
            minutes = "0" + str(self.minutes)
        else:
            minutes = str(self.minutes)

        if self.hours < 10:
            hours = "0" + str(self.hours)
        else:
            hours = str(self.hours)
        
        self.timer = hours + ":" + minutes + ":" + seconds
        return str(self.timer)
    
    def SubtractSecond(self):
        self.seconds = self.seconds - 1
        
        if self.seconds < 0:
            self.seconds = 59
            self.minutes = self.minutes - 1
            if self.minutes < 0:
                self.minutes = 59
                self.hours = self.hours - 1
        
        if self.minutes < 0 or self.hours < 0 or self.seconds < 0:
            self.seconds = 0
            self.minutes = 0
            self.hours = 0
        
    def InitSeconds(self):
        self.seconds = self.task[3]
        while self.seconds > 59:
            self.minutes = self.minutes + 1
            self.seconds = self.seconds - 60
            while self.minutes > 59:
                self.hours = self.hours + 1
                self.minutes = self.minutes - 60
    
    def DB_SaveTimer(self):
        db = DBEditer()

        rSet = f"remainingTime = {self.GetRemainingTime()}"
        condition = f"id = {self.task[0]}"
        sql = {
            "table": "timedTask",
            "set": rSet,
            "condition": condition
        }
        db.EditData(sql)
    
    def GetRemainingTime(self):
        return (self.hours * 60 * 60) + (self.minutes * 60) + self.seconds
    
    def DB_FinishTask(self):
        db = DBEditer()

        rSet = f"done = {True}"
        condition = f"id = {self.task[0]}"
        sql = {
            "table": "timedTask",
            "set": rSet,
            "condition": condition
        }
        db.EditData(sql)

    def GiveRewards(self, task):
        rw = Reward(task, "timedTask", self.header, self.body, self.footer, self.sound)
        self.InitScreen()

    