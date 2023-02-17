#!/usr/bin/env python3
from startup import create_events, reorder_events_priority, load_events, save_events
from schedule import create_calendar
from timeblock import create_tblock
from datetime import datetime

# TODO:
# - Delay increments priority
# - Limit MH types to 1 of each per day
# - Can move daily events around
# - Functional tools, notes, and steps
# - More energy it gives increases priority

events = create_events(load_events())
events = reorder_events_priority(events)

now = datetime.now()
events = create_calendar(now.year, now.month, events)

if events:
    create_tblock(now.year, now.month, now.day, events)

save_events(events)