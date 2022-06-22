import itertools


class Device:
    newid = itertools.count()

    def __init__(self, name):
        self.id = None
        self.name = name
        self.state = False
        
    def change_state(self):
        self.state =  not self.state 

  