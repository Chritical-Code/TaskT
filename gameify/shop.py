import curses
from db.db_reader import DBReader

class Shop:
    
    def __init__(self, header, body, footer, sound):
        self.data = self.ReadData()
        self.items = self.MakeList()

        #screens/windows
        self.header = header
        self.body = body
        self.footer = footer
        self.sound = sound

        self.level = 0
        self.money = 0
        self.ReadUserData()

        #init funcs
        self.InitScreen()
        self.MainLoop()

    #init screen
    def InitScreen(self):
        #header
        self.header.ChangeTitle("Shop")
        
        #body
        self.body.s.clear()
        i = 0
        for item in self.items:
            self.body.s.addstr(i, 0, item)
            i = i + 1
        self.body.s.move(0, (len(self.items[0])))

        #footer
        self.footer.ChangeFooter("Back (Q) - Buy (Enter)")
        
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
                self.sound.PlaySound("com")
                x = 0
                #buy that thang
            elif input == ord('q'):
                self.sound.PlaySound("bac")
                break
            
            #vertical bounds
            if option < 0:
                option = 0
            if option >= len(self.items):
                option = len(self.items) - 1
            
            #move cursor
            self.body.s.move(option, (len(self.items[option])))
            self.body.s.refresh()
    
    def ReadData(self):
        db = DBReader()

        condition = "5 = 5"
        sql = {
            "table": "shopItem",
            "condition": condition
        }

        info = db.ReadData(sql)
        return info
    
    def MakeList(self):
        items = []
        for dat in self.data:
            string = f"{dat[2]} - {dat[1]}"
            items.append(string)
        return items
    
    def ReadUserData(self):
        db = DBReader()

        condition = "ID = 0"
        sql = {
            "table": "user",
            "condition": condition
        }
        userData = db.ReadData(sql)
        self.level = userData[0][2] / 1000
        self.money = userData[0][3]
