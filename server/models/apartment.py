class Apartment:
    def __init__(self, name):
        self.name = name
        self.rooms = []

    def __getitem__(self, index):
        return self.rooms[index]
