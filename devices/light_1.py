from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
import requests


from models.light import Light
from models.fan import Fan
HEADERS = {"Content-type": "application/json"}
app = Flask(__name__)
api = Api(app)

light_1 = Light('lampa-w-salonie')


class Finder(Resource):
    def get(self):
        return light_1.id


class AddDevice(Resource):
    def get(self, id):
        light_1.id = id
        return 'git malina'


class GetNameAndType(Resource):
    def get(self):
        return [light_1.name, light_1.type]


class GetMethod(Resource):
    def get(self):
        dict_method = light_1.get_method
        message = json.dumps(dict_method)
        return message


class UseMethod(Resource):
    def get(self):
        parseraddress = reqparse.RequestParser()
        parseraddress.add_argument('method')
        method = parseraddress.parse_args()
        return light_1(method['method'])

api.add_resource(UseMethod, '/usemethod')
api.add_resource(AddDevice, '/<id>')
api.add_resource(Finder, '/')
api.add_resource(GetNameAndType, "/nameandtype")
api.add_resource(GetMethod, "/method")
if __name__ == '__main__':
    app.run(debug=True, port=5004)
