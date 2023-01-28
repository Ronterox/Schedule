from datetime import datetime
import tkinter as tk
import calendar


def create_tblock(year, month, day, events):
    root = tk.Tk()
    root.title(f"Timeblock for {calendar.month_name[month]} {year} {day}")
    root.minsize(400, 400)
    root.maxsize(400, 400)

    day_events = [e for e in events if day in e["days"]]
    NUM_EVENTS = len(day_events)
    inputs = [None] * (NUM_EVENTS - 1)
    last_hour = 9

    def handle_input(event):
        tblock_start = event.widget.get().split(":")
        if len(tblock_start) == 2:
            hour = int(tblock_start[0]) % 24
            minute = int(tblock_start[1])
        else:
            hour = int(tblock_start[0]) % 24
            minute = 0
        event.widget.delete(0, tk.END)
        last_hour = hour + events[0]['hours'] // len(events[0]['days'])
        last_hour %= 24
        def tblock_color(tblock):
            tblocks = tblock.split("-")
            dt_format = "%H:%M %Y-%m-%d"
            date = f" {year}-{month}-{day}"
            t1, t2 = datetime.strptime(tblocks[0] + date, dt_format), datetime.strptime(tblocks[1] + date, dt_format)
            now = datetime.now()
            return tblock, "pink" if t1 <= now <= t2 else "gray"
        tblock, color = tblock_color(f"{hour}:{minute:02d}-{last_hour}:{minute:02d}")
        event.widget.config(bg=color)
        event.widget.insert(0, tblock)
        for i in range(NUM_EVENTS - 1):
            next_hour = last_hour + \
                day_events[i]["hours"] // len(day_events[i]["days"])
            next_hour %= 24
            tblock, color = tblock_color(f"{last_hour}:00-{next_hour}:00")
            inputs[i].config(text=tblock, bg=color)
            last_hour = next_hour

    def handle_event_click(event):
        label = event.widget
        info_win = tk.Toplevel(root)
        info_win.title(label["text"])
        info_win.minsize(200, 200)
        info_win.maxsize(200, 200)
        text = tk.Text(info_win, font="Arial 12")
        text.pack(fill="both", expand=True)
        text.insert(
            tk.END, f"Name: {label['text']}\nFor each requeriment in the event, create a check label beside an action button in case it can be opened through the app.")
        info_win.bind("<Control-w>", lambda _: info_win.destroy())
        info_win.mainloop()

    root.grid_columnconfigure(0, weight=1, minsize=20)
    for i in range(NUM_EVENTS):
        root.grid_rowconfigure(i, weight=1, minsize=20)
        label = tk.Label(
            root, text=day_events[i]["name"], relief="solid", font="Arial 12 bold")
        label.grid(row=i, column=0, sticky="nsew")
        label.bind("<Button-1>", handle_event_click)
        if i == 0:
            label_input = tk.Entry(root, relief="solid", font="Arial 12 bold")
            label_input.grid(row=i, column=1, sticky="nsew")
            next_hour = last_hour + \
                day_events[i]["hours"] // len(day_events[i]["days"])
            next_hour %= 24
            label_input.insert(0, f"{last_hour}:00-{next_hour}:00")
            last_hour = next_hour
            label_input.bind("<Return>", handle_input)
        else:
            next_hour = last_hour + \
                day_events[i]["hours"] // len(day_events[i]["days"])
            next_hour %= 24
            label_input = tk.Label(
                root, text=f"{last_hour}:00-{next_hour}:00", relief="solid", font="Arial 12 bold")
            last_hour = next_hour
            label_input.grid(row=i, column=1, sticky="nsew")
            inputs[i - 1] = label_input
    root.bind("<Control-w>", lambda _: root.destroy())
    root.mainloop()


print("Press Ctrl+W to close the window.")
print("Write the time in the format of HH:MM and press Enter to save it.")
print("\nThe time will be automatically calculated for the next event.")
print("Remember to set the time of your computer program to the correct days, time, year, etc...")
print("\nYou can click on the event name to see more information about it.")
events = [{"name": "Math", "hours": 2, "days": set([28, 3])},
          {"name": "Break Time\n(Add me \nautomatically)", "hours": 2, "days": set([28, 3])},
          {"name": "English", "hours": 3, "days": set([28])}]
create_tblock(2023, 1, 28, events)
