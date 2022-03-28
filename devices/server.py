from flask import Flask, render_template, make_response, request, jsonify, session
from flask_restful import Resource, Api, marshal_with, reqparse,  fields
import json
import requests


from models.light import Light
from models.fan import Fan

app = Flask(__name__)
api = Api(app)

light_1 = Light('Lampka-nocna')
light_2 = Light('Lampka-ścienna')
light_3 = Light('Oświeglenie-górne')
fan_1 = Fan('wiatrak-w-salonie')
fan_2 = Fan('wiatrak-w-Kuchni')



class Finder(Resource):
    def get(self):
        return fan_1.id

class AddDevice(Resource):
    def get(self,id):
        fan_1.id=id
        return "Dodano wiatrak"

class GetNameAndType(Resource):
    def get(self):
        return [fan_1.name, fan_1.type]


api.add_resource(AddDevice,'/<id>')
api.add_resource(Finder, '/')
api.add_resource(GetNameAndType,"/nameandtype")
if __name__ == '__main__':
    app.run(debug=True, port=5005)




