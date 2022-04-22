from flask import Flask
from flask_restful import Resource, Api, reqparse
import requests
from requests.exceptions import HTTPError
from json import JSONEncoder
from messages import Messages
import json
from models.classes import Lokals, Apartment, Room, Device, Database


Database.initialise(user="postgres",
                    password="Drzewo123",
                    host="localhost",
                    port="5432",
                    database="inthome")


app = Flask(__name__)
api = Api(app)

devices_address_range = [
    'http://localhost:5005',
    'http://localhost:5004'
]


class Apartment_encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


message = Messages()
lokals = Lokals()
apartment = None
room = None
device = Device()


def convert(data):
    return json.dumps(
        data, indent=4, cls=Apartment_encoder)


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

parseradd = reqparse.RequestParser()
parseradd.add_argument('name')


class VerifyDevice(Resource):
    def get(self):
        global device
        for address in devices_address_range:
            try:
                resp = requests.get(address)
                resp.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except Exception as err:
                print(f'Other error occurred: {err}')
            else:
                device.address = address
                device_exists = device.find_in_database()
                if device_exists:
                    return True
                else:
                    continue
        return False


class ApratmentGet(Resource):
    def get(self):
        return convert(lokals.apartments)


class RoomGet(Resource):
    def get(self):
        global apartment
        args = parseradd.parse_args()
        apartment = Apartment(args['name'])
        apartment.load_rooms()
        return convert(apartment.rooms)


class DeviceGet(Resource):
    def get(self):
        global room
        args = parseradd.parse_args()
        room = Room(args['name'])
        room.load_devices()
        return convert(room.devices)


class GetMethod(Resource):
    def get(self):
        parseraddress = reqparse.RequestParser()
        parseraddress.add_argument('address')
        args = parseraddress.parse_args()
        response = requests.get(f"{args['address']}/method").json()
        return response


class UseMethod(Resource):
    def get(self):
        parseraddress = reqparse.RequestParser()
        parseraddress.add_argument('address')
        parseraddress.add_argument('method')
        args = parseraddress.parse_args()
        response = requests.get(
            f"{args['address']}/usemethod", args).json()
        return response


class CreateDevice(Resource):
    def get(self):
        args = parseradd.parse_args()
        room = Room(args['name'])
        device.add_device_to_database(apartment.name, room.name)
        return 'dodano urzadzenie'


api.add_resource(ApratmentGet, '/getapartment')
api.add_resource(RoomGet, '/getrooms')
api.add_resource(DeviceGet, '/getdevice')
api.add_resource(UseMethod, '/usemethod')
api.add_resource(GetMethod, '/getmethod')
api.add_resource(CreateDevice, '/create')
api.add_resource(VerifyDevice, '/verify')
if __name__ == '__main__':
    app.run(debug=True, port=8080)
