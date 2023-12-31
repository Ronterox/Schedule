from datetime import datetime
from progress import create_progress
from utilities import create_tk, get_color
import tkinter as tk
import calendar


def create_tblock(year, month, day, events, start_time=(9, 0)):
    root = create_tk(tk.Tk(), f"Timeblock for {calendar.month_name[month]} {year} {day}", 400, 400)
    day_events = [e for e in events if day in e["days"]]
    if not day_events:
        return
    NUM_EVENTS = len(day_events)
    inputs = [None] * (NUM_EVENTS - 1)
    start_hour, start_minute = start_time
    pgbar = None

    def get_interval_format(t1, t2):
        return f"{t1[0]:02d}:{t1[1]:02d}-{t2[0]:02d}:{t2[1]:02d}"

    def get_next_hour(hour, i):
        return (hour + day_events[i]["hours"] // len(day_events[i]["days"])) % 24

    def handle_input(event):
        nonlocal pgbar, start_time
        if pgbar:
            pgbar = pgbar.destroy()

        tblock_start = event.widget.get().split("-")[0].split(":")
        hour, minute = int(tblock_start[0]) % 24, int(
            tblock_start[1]) % 60 if len(tblock_start) > 1 else 0
        event.widget.delete(0, tk.END)
        last_hour = get_next_hour(hour, 0)
        start_time = hour, minute

        def tblock_color(tblock):
            tblocks = tblock.split("-")
            def gtime(i): return datetime.strptime(tblocks[i] + f" {year}-{month}-{day}", "%H:%M %Y-%m-%d")
            finish = gtime(1)
            return tblock, gtime(0) <= datetime.now() < finish, (finish - datetime.now()).total_seconds() / 3600

        tblock, in_interval, time_left = tblock_color(
            get_interval_format((hour, minute), (last_hour, minute)))

        def check_interval(in_interval, i, time_left):
            if in_interval:
                nonlocal pgbar
                d = day_events[i]
                pgbar = create_progress({"name": d["name"], "hours": time_left}, root, color=i)

        check_interval(in_interval, 0, time_left)
        event.widget.config(bg="pink" if in_interval else "gray")
        event.widget.insert(0, tblock)
        for i in range(NUM_EVENTS - 1):
            next_hour = get_next_hour(last_hour, i)
            tblock, in_interval, time_left = tblock_color(
                get_interval_format((last_hour, minute), (next_hour, minute)))
            check_interval(in_interval, i + 1, time_left)
            inputs[i].config(text=tblock, bg="pink" if in_interval else "gray")
            last_hour = next_hour
        if pgbar:
            pgbar.mainloop()

    def handle_event_click(event):
        label = event.widget
        info_win = create_tk(tk.Toplevel(root), label["text"], 200, 200)
        text = tk.Text(info_win, font="Arial 12")
        text.pack(fill="both", expand=True)
        text.insert(
            tk.END, f"Name: {label['text']}\nFor each requeriment in the event, create a check label beside an action button in case it can be opened through the app.")
        info_win.mainloop()

    def get_interval(i):
        nonlocal start_hour
        next_hour = get_next_hour(start_hour, i)
        interval = get_interval_format(
            (start_hour, start_minute), (next_hour, start_minute))
        start_hour = next_hour
        return interval

    def set_grid(label, row, column):
        label.grid(row=row, column=column, sticky="nsew")
        return label

    def get_label(txt, i=0, col=0):
        bg, fg = None, None
        if col == 0:
            bg, fg = get_color(i)
        return set_grid(tk.Label(root, text=txt, relief="solid", font="Arial 12 bold", bg=bg, fg=fg), i, col)

    def create_event_label(i, row=0):
        event = day_events[i]
        label = get_label(
            f'{event["name"]}\n{(event["hours"] // len(event["days"]))}h', row, 0)
        label.bind("<Button-1>", handle_event_click)

    def create_event_interval(i):
        row = i * 2
        root.grid_rowconfigure(row, weight=1, minsize=20)
        create_event_label(i, row)
        inputs[i - 1] = get_label(get_interval(i), row, 1)

    def on_break_button(i, remove=False):
        root.destroy()
        events_break = []

        def is_break(i):
            event = day_events[i % NUM_EVENTS]
            if event["name"] == "Break":
                event["hours"] += -1 if remove else 1
                if event["hours"] == 0:
                    events_break.remove(event)
                return True
            return False

        for j in range(NUM_EVENTS):
            if i == j and not (is_break(j - 1) or is_break(j)):
                if not remove:
                    events_break.append({"name": "Break", "hours": 1, "days": [day]})
            events_break.append(day_events[j])
        create_tblock(year, month, day, events_break, start_time)

    def break_button(i, row):
        canRemove = day_events[i - 1]["name"] == "Break"
        remove = set_grid(tk.Button(root, text="Remove Break",
                                    state=tk.NORMAL if canRemove else tk.DISABLED), row, 0)
        if canRemove:
            remove.bind("<Button-1>", lambda _: on_break_button(i, True))
        add = set_grid(tk.Button(root, text="Add Break"), row, 1)
        add.bind("<Button-1>", lambda _: on_break_button(i))

    root.grid_columnconfigure(0, weight=1, minsize=20)
    root.grid_rowconfigure(0, weight=1, minsize=20)

    label_input = set_grid(
        tk.Entry(root, relief="solid", font="Arial 12 bold"), 0, 1)
    label_input.insert(0, get_interval(0))
    label_input.bind("<Return>", handle_input)

    create_event_label(0)
    break_button(1, 1)
    for i in range(1, NUM_EVENTS - 1):
        create_event_interval(i)
        break_button(i + 1, i * 2 + 1)

    if NUM_EVENTS > 1:
        create_event_interval(NUM_EVENTS - 1)

    def handle_click(_):
        label_input.focus_set()
        label_input.event_generate("<Return>")

    root.bind("<Button-1>", handle_click)
    root.mainloop()


if __name__ == "__main__":
    print("\nYou can click on the event name to see more information about it.")
    now = datetime.now()
    events = [{"name": "Math", "hours": 2, "days": set([now.day, 3])},
              {"name": "Jumping", "hours": 2, "days": set([now.day, 3])},
              {"name": "English", "hours": 3, "days": set([now.day])}]
    create_tblock(now.year, now.month, now.day, events)
