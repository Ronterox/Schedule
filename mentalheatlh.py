from enum import Enum


class Types(Enum):
    HACK = 0
    IRL = 1
    CREATE = 2
    PLAY = 3
    STUDY = 4
    TRAIN = 5
    PROGRAM = 6


def create_events():
    events = []
    while True:
        try:
            name = input("Event name: ")
            if name == "":
                break
            hours = int(input("Hours: "))
            types = input("Type: " + ", ".join([t.name for t in Types]) + ": ").upper()
            if types not in Types._member_names_:
                raise ValueError
            events.append([name, hours, Types[types]])
        except ValueError:
            print("Invalid input")
    return events


def reorder_events_priority(events):
    while True:
        try:
            for i, event in enumerate(events):
                print(f"{i}: {event}")
            print("Enter the index of the event you want to move")
            idx = int(input())
            if idx < 0:
                break
            print("Enter the index you want to move it to")
            idx2 = int(input())
            events.insert(idx2 % len(events), events.pop(idx % len(events)))
        except ValueError:
            print("Invalid input")
    return events


# events = create_events()
# events = reorder_events_priority(events)
# print(events)
