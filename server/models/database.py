from psycopg2 import Error,  pool

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

    @staticmethod
    def make_query(query: str, *params):
        with CursorFromConnectionPool() as cursor:
            cursor.execute(query,(*params,))
            return cursor.fetchall()

class CursorFromConnectionPool:

    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = Database.get_connection()
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exception_cos: str, exception_value: str, exception_jeszczecos: str):
        if exception_value:
            self.conn.rollback()
        else:
            self.conn.commit()
            self.cursor.close()

        Database.return_connection(self.conn)

class Query:

    @staticmethod
    def select_apartament():
        return 'SELECT apartment_name FROM apartments'

    @staticmethod
    def select_room_from_apartament():
        return 'SELECT name FROM rooms WHERE id_apartment = (SELECT id FROM apartments WHERE apartment_name = (%s));'

    @staticmethod
    def select_device_from_room():
        return 'SELECT address, id, name, type FROM devices WHERE id_rooms = (SELECT id FROM rooms WHERE name = (%s));'

    @staticmethod
    def check_device_exist():
        return 'SELECT id FROM devices WHERE name = %s AND address = %s AND type = %s;'

    @staticmethod
    def create_device_in_database():
        return 'INSERT INTO devices( name, address, type ) VALUES  (%s, %s, %s)  RETURNING id;'

    @staticmethod
    def create_relation_device_with_room():
        return 'UPDATE devices SET id_rooms = (SELECT id FROM rooms WHERE name = %s AND id_apartment = (SELECT id FROM apartments WHERE apartment_name = %s)) WHERE id = %s RETURNING id;'