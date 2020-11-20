import backend
import sys


class ModelPostgreSQL(object):
    def __init__(self):
        try:
            self._connection = backend.connect_to_db()
            self._present_table_type = ''
            self._cursor = self.connection.cursor()
        except Exception:
            print("Failed to connect to database")
            sys.exit()

    @property
    def connection(self):
        return self._connection

    @property
    def cursor(self):
        return self._cursor

    @property
    def present_table_type(self):
        return self._present_table_type

    @present_table_type.setter
    def present_table_type(self,new_present_table_type):
        self._present_table_type = new_present_table_type

    def create_item(self,cortage):
        backend.insert_one(self.cursor,self.present_table_type,cortage)

    def read_items(self):
        return backend.select_all(self.cursor,self.present_table_type)

    def update_item(self, list):
        backend.update_item(self.cursor, self.present_table_type, list)

    def delete_item(self,pr_key):
        return backend.delete_one(self.cursor,self.present_table_type,pr_key)

    def delete_all(self):
        return backend.delete_all(self.cursor,self.present_table_type)

    def disconnect_from_db(self):
        backend.disconnect_from_db(self.connection,self.cursor)

    def random(self, value):
        backend.random(self.cursor, value)

    def static_search(self):
        return backend.static_search(self.cursor)

