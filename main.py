import curses
from modes.checklist.checklist_menu import ChecklistMenu
from modes.timed_task.timed_task_menu import TimedTaskMenu
from modes.quick_task.quick_task_menu import QuickTaskMenu
from db.db_reader import DBReader
from gameify.shop import Shop


class Main:
    
    #constructor
    def __init__(self, header, body, footer, sound):
        self.items = ["Checklist", "Timed Task", "Quick Task", "Shop"]
        self.level = 0
        self.money = 0

        #screens/windows
        self.header = header
        self.body = body
        self.footer = footer
        self.sound = sound

        #init functions
        self.InitCurses()
        self.InitScreen()
        self.MainLoop()
    
    #main loop
    def MainLoop(self):
        #user input
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
                if option == 0:
                    check = ChecklistMenu(self.header, self.body, self.footer, self.sound)
                    self.InitScreen()
                elif option == 1:
                    time = TimedTaskMenu(self.header, self.body, self.footer, self.sound)
                    self.InitScreen()
                elif option == 2:
                    quick = QuickTaskMenu(self.header, self.body, self.footer, self.sound)
                    self.InitScreen()
                elif option == 3:
                    shop = Shop(self.header, self.body, self.footer, self.sound)
                    self.InitScreen()
            elif input == 27: #esc
                self.sound.PlaySound("bac").wait_done()
                break
            
            #vertical bounds
            if option < 0:
                option = 0
            if option >= len(self.items):
                option = len(self.items) - 1

            #move cursor
            self.body.s.move(option, (len(self.items[option])))
            self.body.s.refresh()

    #defined functions
    #initialize curses
    def InitCurses(self):  
        curses.noecho()
        curses.cbreak()
        self.body.s.nodelay(True)
        self.body.s.timeout(100)
        self.body.s.keypad(True)

    #initialize the screen menu
    def InitScreen(self):
        #header
        self.header.ChangeTitle("Main Menu")
        self.header.s.addstr(0, 0, f"Level: {1 + self.level:.0f}")
        self.header.s.addstr(0, 40, f"Money: {self.money}")

        #body
        self.body.s.clear()
        i = 0
        for item in self.items:
            self.body.s.addstr(i, 0, item)
            i = i + 1
        self.body.s.move(0, (len(self.items[0])))

        #footer
        self.footer.ChangeFooter("Exit (Esc) - Select (Enter)")

        self.body.s.refresh()

    def EndApp(self):
        #end the app
        curses.nocbreak()
        self.body.s.keypad(False)
        curses.echo()
        curses.endwin()

    def ReadData(self):
        db = DBReader()

        condition = "ID = 0"
        sql = {
            "table": "user",
            "condition": condition
        }
        userData = db.ReadData(sql)
        self.level = userData[0][2] / 1000
        self.money = userData[0][3]
