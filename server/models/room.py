class Room:
    def __init__(self, name):
        self.name = name
        self.devices = []

    def __getitem__(self, index):
        return self.devices[index]
