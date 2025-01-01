import curses

class Body:
    def __init__(self, s):
        self.s = s
        self.s.addstr(0, 20, "Body")
        self.s.nodelay(True)
        self.s.timeout(100)
        self.s.keypad(True)
        self.s.refresh()
