import requests
from psycopg2 import Error,  pool

devices_address_range = [
    'http://localhost:5005',
    'http://localhost:5004'
]


class Lokals():

    def __init__(self):
        self.apartments = []
        self.load_apartment_from_database()

    def create_apartments(self, name):
        self.apartments.append(Apartment(name))

    def load_apartment_from_database(self):
        with CursorFromConnectionPool() as cursor:
            cursor.execute('SELECT apartment_name FROM apartments')
            apartments_data = cursor.fetchall()
            for apartment in apartments_data:
                self.create_apartments(apartment[0])


class Apartment:

    def __init__(self, name):
        self.name = name
        self.rooms = []

    def create_room(self, name):
        self.rooms.append(Room(name))

    def load_rooms(self):
        with CursorFromConnectionPool() as cursor:
            cursor.execute(
                'SELECT name FROM rooms WHERE id_apartment = (SELECT id FROM apartments WHERE apartment_name = (%s));', (self.name,))
            room_data = cursor.fetchall()
            for room in room_data:
                self.create_room(room[0])


class Room:
    def __init__(self, name):
        self.name = name
        self.devices = []

    def create_device(self, address, id, name, type_device):
        self.devices.append(Device(address, id, name, type_device))

    def load_devices(self):
        with CursorFromConnectionPool() as cursor:
            cursor.execute(
                'SELECT address, id, name, type FROM devices WHERE id_rooms = (SELECT id FROM rooms WHERE name = (%s));', (self.name,))
            device_data = cursor.fetchall()
            for device in device_data:
                self.create_device(device[0], device[1], device[2], device[3])


class Device:

    def __init__(self, address=None, id=None, name=None, type_device=None):
        self.id = id
        self.name = name
        self.address = address
        self.type_device = type_device

    def creata_device(self):
        return self()

    def find_in_database(self):
        resp = requests.get(f'{self.address}/nameandtype').json()
        self.name, self.type_device = resp
        with CursorFromConnectionPool() as cursor:
            cursor.execute(
                'SELECT id FROM devices WHERE name = %s AND type = %s AND address = %s;', (self.name, self.type_device, self.address))
            id_data = cursor.fetchall()
        if id_data:
            self.id = id_data[0]
            requests.get(f'{self.address}/{self.id}')
        else:
            return True

    def add_device_to_database(self, apartment, room):
        with CursorFromConnectionPool() as cursor:
            cursor.execute('INSERT INTO devices( name , address, type ) VALUES  (%s, %s, %s)  RETURNING id',
                           (self.name, self.address, self.type_device))
            self.id = cursor.fetchone()[0]
        with CursorFromConnectionPool() as cursor:
            cursor.execute('UPDATE devices SET id_rooms = (SELECT id FROM rooms WHERE name = %s AND id_apartment = (SELECT id FROM apartments WHERE apartment_name = %s)) WHERE id = %s;', (room, apartment, self.id))
            requests.get(f'{self.address}/{self.id}')


class Database:

    __connection_pool = None

    @staticmethod
    def initialise(**kwargs):
        Database.__connection_pool = pool.SimpleConnectionPool(1, 10, **kwargs)

    @staticmethod
    def get_connection():
        return Database.__connection_pool.getconn()

    @staticmethod
    def return_connection(connection):
        Database.__connection_pool.putconn(connection)

    @staticmethod
    def close_all_connections():
        Database.__connection_pool.closeall()


class CursorFromConnectionPool:

    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = Database.get_connection()
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self,exception_cos, exception_value,exception_jeszczecos):
        if exception_value:
            self.conn.rollback()
        else:
            self.conn.commit()
            self.cursor.close()

        Database.return_connection(self.conn)


