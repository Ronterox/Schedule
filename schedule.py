import calendar
import tkinter as tk
from utilities import get_color, create_tk


def create_calendar(year, month, events):
    index = 0
    root = create_tk(
        tk.Tk(), f"Calendar for {calendar.month_name[month]} {year}")

    for i in range(len(events)):
        events[i] = {"name": events[i][0],
                     "hours": events[i][1], "days": set()}

    # create the calendar
    cal = calendar.monthcalendar(year, month)
    labels, assign_labels = [], []

    def get_assign():
        txt, bg, fg = "All events assigned!", None, None
        for i, event in enumerate(events):
            if len(event["days"]) == 0:
                txt = f'Left to assign...\n{event["name"]}: {event["hours"]}h\n'
                bg, fg = get_color(i)
                break
        return txt, bg, fg

    txt, bg, fg = get_assign()
    for row in range(len(cal)):
        root.grid_rowconfigure(row, weight=1, minsize=20)
        for col in range(7):
            day = cal[row][col]
            if day:
                label = tk.Label(root, text=day, relief="solid",
                                 font="Arial 12 bold")

                def add_event(day):
                    def update_label(label, evs, day):
                        evs_txt = [e[0] for e in evs]
                        evs_hours = [
                            float(f'{events[e[1]]["hours"] / len(events[e[1]]["days"]):0.2f}') for e in evs]
                        evs_total = sum(evs_hours)

                        if evs:
                            idx = evs_hours.index(max(evs_hours))
                            for event in events:
                                if event["name"] == evs_txt[idx]:
                                    idx = events.index(event)
                                    break
                            bg_col, fg_col = get_color(idx)
                        else:
                            bg_col, fg_col = None, None

                        label.config(text=f'{day}\n{evs_txt}\n{evs_hours}\nTotally: {evs_total}h',
                                     bg=bg_col, fg=fg_col)

                    curr_event = (events[index]["name"], index)
                    evs_days = events[index]["days"]

                    if day in evs_days:
                        lab, evs = labels[day - 1]
                        evs_days.remove(day)
                        evs.remove(curr_event)
                        update_label(lab, evs, day)
                    else:
                        evs_days.add(day)

                    for d in evs_days:
                        label, evs = labels[d - 1]
                        evs.add(curr_event)
                        update_label(label, evs, d)

                    txt, bg, fg = get_assign()
                    for label in assign_labels:
                        label.config(text=txt, bg=bg, fg=fg)

                label.bind("<Button-1>", lambda _, day=day: add_event(day))
                labels.append([label, set()])  # [label, [events]]
            else:
                label = tk.Label(root, text=txt, relief="solid", bg=bg, fg=fg)
                assign_labels.append(label)

            label.grid(row=row, column=col, sticky='nsew')
            root.grid_columnconfigure(col, weight=1, minsize=20)

    mouse_label = tk.Label(root, text=events[index])

    def update_idx(_):
        nonlocal index
        index = (index + 1) % len(events)

    def update_mouse_label():
        mouse_label.config(text=events[index])
        mouse_label.place(x=root.winfo_pointerx(), y=root.winfo_pointery())
        root.after(100, update_mouse_label)

    update_mouse_label()

    root.bind("<Button-3>", update_idx)
    root.mainloop()
    return [e for e in events if e["days"]]

# events = [["Study", 4, Types.STUDY], ["Break Time\n(Add me \nautomatically)", 2, Types.PROGRAM], ["Interactive/Gamify/'Force to know why' the why of things. Don't assume", 2, Types.STUDY], [
#     "Better Watchfile", 1, Types.CREATE], ["VIM your whole world", 2, Types.CREATE]]

# events = create_calendar(2023, 1, events)
