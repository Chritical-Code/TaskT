import curses
import os
from main import Main
from layout.header import Header
from layout.body import Body
from layout.footer import Footer
from style.colors import Colors
from sound.sound import Sound


#init base screen/window
os.system("mode con cols=60 lines=21")
#os.system("chcp 437")
wholeScreen = curses.initscr()
curses.start_color()

#init screens
headerScreen = curses.newwin(3, 60, 0, 0)
bodyScreen = curses.newwin(15, 60, 3, 0)
footerScreen = curses.newwin(3, 60, 18, 0)

#init classes
header = Header(headerScreen)
body = Body(bodyScreen)
footer = Footer(footerScreen)
colors = Colors(headerScreen, bodyScreen, footerScreen)
sound = Sound()

#start the main program
m = Main(header, body, footer, sound)