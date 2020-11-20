from dateutil import parser
import random


class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_items(self):
        items = self.model.read_items()
        if items.rowcount:
            self.view.table_rows_display(items)
            return
        self.view.message_print("This table was already empty\n")

    def enter_items(self, table_item_names):
        return_array = []
        for name in table_item_names:
            while True:
                self.view.enter_cortege_item_display(name)
                inp = str(input())
                if validate_input(name, inp):
                    return_array.append(inp)
                    break
                else:
                    self.view.message_print("Error:enter valid value\n")
        return return_array

    def table_type_select(self):
        self.view.table_name_select_display()
        while True:
            table_type = str(input())
            if 0 < int(table_type) < 7:
                if table_type == "1":
                    self.model.present_table_type = "Bus"
                elif table_type == "2":
                    self.model.present_table_type = "Driver"
                elif table_type == "3":
                    self.model.present_table_type = "Passenger"
                elif table_type == "4":
                    self.model.present_table_type = "Route"
                elif table_type == "5":
                    self.model.present_table_type = "Ticket"
                elif table_type == "6":
                    self.model.present_table_type = "route_bus"
                return
            self.view.message_print("Error:enter number from 1 to 6\n")
    

    def action_type_select(self):
        self.view.action_type_select_display()
        while True:
            action_type = str(input())
            if action_type != "1" and action_type != "2" and action_type != "3":
                self.view.message_print("Error:enter number from 1 to 3\n")
                continue
            break
        return action_type

    def action_select(self):
        self.view.action_select_display()
        while True:
            action = str(input())
            if action == "1":
                self.show_items()
            elif action == "2":
                self.update_item()
            elif action == "3":
                self.insert_item()
            elif action == "4":
                self.delete_item()
            elif action == "5":
                self.delete_all()
            else:
                self.view.message_print("Error:Enter number from 1-5\n")
                continue
            break

        self.model.connection.commit()

    def question_about_end(self):
        self.view.question_about_end_display()
        while True:
            inp = str(input())
            if inp == "Y" or inp == "y":
                return True
            elif inp == "N" or inp == "n":
                return False
            else:
                self.view.message_print("""Error:enter "Y" or "N"\n """)

    def disconnect_from_db(self):
        self.model.disconnect_from_db()

    def insert_item(self):
        while True:
            if self.model.present_table_type == 'Bus':
                list = self.enter_items(("bus_number", "sits_count"))
            elif self.model.present_table_type == 'Driver':
                list = self.enter_items(("name", "surname"))
            elif self.model.present_table_type == 'Passenger':
                list = self.enter_items(("name", "surname", "age"))
            elif self.model.present_table_type == 'Route':
                list = self.enter_items(("first_town", "last_town", "driver_id"))
            elif self.model.present_table_type == 'Ticket':
                list = self.enter_items(("ticket_id", "price", "sold_date", "route_id"))
            else:
                list = self.enter_items(("route_id", "bus_id"))
            try:
                self.model.create_item(list)
                self.view.message_print("Row was inserted successfully\n")
                break
            except Exception as error:
                print(error)
                break
            finally:
                self.model.connection.commit()

    def update_item(self):
        while True:
            if self.model.present_table_type == 'Bus':
                list = self.enter_items(("bus_id","bus_number", "sits_count"))
            elif self.model.present_table_type == 'Driver':
                list = self.enter_items(("driver_id","name", "surname"))
            elif self.model.present_table_type == 'Passenger':
                list = self.enter_items(("passenger_id","name", "surname", "age"))
            elif self.model.present_table_type == 'Route':
                list = self.enter_items(("route_id","first_town", "last_town", "driver_id"))
            elif self.model.present_table_type == 'Ticket':
                list = self.enter_items(("ticket_id","price", "sold_date", "route_id"))
            else:
                list = self.enter_items(("route_bus_id","route_id", "bus_id"))
            try:
                self.model.update_item(list)
                self.view.message_print("Row was updated successfully\n")
                break
            except Exception as error:
                print(error)
            finally:
                self.model.connection.commit()

    def delete_item(self):
        id = self.enter_items(["id"])
        try:
            if self.model.delete_item(id):
                self.view.message_print("Row was deleted successfully\n")
            else:
                self.view.message_print("There isn't row for deleting with such attribute value\n")
        except Exception as error:
                print(error)
        finally:
                self.model.connection.commit()

                
    def delete_all(self):
        if self.model.delete_all():
            self.view.message_print("All rows in table were deleted successfully\n")
        else:
            self.view.message_print("Table was already empty\n")

    def random_insert(self):
        self.view.message_print("How many random records do you want to enter?\n")
        value = str(input())
        self.model.random(value)
        self.model.connection.commit()



    def static_search(self):
        c = self.model.static_search()
        if c:
            for row in c[0]:
                # self.view.message_print(row)
                self.view.message_print(f"Name of passenger: {row[0]}\nName of driver: {row[1]}\nCost of ticket: {row[2]}\n\
Sold date: {row[3]}\nFirst town: {row[4]}\n\n")
            self.view.message_print(f"Query execution time: {c[1]}")
        else:
            self.view.message_print("No data found")

def validate_input(attr_name, attr_value):
    bound_check = list(attr_name.split(' '))
    if len(bound_check) > 1:
        if bound_check[1] == "Lower" or bound_check[1] == "Upper":
            attr_name = bound_check[0]
    if attr_name.find("table") != -1:
        if (attr_value == "Bus" or attr_value =="Driver" or attr_value == "Passenger"
        or attr_value == "Route" or attr_value == "Ticket" or attr_value == "route_bus"):
            return True
        return False
    if "id" in attr_name:
        if attr_value.isdecimal():
            return True
    elif attr_name == "sits_count":
        if attr_value.isdecimal():
            return True
    elif attr_name == "name":
        if attr_value.isalpha():
            return True
    elif attr_name == "surname":
        if attr_value.isalpha():
            return True
    elif attr_name == "age":
        if attr_value.isdecimal():
            return True
    elif attr_name == "bus_number":
        li = list(attr_value.split(" "))
        if li[0].isalpha() and li[2].isalpha():
            if li[1].isdecimal:
                return True
        return False
    elif "town" in attr_name:
        li = list(attr_value.split(" "))
        for item in li:
            if not item.isalpha():
                return False
        return True
    elif attr_name == "price":
        if attr_value.isdecimal():
            return True
    elif attr_name == "sold_date":
        try:
            parser.parse(attr_value)
            return True
        except ValueError:
            return False
 