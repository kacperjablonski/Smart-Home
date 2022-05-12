import requests
import json
from json import JSONEncoder

ADDRESS = 'http://localhost:8080' # SERVER_ADDRESS albo czegokolwiek
HEADERS = {"Content-type": "application/json"} #  JSON_HEADER


def get_user_select(data: dict) -> str:
    print([f"{i}. {s['name']}" for i, s in enumerate(data)])
    select = data[int(input())]
    return select


def get_user_selected_method(data: dict) -> str: 
    keys = {}
    keys[10] = 'exit'
    for i, key in enumerate(data):
        print(f"{i}. {key} status: {data[key]}")
        keys[i] = key
    print('10 jeśli skończyłeś')
    select_method = keys[int(input())]
    return select_method


def verify_address_and_find_device():
    return requests.get(f'{ADDRESS}/verify').json()


def add_new_device():

    print("Wykryto nowe urządzenie ")
    apartment_list = json.loads(requests.get(
        f'{ADDRESS}/get_apartment').json())
    print("Wybierz gdzie znajduje sie urządzenie:")
    print('Wybierz mieszkanie')
    user_selection = get_user_select(apartment_list)
    rooms_list = json.loads(requests.get(
        f'{ADDRESS}/get_rooms', user_selection).json())
    print('Wybierz pokój')
    user_selection = get_user_select(rooms_list)
    response = requests.get(f'{ADDRESS}/create', user_selection).json()
    print(response)


def menu_action():
    url = {}
    apartment_list = json.loads(requests.get(
        f'{ADDRESS}/get_apartment').json())
    print('Wybierz mieszkanie')
    user_selection = get_user_select(apartment_list)
    rooms_list = json.loads(requests.get(
        f'{ADDRESS}/get_rooms', user_selection).json())
    print('Wybierz pokój')
    user_selection = get_user_select(rooms_list)
    device_list = json.loads(requests.get(
        f'{ADDRESS}/get_device', user_selection).json())
    print("Wybierz Urządzenie")
    user_selection = get_user_select(device_list)
    while True:
        response = json.loads(requests.get(
            f"{ADDRESS}/get_device_options", user_selection).json())
        user_selection_option = get_user_selected_method(response)
        if user_selection_option == 'exit':
            break
        url['address'] = user_selection['address']
        url['method'] = user_selection_option
        response = requests.get(f"{ADDRESS}/use_method", url).json()
        print(response)


while True:
    if verify_address_and_find_device():
        add_new_device()
    else:
        menu_action()


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




#poprawic exit z pętli metod