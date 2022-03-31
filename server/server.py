from flask import Flask, render_template, make_response, request, jsonify, session
from flask_restful import Resource, Api, marshal_with, reqparse,  fields
import requests
from json import JSONEncoder
from dataclasses import dataclass
from typing import List
from messages import Messages
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

    def __call__(self, device, name,method,address):
        return self.operation[device](name,method,address)

    def fan(self, name,method,address):
        return Fan(name,method, address)

    def light(self, name,method,address):
        return Light(name,method ,address)


class Device():
    def __init__(self):
        self.address = None

    def find_apartment_by_name(self, apartment):
        return [a for a in APARMENTS if a.name == apartment].pop()

    def find_room_by_name(self, apartment, room):
        return [r.name for r in apartment.rooms if room].index(room)

    def find_device_by_name(self,device):
        return [d.name for d in self.apartment[self.nr_room].devices if device].index(device)

    def create_new_devise(self, address):
        self.address = address
        resp = requests.get(f'{self.address}/nameandtype').json()
        obj_name, obj_type, obj_method = resp
        self.add_devices = manager(obj_type, obj_name, obj_method, self.address)

    def find_devices_to_apartment_room(self,chosen):
        self.apartment = self.find_apartment_by_name(chosen['apartment'])
        self.nr_room = self.find_room_by_name(self.apartment, chosen['room'])


    def add_devices_to_apartment_and_room(self, chosen):
        self.find_devices_to_apartment_room(chosen)
        self.apartment[self.nr_room].devices.append(self.add_devices)
        self.add_devices.get_id()
        requests.get(f'{self.address}/{self.add_devices.id}')
        return 'git malina'

    def chose_method_to_use(self,chosen_apartment_room_device,chose_method):
        self.find_devices_to_apartment_room(chosen_apartment_room_device)
        self.device = self.find_device_by_name(chosen_apartment_room_device['device'])
        response =requests.get(self.apartment[self.nr_room][self.device].address, chose_method)
        return response

    

manager = ManagerDevices()
device = Device()
message =  Messages()

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# TEMP INIT
mk = Apartment('Mieszkanie Kacpra'  )

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

devices_address_range = [
    'http://localhost:5005',
    'http://localhost:5004'
]

parseradd = reqparse.RequestParser()
parseradd.add_argument('apartment')
parseradd.add_argument("room")
parser = reqparse.RequestParser()
parser.add_argument('apartment')
parser.add_argument("room")
parser.add_argument("device")

def convert ():
    ready_to_convertet = []
    ready_to_convertet.append(mk)
    ready_to_convertet.append(ob)
    return  json.dumps(
    ready_to_convertet, indent=4, cls=Apartment_encoder)


def verify_port():
    address = devices_address_range[0]
    resp = requests.get(url=address)
    if resp.status_code == 200:
        if resp.json() == None:
            device.create_new_devise(address)
            return True
    return False

class GetList(Resource):
    def get(self):
        return convert()


class UserChoise(Resource):
    def get(self):
        args = parser.parse_args()
        response = device.chose_method_to_use(args)
        return response

class CheckDevice(Resource):
    def get(self):
        verify = verify_port()
        return  verify
            


class AddList(Resource):
    def get(self):
        return convert()


class CreateDevice(Resource):
    def get(self):
        args = parseradd.parse_args()
        response = device.add_devices_to_apartment_and_room(args)
        return response


api.add_resource(UserChoise, '/')
api.add_resource(GetList, '/list')
api.add_resource(AddList, '/addlist')
api.add_resource(CheckDevice, '/checkdevice')
api.add_resource(CreateDevice, '/create')

if __name__ == '__main__':
    app.run(debug=True, port=8080)




