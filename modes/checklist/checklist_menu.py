import curses
from modes.checklist.checklist import Checklist
from db.db_reader import DBReader
from modes.checklist.editChecklist import EditChecklist

class ChecklistMenu:
    
    def __init__(self, header, body, footer, sound):
        #init screens
        self.header = header
        self.body = body
        self.footer = footer
        self.sound = sound
        self.hidden = False
        self.items = self.ReadData()

        #init functions
        self.InitScreen()
        self.MainLoop()

    #init screen
    def InitScreen(self):
        self.items = self.ReadData()
        
        #header
        self.header.ChangeTitle("Checklists")
        
        #body
        self.body.s.clear()
        i = 0
        for item in self.items:
            self.body.s.addstr(i, 0, item[1])
            i = i + 1

        #footer
        self.footer.ChangeFooter("Back (Q) - Select (Enter) - Edit (E) - Toggle Hidden (H)")
        
        #move cursor to 1
        self.body.s.move(0, self.GetCursorPos(0))
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
            elif input == 10: #enter open
                if len(self.items) > 0:
                    self.sound.PlaySound("sel")
                    checkL = Checklist(self.items[option], self.header, self.body, self.footer, self.sound)
                    self.InitScreen()
            elif input == ord('e'): #edit
                if len(self.items) > 0:
                    self.sound.PlaySound("sel")
                    stayEdit = True
                    while stayEdit:
                        editCL = EditChecklist(self.items[option], self.header, self.body, self.footer, self.sound)
                        self.InitScreen()
                        stayEdit = editCL.stayEdit
            elif input == ord('h'): #toggle hidden
                self.hidden = not(self.hidden)
                self.items = self.ReadData()
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
            "table": "checklist",
            "condition": condition
        }

        info = db.ReadData(sql)
        return self.SeperateData(info)
    
    def SeperateData(self, data):
        #read in all tasks
        db = DBReader()

        condition = "5 = 5"
        sql = {
            "table": "task",
            "condition": condition
        }

        tasks = db.ReadData(sql)
        
        #append hidden? items
        rinsedList = []
        i = 0
        for dat in data:
            include = False
            for task in tasks:
                if (task[2] == dat[0]) and not(task[3]):
                    include = True
            if include != self.hidden:
                rinsedList.append(dat)
            i = i + 1

        #return list
        return rinsedList
    
    def GetCursorPos(self, option):
        if len(self.items) > 0:
            return len(self.items[option][1])
        else:
            return 0