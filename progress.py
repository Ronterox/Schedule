import tkinter as tk

def create_loadingbar_event_countdown(event):
    root = tk.Tk()
    root.title(f"Countdown for {event['name']}")
    root.geometry("300x100")
    root.resizable(False, False)
    
    # create loading bar
    loadingbar = tk.Canvas(root, width=300, height=100, bg="white")
    loadingbar.grid(row=0, column=0)
    
    # create countdown label
    countdown = tk.Label(root, text=f"{event['hours']}h", font="Arial 12 bold")
    countdown.grid(row=0, column=0)

    event_seconds = event['hours'] * 3600

    # create loading bar
    loadingbar = tk.Canvas(root, width=300, height=100, bg="white")
    loadingbar.grid(row=0, column=0)
    
    # create countdown label
    countdown = tk.Label(root, text=f"{event['hours']}h", font="Arial 12 bold")
    countdown.grid(row=0, column=0)

    def update_loadingbar():
        nonlocal event_seconds
        event_seconds -= 1
        if event_seconds <= 0:
            root.destroy()
            return
        loadingbar.delete("all")
        # create loading bar
        width = 300 * (1 - event_seconds / (event['hours'] * 3600))
        loadingbar.create_rectangle(0, 0, width, 100, fill="green")
        countdown.config(text=f"{event_seconds // 3600}h {event_seconds % 3600 // 60}m {event_seconds % 60}s")
        root.after(1000, update_loadingbar)
    
    update_loadingbar()
            
    root.bind("<Control-w>", lambda _: root.destroy())
    root.mainloop()
    

event = {"name": "Event", "hours": 0.005 }
create_loadingbar_event_countdown(event)