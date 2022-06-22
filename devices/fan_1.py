from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
from models.light import Light
from models.fan import Fan

app = Flask(__name__)
api = Api(app)

fan_1 = Fan('wiatrak-w-salonie')
parser_option = reqparse.RequestParser()


class GetId(Resource):
    def get(self):
        return fan_1.id


class AddDevice(Resource):
    def get(self, id):
        fan_1.id = id


class GetNameAndTypeDevice(Resource):
    def get(self):
        return [fan_1.name, fan_1.type]


class GetDeviceState(Resource):
    def get(self):
        return (fan_1.state, fan_1.color, fan_1.power_light)


class DeviceAction(Resource):
    def get(self):
        parser_address = reqparse.RequestParser()
        parser_address.add_argument('method')
        method = parser_address.parse_args()
        return fan_1(method['method'])


class GetDeviceOptions(Resource):
    def get(self):
        return json.dumps(fan_1.get_option)


class UseDeviceOption(Resource):
    def get(self):
        args = parser_option.parse_args()
        response = fan_1(args)
        return response


api.add_resource(DeviceAction, '/device_action')
api.add_resource(AddDevice, '/<id>')
api.add_resource(GetId, '/')
api.add_resource(GetNameAndTypeDevice, "/name_and_type")
api.add_resource(GetDeviceState, "/get_device_state")
api.add_resource(GetDeviceOptions, "/get_device_options")
api.add_resource(UseDeviceOption, "/device_action")
if __name__ == '__main__':
    app.run(debug=True, port=5005)
