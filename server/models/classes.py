import requests
from models.database import Database, Query


class Flats():

    def __init__(self) -> None:
        self.apartments = []
        self.load_apartment_from_database()

    def create_apartments(self, name: str) -> None:
        self.apartments.append(Apartment(name))

    def load_apartment_from_database(self) -> None:
        apartments_data = Database.make_query(Query.select_apartament())
        for apartment in apartments_data:
            self.create_apartments(apartment[0])


class Apartment:

    def __init__(self, name: str) -> None:
        self.name = name
        self.rooms = []

    def create_room(self, name: str) -> None:
        self.rooms.append(Room(name))

    def load_rooms(self) -> None:
        room_data = Database.make_query(
            Query.select_room_from_apartament(), self.name)
        for room in room_data:
            self.create_room(room[0])


class Device:
    
    def __init__(self, address: str = None, id: int = None, name: str = None, type_device: str = None, available_options: dict = None,state: bool =None) -> None:
        self.id = id
        self.name = name
        self.address = address
        self.type_device = type_device
        self.available_options = available_options
        self.state= state

    def check_in_database_device_exist(self):
        resp = requests.get(f'{self.address}/name_and_type').json()
        self.name, self.type_device = resp
        id_data = Database.make_query(
            Query.check_device_exist(), self.name, self.address, self.type_device)
        if id_data:
            self.id = id_data[0]
            requests.get(f'{self.address}/{self.id}')
        else:
            return True

    def add_device_to_database(self, apartment_name: str, room_name: str) -> None:
        id_data = Database.make_query(
            Query.create_device_in_database(), self.name, self.address, self.type_device)
        self.id = id_data[0][0]
        Database.make_query(
            Query.create_relation_device_with_room(), room_name, apartment_name, self.id)
        requests.get(f'{self.address}/{self.id}')

    def change_state(self):
        if self.state:
            self.state = False
        else:
            self.state = True


class Room:
    def __init__(self, name: str) -> None:
        self.name = name
        self.devices = []

    
    def create_device(self, address, id, name, type_device) -> None:
        self.devices.append(Device(address, id, name, type_device))

    def load_devices(self, list_address_response: list) -> None:
        device_data = Database.make_query(
            Query.select_device_from_room(), self.name)
        for device in device_data:
            if device[0] in list_address_response:
                self.create_device(
                    device[0], device[1], device[2], device[3])