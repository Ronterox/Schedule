import tkinter as tk
from utilities import create_tk, get_color

def create_progress(event, root=None, color=0):
    root = create_tk(tk.Toplevel(root) if root else tk.Tk(), f"Countdown for {event['name']}", 300, 100)

    bg, fg = get_color(color)
    
    # create loading bar
    loadingbar = tk.Canvas(root, width=300, height=100, bg="white")
    loadingbar.grid(row=0, column=0)
    
    # create countdown label
    countdown = tk.Label(root, text=f"{event['hours']}h", font="Arial 12 bold")
    countdown.grid(row=0, column=0)

    event_seconds = event['hours'] * 3600

    def update_loadingbar():
        nonlocal event_seconds
        event_seconds -= 1
        if event_seconds <= 0:
            root.destroy()
            return
        loadingbar.delete("all")
        # create loading bar
        width = 300 * (1 - event_seconds / (event['hours'] * 3600))
        loadingbar.create_rectangle(0, 0, width, 100, fill=bg)
        countdown.config(text=f"{event_seconds / 3600:.0f}h {event_seconds % 3600 / 60:.0f}m {event_seconds % 60:.0f}s", fg=fg, bg=bg)
        root.after(1000, update_loadingbar)
    
    update_loadingbar()
    return root
    

# event = {"name": "Event", "hours": 0.005 }
# root = create_progress(event)
# root.mainloop()