import requests
import json
from json import JSONEncoder

ADDRESS = 'http://localhost:8080'



def get_user_select(data):
    print(f"{i}. {s['name']}" for i, s in enumerate(data))
    select = data[int(input())]
    return select

def new_device():
    return requests.get(f'{ADDRESS}/checkdevice').json()

def add_device():
    url = {}

    print("Wykryto nowe urządzenie ")
    list_response = json.loads(requests.get('http://localhost:8080/addlist').json())
    print("Wybierz gdzie znajduje sie urządzenie:")
    print('Wybierz mieszkanie')
    selected_apartment = get_user_select(list_response)

    print('Wybierz pokój')
    selected_room = get_user_select(selected_apartment['rooms'])

    url = {'room': selected_room['name'],
           'apartment': selected_apartment['name'] 
           }


    response = requests.get(f'{ADDRESS}/create', url).json()
    print(response)


def menu_method():
    url = {}

    response = requests.get(f'{ADDRESS}/list').json()
    data_response = json.loads(response)

    print("Wybierz mieszkanie")
    selected = get_user_select(data_response)

    print("Wybierz pokój")
    selected = get_user_select(selected['rooms'])

    print("Wybierz Urządzenie")
    device = get_user_select(selected['devices'])

    response = requests.get(f"{ADDRESS}/{device['id']}").json()

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