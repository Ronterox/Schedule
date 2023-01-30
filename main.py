from schedule import create_calendar
from timeblock import create_tblock
from datetime import datetime

# This is gonna be VIMable
events = [["Study", 4], ["Break Time\n(Add me \nautomatically)", 2], ["Interactive/Gamify/'Force to know why' the why of things. Don't assume", 2], [
    "Better Watchfile", 1], ["VIM your whole world", 2]]

now = datetime.now()
events = create_calendar(now.year, now.month, events)

if events:
    create_tblock(now.year, now.month, now.day, events)