from datetime import datetime
from progress import create_progress
import tkinter as tk
import calendar


def create_tk(root, title, width, height):
    root.title(title)
    root.minsize(width, height)
    root.maxsize(width, height)
    root.bind("<Control-w>", lambda _: root.destroy())
    return root


def create_tblock(year, month, day, events):
    root = create_tk(
        tk.Tk(), f"Timeblock for {calendar.month_name[month]} {year} {day}", 400, 400)

    day_events = [e for e in events if day in e["days"]]
    NUM_EVENTS = len(day_events)
    inputs = [None] * (NUM_EVENTS - 1)
    start_hour = 9
    pr = None

    def get_next_hour(hour, i):
        return (hour + day_events[i]["hours"] // len(day_events[i]["days"])) % 24

    def handle_input(event):
        nonlocal pr
        if pr:
            pr = pr.destroy()

        tblock_start = event.widget.get().split(":")
        if len(tblock_start) == 2:
            hour = int(tblock_start[0]) % 24
            minute = int(tblock_start[1]) % 60
        else:
            hour = int(tblock_start[0]) % 24
            minute = 0
        event.widget.delete(0, tk.END)
        last_hour = get_next_hour(hour, 0)

        def tblock_color(tblock):
            tblocks = tblock.split("-")
            def gtime(i): return datetime.strptime(
                tblocks[i] + f" {year}-{month}-{day}", "%H:%M %Y-%m-%d")
            return tblock, gtime(0) <= datetime.now() <= gtime(1)

        tblock, in_interval = tblock_color(f"{hour}:{minute:02d}-{last_hour}:{minute:02d}")

        def check_interval(in_interval, i):
            if in_interval:
                nonlocal pr
                d = day_events[i]
                pr = create_progress({"name": d["name"], "hours": d["hours"] // len(d["days"])}, root)
        
        check_interval(in_interval, 0) 
        event.widget.config(bg="pink" if in_interval else "gray")
        event.widget.insert(0, tblock)
        for i in range(NUM_EVENTS - 1):
            next_hour = get_next_hour(last_hour, i)
            tblock, in_interval = tblock_color(f"{last_hour}:00-{next_hour}:00")
            check_interval(in_interval, i + 1)
            inputs[i].config(text=tblock, bg="pink" if in_interval else "gray")
            last_hour = next_hour
        if pr:
            pr.mainloop()

    def handle_event_click(event):
        label = event.widget
        info_win = create_tk(tk.Toplevel(root), label["text"], 200, 200)
        text = tk.Text(info_win, font="Arial 12")
        text.pack(fill="both", expand=True)
        text.insert(tk.END, f"Name: {label['text']}\nFor each requeriment in the event, create a check label beside an action button in case it can be opened through the app.")
        info_win.mainloop()

    def get_interval(i):
        nonlocal start_hour
        next_hour = get_next_hour(start_hour, i)
        interval = f"{start_hour}:00-{next_hour}:00"
        start_hour = next_hour
        return interval

    def set_grid(label, row, column):
        label.grid(row=row, column=column, sticky="nsew")
        return label

    def get_label(txt, i=0, col=0):
        return set_grid(tk.Label(root, text=txt, relief="solid", font="Arial 12 bold"), i, col)

    def create_event_label(i):
        label = get_label(day_events[i]["name"], i, 0)
        label.bind("<Button-1>", handle_event_click)

    root.grid_columnconfigure(0, weight=1, minsize=20)
    root.grid_rowconfigure(0, weight=1, minsize=20)

    label_input = set_grid(
        tk.Entry(root, relief="solid", font="Arial 12 bold"), 0, 1)
    label_input.insert(0, get_interval(0))

    label_input.bind("<Return>", handle_input)
    create_event_label(0)
    for i in range(1, NUM_EVENTS):
        root.grid_rowconfigure(i, weight=1, minsize=20)
        create_event_label(i)
        label_input = get_label(get_interval(i), i, 1)
        inputs[i - 1] = label_input
    root.mainloop()

# print("\nYou can click on the event name to see more information about it.")
# events = [{"name": "Math", "hours": 2, "days": set([28, 3])},
#           {"name": "Break Time\n(Add me \nautomatically)",
#            "hours": 2, "days": set([28, 3])},
#           {"name": "English", "hours": 3, "days": set([28])}]
# create_tblock(2023, 1, 28, events)
