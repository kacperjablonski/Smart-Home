import requests
import json
from json import JSONEncoder

ADDRESS = 'http://localhost:8080'
HEADERS = {"Content-type": "application/json"}


def get_user_select(data):
    print([f"{i}. {s['name']}" for i, s in enumerate(data)])
    select = data[int(input())]
    return select


def method_and_status(data):
    keys = {}
    keys[10] = 'exit'
    for i, key in enumerate(data):
        print(f"{i}. {key} status: {data[key]}")
        keys[i] = key
    print('10 jeśli skończyłeś')
    select_method = keys[int(input())]
    return select_method


def new_device():
    return requests.get(f'{ADDRESS}/verify').json()


def add_device():

    print("Wykryto nowe urządzenie ")
    apartment_list = json.loads(requests.get(f'{ADDRESS}/getapartment').json())
    print("Wybierz gdzie znajduje sie urządzenie:")
    print('Wybierz mieszkanie')
    selected_apartment = get_user_select(apartment_list)
    rooms_list = json.loads(requests.get(
        f'{ADDRESS}/getrooms', selected_apartment).json())
    print('Wybierz pokój')
    selected_room = get_user_select(rooms_list)
    response = requests.get(f'{ADDRESS}/create', selected_room).json()
    print(response)


def menu_method():
    url = {}
    apartment_list = json.loads(requests.get(f'{ADDRESS}/getapartment').json())
    print('Wybierz mieszkanie')
    selected_apartment = get_user_select(apartment_list)
    rooms_list = json.loads(requests.get(
        f'{ADDRESS}/getrooms', selected_apartment).json())
    print('Wybierz pokój')
    selected_room = get_user_select(rooms_list)
    device_list = json.loads(requests.get(
        f'{ADDRESS}/getdevice', selected_room).json())
    print("Wybierz Urządzenie")
    selected_device = get_user_select(device_list)
    while True:
        response = json.loads(requests.get(
            f"{ADDRESS}/getmethod", selected_device).json())
        method = method_and_status(response)
        if method == 'exit':
            break
        url['address']= selected_device['address']
        url['method'] = method
        response = requests.get(f"{ADDRESS}/usemethod", url).json()
        print(response)


while True:
    if new_device():
        add_device()
    else:
        menu_method()


[
    {
        "name": "Mieszkanie Kacpra",
        "rooms": [
            {
                "name": "Kuchnia",
                "devices": []
            },
            {
                "name": "Sypialnia",
                "devices": []
            }
        ]
    },
    {
        "name": "Burdel Oskara",
        "rooms": [
            {
                "name": "BDSM ROOM",
                "devices": []
            },
            {
                "name": "FISTING ROOM",
                "devices": []
            },
            {
                "name": "Kuchnia",
                "devices": []
            }
        ]
    }
]
