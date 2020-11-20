from controller import Controller
from model import ModelPostgreSQL
from view import View

if __name__ == '__main__':

    c = Controller(ModelPostgreSQL(),View())
    while True:
        type = c.action_type_select()
        if type == "1":
            c.table_type_select()
            c.action_select()
        elif type == "2":
            c.static_search()
        else:
            c.random_insert()
        if not c.question_about_end():
            break
    c.disconnect_from_db()


