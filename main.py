#!/usr/bin/env python3
from starter import create_events, reorder_events_priority
from schedule import create_calendar
from timeblock import create_tblock
from datetime import datetime

events = reorder_events_priority(create_events())

now = datetime.now()
events = create_calendar(now.year, now.month, events)

if events:
    create_tblock(now.year, now.month, now.day, events)