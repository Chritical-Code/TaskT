import os
import curses

class Colors:
    def __init__(self, header, body, footer):
        #colors
        curses.init_color(1, 0, 1000, 0) #green
        curses.init_color(2, 1000, 1000, 1000) #white
        curses.init_color(3, 100, 100, 100) #almost black
        curses.init_color(4, 150, 150, 150) #almost almost black
        curses.init_color(5, 0, 0, 0) #black
        curses.init_color(6, 168, 254, 383) #dark blue
        curses.init_color(7, 957, 938, 961) #offwhite
        curses.init_color(8, 559, 457, 309) #dark brorange
        curses.init_color(9, 996, 219, 996) #neon pink
        curses.init_color(10, 800, 800, 800) #dark white
        curses.init_color(11, 949, 559, 965) #pink
        curses.init_color(12, 793, 395, 805) #dark pink
        curses.init_color(13, 945, 781, 953) #light pink
        curses.init_color(14, 645, 328, 656) #darker pink



        #pairs
        #theme darkmode 2 3 2
        curses.init_pair(2, 2, 3)
        curses.init_pair(3, 2, 4)

        #theme bluebrownwhite 4 5 6
        curses.init_pair(4, 2, 6)
        curses.init_pair(5, 5, 7)
        curses.init_pair(6, 5, 8)

        #theme blacknpink 7 7 7
        curses.init_pair(7, 9, 5)

        #theme lightmode 8 9 8
        curses.init_pair(8, 2, 4)
        curses.init_pair(9, 5, 2)

        #theme extrapink 10 11 10
        curses.init_pair(10, 7, 12)
        curses.init_pair(11, 2, 11)

        #set colors
        #header.bkgd(' ', curses.color_pair(10))
        #body.bkgd(' ', curses.color_pair(11))
        #footer.bkgd(' ', curses.color_pair(10))