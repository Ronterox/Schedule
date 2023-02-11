from random import shuffle

COLOR_PAL = [('black', 'white'), ('white', 'black'), ('red', 'white'), ('blue', 'white'), ('green', 'white'), ('yellow', 'black'),
             ('orange', 'black'), ('purple', 'white'), ('pink', 'black'), ('brown', 'white'), ('grey', 'black'), ('cyan', 'black')]

shuffle(COLOR_PAL)

def get_color(index):
    return COLOR_PAL[index % len(COLOR_PAL)]

def create_tk(root, title, width=None, height=None):
    root.title(title)
    if width and height:
        root.minsize(width, height)
        root.maxsize(width, height)
    root.bind("<Control-w>", lambda _: root.destroy())
    return root

