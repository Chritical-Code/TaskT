import curses
from db.db_reader import DBReader
from db.db_adder import DBAdder
from db.db_deleter import DBDeleter

class EditChecklist:
    
    def __init__(self, cL, header, body, footer, sound):
        self.cL = cL
        self.items = self.ReadData()
        self.newline = len(self.items) + 1 + 6
        self.stayEdit = True

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
        #header
        self.header.ChangeTitle("Editing " + self.cL[1])

        #body
        self.body.s.clear()
        i = 0
        for item in self.items:
            self.body.s.addstr(i, 0, item[1])
            i = i + 1
        self.body.s.move(0, self.GetCursorPos(0))
        self.body.s.refresh()

        #footer
        self.footer.ChangeFooter("Back (Q) - Add (H) - Delete (X)")

    
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
            elif input == ord('h'):
                self.sound.PlaySound("sel")
                self.AddMode()
                self.sound.PlaySound("sel")
                break
            elif input == ord('x'):
                self.sound.PlaySound("bac")
                self.DeleteItem(option)
                break
            elif input == ord('q'):
                self.sound.PlaySound("bac")
                self.stayEdit = False
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

        condition = "checklistID = " + str(self.cL[0])
        sql = {
            "table": "task",
            "condition": condition
        }

        info = db.ReadData(sql)
        return info
    
    #mode that lets you add an item to the list
    def AddMode(self):
        #init
        curses.echo()
        self.body.s.nodelay(False)
        self.body.s.timeout(-1)
        self.body.s.move(len(self.items), 0)
        
        #do
        inString = self.body.s.getstr().decode('utf-8')

        #add to db
        db = DBAdder()
        columns = "name, checklistID, done"
        values = f"'{inString}', {str(self.cL[0])}, {0}"
        sql = {
            "table": "task",
            "columns": columns,
            "values": values
        }
        db.AddData(sql)
        
        #unnit
        curses.noecho()
        self.body.s.nodelay(True)
        self.body.s.timeout(100)

    def DeleteItem(self, option):
        db = DBDeleter()
        
        condition = f"ID = {self.items[option][0]}"
        sql = {
            "table": "task",
            "condition": condition
        }
        db.DeleteData(sql)

    def GetCursorPos(self, option):
        if len(self.items) > 0:
            return len(self.items[option][1])
        else:
            return 0