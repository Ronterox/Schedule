from enum import Enum
import json


class EventTypes(Enum):
    HACK = 0
    IRL = 1
    CREATE = 2
    PLAY = 3
    STUDY = 4
    TRAIN = 5
    PROGRAM = 6


def create_events(events=[]):
    while True:
        try:
            for i, event in enumerate(events):
                print(f"{i}: {event}")
            name = input("Event name: ")
            if name == "":
                break
            hours = int(input("Hours: "))
            types = input(
                "Type: " + ", ".join(EventTypes._member_names_) + ": ").upper()
            if types not in EventTypes._member_names_:
                raise ValueError
            events.append([name, hours, EventTypes[types].name])
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
            if idx2 < 0 or idx2 >= len(events) or idx >= len(events):
                raise ValueError
            events[idx2], events[idx] = events[idx], events[idx2]
        except ValueError:
            print("Invalid input")
    return events


def load_events():
    try:
        return json.load(open("data.json"))
    except FileNotFoundError:
        return []


def save_events(events):
    if isinstance(events[0], dict):
        input_events = []
        for event in events:
            input_events.append(
                [event["name"], event["hours"], event["type"], list(event["days"])])
        events = input_events
    json.dump(events, open("data.json", "w"))


if __name__ == "__main__":
    old_data = load_events()
    events = create_events(old_data)
    events = reorder_events_priority(events)
    save_events(events)
    print(events)
