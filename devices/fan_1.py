from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
from models.light import Light
from models.fan import Fan

app = Flask(__name__)
api = Api(app)

fan_1 = Fan('wiatrak-w-salonie')

class GetId(Resource):
    def get(self):
        return fan_1.id


class AddDevice(Resource):
    def get(self, id):
        fan_1.id = id


class GetNameAndTypeDevice(Resource):
    def get(self):
        return [fan_1.name, fan_1.type]


class GetDeviceOptions(Resource):
    def get(self):
        dict_method = fan_1.get_option
        message = json.dumps(dict_method)
        return message


class DeviceAction(Resource):
    def get(self):
        parser_method = reqparse.RequestParser()
        parser_method.add_argument('method')
        method = parser_method.parse_args()
        return fan_1(method['method'])


api.add_resource(DeviceAction, '/device_action')
api.add_resource(AddDevice, '/<id>')
api.add_resource(GetId, '/')
api.add_resource(GetNameAndTypeDevice, "/name_and_type")
api.add_resource(GetDeviceOptions, "/get_device_options")
if __name__ == '__main__':
    app.run(debug=True, port=5005)
