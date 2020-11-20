class View(object):
    @staticmethod
    def action_type_select_display():
        print("Select action_type(number):\n")
        print("1---Definite action in definite table\n2---Static search\n3---Random")


    @staticmethod
    def table_name_select_display():
        print("Select table name:\n")
        print("1---Bus\n2---Driver\n3---Passenger\n4---Route\n5---Ticket\n6---route_bus\n")

    @staticmethod
    def action_select_display():
        print("Select action(number):\n")
        print("1---Show table items\n2---Update table item\n3---Create new table item\n"
        "4---Delete table item\n5---Delete all data from table\n")

    @staticmethod
    def enter_cortege_item_display(item):
        print("Enter {}".format(item))

    @staticmethod
    def table_rows_display(items):
        cursor = items
        row = items.fetchone()
        while row is not None:
            print(row)
            row = cursor.fetchone()

    @staticmethod
    def question_about_end_display():
        print("Continue to work with Database?(Y/N)\n")

    @staticmethod
    def message_print(message):
        print(message)

