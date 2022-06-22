from flask import Flask
from flask_restful import Resource, Api, reqparse
import requests
from requests.exceptions import HTTPError
from json import JSONEncoder
from messages import Messages
import json
from models.classes import Flats, Apartment, Room, Device
from models.database import Database 
import os

Database.initialise(user="postgres",
                    password=os.environ['password_postgress'],
                    host="localhost",
                    port="5432",
                    database="inthome")


app = Flask(__name__)
api = Api(app)
class General():
    def __init__(self):
        self.message = Messages()
        self.lokals = Flats()
        self.device = Device()
        self.apartment = None
        self.room = None

general = General()

app.secret_key = os.environ['secret_key']

devices_address_range = [
    'http://localhost:5005',
    'http://localhost:5004'
]

address_get_response = []

class ApartmentEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def convert_data_from_json(data):
    return json.dumps(
        data, indent=4, cls=ApartmentEncoder)


parser_add = reqparse.RequestParser()
parser_add.add_argument('name')
parser_address = reqparse.RequestParser()
parser_address.add_argument('address')
parser_address.add_argument('method')


class VerifyDevice(Resource):
    def get(self):
        address_get_response.clear()
        for address in devices_address_range:
            try:
                resp = requests.get(address)
                resp.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
                continue
            except Exception as err:
                print(f'Other error occurred: {err}')
                continue 
            address_get_response.append(address)
            general.device.address = address
            device_exists = general.device.check_in_database_device_exist()
            if device_exists:
                return True
            else:
                continue
        return False

class CreateDevice(Resource):
    def get(self):
        args = parser_add.parse_args()
        room = Room(args['name'])
        general.device.add_device_to_database(general.apartment.name, room.name)
        return 'dodano urzadzenie'

class ApratmentGet(Resource):
    def get(self):
        return convert_data_from_json(general.lokals.apartments)


class RoomGet(Resource):
    def get(self):
        args = parser_add.parse_args()
        general.apartment = Apartment(args['name'])
        general.apartment.load_rooms()
        return convert_data_from_json(general.apartment.rooms)


class DeviceGet(Resource):
    def get(self):
        args = parser_add.parse_args()
        room = Room(args['name'])
        room.load_devices(address_get_response)
        return convert_data_from_json(room.devices)


class GetDeviceOptions(Resource):
    def get(self):
        args = parser_address.parse_args()
        response = requests.get(f"{args['address']}/get_device_options").json()
        return response


class UseDeviceOptions(Resource):
    def get(self):
        args = parser_address.parse_args()
        response = requests.get(
            f"{args['address']}/device_action", args).json()
        return response



api.add_resource(VerifyDevice, '/verify')
api.add_resource(CreateDevice, '/create')
api.add_resource(ApratmentGet, '/get_apartment')
api.add_resource(RoomGet, '/get_rooms')
api.add_resource(DeviceGet, '/get_device')
api.add_resource(GetDeviceOptions, '/get_device_options')
api.add_resource(UseDeviceOptions, '/use_method')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
