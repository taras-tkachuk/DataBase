from controller import Controller
from model import ModelPostgreSQL
from view import View

if __name__ == '__main__':

    c = Controller(ModelPostgreSQL(),View())
    while True:
        c.table_type_select()
        c.action_select()
        if not c.question_about_end():
            break
    c.disconnect_from_db()


