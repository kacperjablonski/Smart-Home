import itertools

from flask import request


class Device:
    new_id = itertools.count()

    def __init__(self, name):
        self.id = None
        self.name = name
        self.status = False

    def change_status(self):
        self.status = not self.status
        

    def get_id(self):
        self.id = next(self.new_id)



