import itertools

from flask import request


class Device:
    new_id = itertools.count()

    def __init__(self, name, method, address):
        self.id = None
        self.name = name
        self.method = method
        self.address = address

    def get_id(self):
        self.id = next(self.new_id)
