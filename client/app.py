import requests
import json
from json import JSONEncoder



def print_chose(list):
    for nr, name in enumerate(list):
        print(nr, name['name'])


def get_chose(list):
    chose = input()
    return list[int(chose)]


def new_device():
    response = requests.get('http://localhost:8080/checkdevice').json()
    return response


def add_device():
    url = {}

    print("Wykryto nowe urządzenie ")
    resp = requests.get('http://localhost:8080/addlist').json()

    list_response = json.loads(resp)
    print("Wybierz gdzie znajduje sie urządzenie")
    print('Wybierz mieszkanie')
    print_chose(list_response)

    chose_apartment = get_chose(list_response)
    rooms = chose_apartment['rooms']

    print('Wybierz pokój')
    print_chose(rooms)

    chose_room = get_chose(rooms)
    
    url['room'] = chose_room['name']
    url['apartment'] = chose_apartment['name']
    
    response = requests.get('http://localhost:8080/create', url).json()
    print(response)


def menu_method():
    url = {}

    response = requests.get('http://localhost:8080/apartments').json()
    data_response = json.loads(response)

    print("Wybierz mieszkanie")
    print_chose(data_response)

    chose_apartment = get_chose(data_response)
    rooms = chose_apartment['rooms']

    print("Wybierz pokój")
    print_chose(rooms)

    chose_room = get_chose(rooms)
    devices = chose_room['devices']

    print("Wybierz Urządzenie")
    print_chose(devices)

    chose_device = get_chose(devices)

    url['device'] = chose_device['name']
    url['room'] = chose_room['name']
    url['apartment'] = chose_apartment['name']

    print(url)

    response = requests.get('http://localhost:8080/', url).json()
    print(response)


if new_device():
    add_device()
else:
    menu_method()
