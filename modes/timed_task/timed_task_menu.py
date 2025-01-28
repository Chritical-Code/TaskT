import curses
from modes.timed_task.timed_task import TimedTask
from db.db_reader import DBReader


class TimedTaskMenu:
    def __init__(self, header, body, footer, sound):
        self.hidden = False
        self.title = "Timed Tasks"
        self.items = self.ReadData()

        #screens
        self.header = header
        self.body = body
        self.footer = footer
        self.sound = sound

        #init
        self.InitScreen()
        self.MainLoop()

    #init screen
    def InitScreen(self):
        #re-read data
        self.items = self.ReadData()

        #header
        self.header.ChangeTitle(self.title)

        #body
        self.body.s.clear()
        i = 0
        for item in self.items:
            self.body.s.addstr(i, 0, item[1])
            i = i + 1
        self.body.s.move(0, self.GetCursorPos(0))

        #footer
        self.footer.ChangeFooter("Back (Q) - Select (Enter) - Toggle Hidden (H)")
        
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
                if len(self.items) > 0:
                    self.sound.PlaySound("sel")
                    timedT = TimedTask(self.items[option], self.header, self.body, self.footer, self.sound)
                    self.InitScreen()
            elif input == ord('h'): #hidden
                self.sound.PlaySound("sel")
                self.hidden = not(self.hidden)
                if self.hidden:
                    self.title = "Timed Tasks (Hidden)"
                else:
                    self.title = "Timed Tasks"
                self.InitScreen()
            elif input == ord('q'):
                self.sound.PlaySound("bac")
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

        condition = "5 = 5"
        sql = {
            "table": "timedTask",
            "condition": condition
        }
        info = db.ReadData(sql)

        rinsedInfo = []
        for inf in info:
            if inf[4] == self.hidden:
                rinsedInfo.append(inf)

        return rinsedInfo
    
    def GetCursorPos(self, option):
        if len(self.items) > 0:
            return len(self.items[option][1])
        else:
            return 0
    