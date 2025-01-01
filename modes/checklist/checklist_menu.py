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
        self.items = self.ReadData()
        self.sound = sound

        #init functions
        self.InitScreen()
        self.MainLoop()

    #init screen
    def InitScreen(self):
        #header
        self.header.ChangeTitle("Checklists")
        
        #body
        self.body.s.clear()
        i = 0
        for item in self.items:
            self.body.s.addstr(i, 0, item[1])
            i = i + 1

        #footer
        self.footer.ChangeFooter("Back (Q) - Select (Enter) - Edit (H)")
        
        #move cursor to 1
        self.body.s.move(0, (len(self.items[0][1])))
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
                self.sound.PlaySound("sel")
                checkL = Checklist(self.items[option][1], self.items[option][0], self.header, self.body, self.footer, self.sound)
                self.InitScreen()
            elif input == ord('h'):
                self.sound.PlaySound("sel")
                stayEdit = True
                while stayEdit:
                    editCL = EditChecklist(self.items[option], self.header, self.body, self.footer, self.sound)
                    self.InitScreen()
                    stayEdit = editCL.stayEdit
            elif input == ord('q'):
                self.sound.PlaySound("bac")
                break
            
            #vertical bounds
            if option < 0:
                option = 0
            if option >= len(self.items):
                option = len(self.items) - 1
            
            #move cursor
            self.body.s.move(option, (len(self.items[option][1])))
            self.body.s.refresh()
    
    def ReadData(self):
        db = DBReader()

        condition = "5 = 5"
        sql = {
            "table": "checklist",
            "condition": condition
        }

        info = db.ReadData(sql)
        return info