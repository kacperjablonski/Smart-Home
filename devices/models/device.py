import itertools


class Device:
    newid = itertools.count()

    def __init__(self, name):
        self.id = None
        self.name = name
        self.status = False

    def change_status(self):
        if self.status:
            self.status = False
        else:
            self.status = True
