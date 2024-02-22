from main import Tracker


def test():
    tracker = Tracker()
    with open('export.json', 'wb') as file:
        data = tracker.markets().encode('utf-8')
        file.write(data)
