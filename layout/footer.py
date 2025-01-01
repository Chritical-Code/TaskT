import curses

class Footer:
    def __init__(self, s):
        #init
        self.s = s
        self.s.nodelay(True)
        self.s.timeout(100)
        self.s.keypad(True)

        #set text
        self.ChangeFooter("")
    
    def ChangeFooter(self, inFooter):
        self.s.clear()
        self.s.addstr(1, 0, "Controls:")
        self.s.addstr(2, 0, inFooter)
        #self.s.addstr(2, 0, "Navigate (WASD)")
        self.s.refresh()