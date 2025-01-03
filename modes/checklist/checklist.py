import curses
from db.db_reader import DBReader
from db.db_editer import DBEditer

class Checklist:
    
    def __init__(self, title, clID, header, body, footer, sound):
        self.title = title
        self.clID = clID
        
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
        self.header.ChangeTitle(self.title)

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
        self.body.s.move(0, (len(self.items[0][1]) + 2))

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
            
            #vertical bounds
            if option < 0:
                option = 0
            if option >= len(self.items):
                option = len(self.items) - 1
            
            #move cursor
            self.body.s.move(option, (len(self.items[option][1]) + 2))
            self.body.s.refresh()
    
    def ReadData(self):
        db = DBReader()

        condition = "checklistID = " + str(self.clID)
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
        
    