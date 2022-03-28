from flask import Flask, render_template, make_response, request, jsonify, session
from flask_restful import Resource, Api, marshal_with, reqparse,  fields
import requests
from json import JSONEncoder
from dataclasses import dataclass
from typing import List

from models.apartment import Apartment
from models.room import Room
import json
from models.devices.fan import Fan
from models.devices.light import Light

app = Flask(__name__)
api = Api(app)


class Apartment_encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class ManagerDevices():

    def __init__(self):
        self.operation = {
            'fan': self.fan,
            'light': self.light
        }

    def __call__(self, device, name):
        return self.operation[device](name)

    def fan(self, name):
        return Fan(name)

    def light(self, name):
        return Light(name)


class NewDevice():
    def __init__(self):
        self.address = str

    def find_apartment_by_name(self, apartment):
        return [a for a in APARMENTS if a.name == apartment].pop()

    def find_room_by_name(self, apartment, room):
        return [r.name for r in apartment.rooms if room].index(room)

    def create_new_devise(self, address):
        self.address = address
        resp = requests.get(f'{self.address}/nameandtype').json()
        obj_name, obj_type = resp
        self.add_devices = manager(obj_type, obj_name)
        return 'Dodano nowe Urzadzenie'

    def add_devices_to_apartment_and_room(self, chosen):
        apartment = self.find_apartment_by_name(chosen['apartment'])
        nr_room = self.find_room_by_name(apartment, chosen['room'])
        apartment[nr_room].devices.append(self.add_devices)
        self.add_devices.get_id()
        requests.get(f'{self.address}/{self.add_devices.id}')
        return 'Utworzono nowe Urządzenie'


manager = ManagerDevices()
newdevice = NewDevice()

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# TEMP INIT
mk = Apartment('Mieszkanie Kacpra')

mk.rooms.append(Room('Kuchnia'))
mk.rooms.append(Room('Sypialnia'))

ob = Apartment('Burdel Oskara')
ob.rooms.append(Room('BDSM ROOM'))
ob.rooms.append(Room('FISTING ROOM'))
ob.rooms.append(Room('Kuchnia'))

# DATABASE
APARMENTS = [
    mk, ob
]

# Endpoint : Lista mieszkań =< GET
# Endpoint : Stworz mieszkanie =< POST
# localhost:5002
# localhost:5003
devices_address_range = [
    'http://localhost:5005']

parser = reqparse.RequestParser()
parser.add_argument('apartment')
parser.add_argument("room")
cache_parser = {}

ready_to_convertet = []
ready_to_convertet.append(mk)
ready_to_convertet.append(ob)
apartment_data_json = json.dumps(
    ready_to_convertet, indent=4, cls=Apartment_encoder)


def verify_port():
    address = devices_address_range[0]
    resp = requests.get(url=address)
    if resp.status_code == 200:
        if resp.json() == None:
            return True, address
    return False

# class Apartments(Resource):
#     def get(self):
#         pass


# class UserChoise(Resource):
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('apartment')
#         parser.add_argument("room")
#         parser.add_argument("device")
#         parser.add_argument('action')
#         args = parser.parse_args()
#         return args['room']


class CheckDevice(Resource):
    def get(self):
        verify, address = verify_port()
        if verify == True:
            newdevice.create_new_devise(address)
            return True
        else:
            return False


class AddList(Resource):
    def get(self):
        return apartment_data_json


class CreateDevice(Resource):
    def get(self):
        args = parser.parse_args()
        response = newdevice.add_devices_to_apartment_and_room(args)
        return response


# api.add_resource(UserChoise, '/')
# api.add_resource(Apartments, '/apartments')
api.add_resource(AddList, '/addlist')
api.add_resource(CheckDevice, '/checkdevice')
api.add_resource(CreateDevice, '/create')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
