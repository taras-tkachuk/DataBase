import psycopg2
from time import time
from model_orm import *
from sqlalchemy.orm import *
from sqlalchemy import create_engine


def insert_one(cursor, table_name, list):

    if table_name == "Bus":
        cursor.execute("""INSERT INTO "Bus" ("bus_number", "sits_count") VALUES(%s, %s)""",(list[0], list[1]))

    elif table_name == "Driver":
        cursor.execute("""INSERT INTO "Driver" ("name", "surname") VALUES (%s, %s)""",(list[0], list[1]))

    elif table_name == "Passenger":
        cursor.execute("""INSERT INTO "Passenger" ("name","surname","age") VALUES (%s, %s, %s)""",(list[0], list[1], list[2]))

    elif table_name == "Route":
        cursor.execute("""INSERT INTO "Route" ("first_town","last_town","driver_id") VALUES (%s, %s, %s)""", (list[0], list[1], list[2]))

    elif table_name == "Ticket":
        cursor.execute("""INSERT INTO "Ticket" ("ticket_id", "price","sold_date","route_id") VALUES (%s, %s, %s, %s)""",(list[0], list[1], list[2], list[3]))

    else:
        cursor.execute("""INSERT INTO "route_bus" ("route_id","bus_id") VALUES (%s, %s)""",(list[0], list[1]))

def insert_one_orm(Session,table_name,list):

    session = Session()

    if table_name == "Driver":
        table_item = Driver(name = list[0], surname = list[1])
    elif table_name == "Bus":
        table_item = Bus(bus_number = list[0],sits_count = list[1])
    elif table_name == "Passenger":
        table_item = Passenger(name = list[0],surname = list[1],age = list[2])
    elif table_name == "Route":
        table_item = Route(first_town = list[0],last_town = list[1],driver_id = list[2])
    elif table_name == "Ticket":
        table_item = Ticket(ticket_id = list[0],price = list[1],sold_date = list[2],route_id = list[3])
    else:
        table_item = Route_Bus(route_id = list[0],bus_id = list[1])
    session.add(table_item)
    session.commit()
    session.close()


def select_all(cursor, table_name):

    if table_name == "Ticket":
        cursor.execute(""" SELECT ticket_id, concat(price::numeric, ' $') as price, to_char(sold_date, 'YYYY-MM-DD'), route_id from "Ticket" """)
    else:
        cursor.execute(""" SELECT * FROM "{}" """.format(table_name))

    return cursor


def select_all_orm(Session,table_name):
    session = Session()
    if table_name == "Driver":
        table_item = session.query(Driver).all()
    elif table_name == "Bus":
        table_item = session.query(Bus).all()
    elif table_name == "Passenger":
        table_item = session.query(Passenger).all()
    elif table_name == "Route":
        table_item = session.query(Route).all()
    elif table_name == "Ticket":
       table_item = session.query(Ticket).all()
    else:
        table_item = session.query(Route_Bus).all()
    session.close()

    return table_item

def delete_one(cursor, table_name, pr_key):

    if table_name == "Bus":
        cursor.execute("""DELETE FROM "Bus" WHERE "bus_id" = %s """,(pr_key))
    elif table_name == "Driver":
        cursor.execute("""DELETE FROM "Driver" WHERE "driver_id" = %s """,(pr_key))
    elif table_name == "Passenger":
        cursor.execute("""DELETE FROM "Passenger" WHERE "passenger_id" = %s """,(pr_key))
    elif table_name == "Route":
        cursor.execute("""DELETE FROM "Route" WHERE "route_id" = %s """,(pr_key))
    elif table_name == "Ticket":
        cursor.execute("""DELETE FROM "Ticket" WHERE "ticket_id" = %s """,(pr_key))
    else:
        cursor.execute("""DELETE FROM "route_bus" WHERE "route_bus_id" = %s """,(pr_key))

    return cursor.rowcount


def delete_one_orm(Session,table_name,pr_key):
    session = Session()
    pr_key = pr_key[0]
    if table_name == "Bus":
        table_item = session.query(Bus).filter(Bus.bus_id == pr_key).first()
    elif table_name == "Driver":
        table_item = session.query(Driver).filter(Driver.driver_id == pr_key).first()
    elif table_name == "Passenger":
        table_item = session.query(Passenger).filter(Passenger.passenger_id == pr_key).first()
    elif table_name == "Route":
        table_item = session.query(Route).filter(Route.route_id == pr_key).first()
    elif table_name == "Ticket":
        table_item = session.query(Ticket).filter(Ticket.ticket_id == pr_key).first()
    else:
        table_item = session.query(Route_Bus).filter(Route_Bus.route_bus_id == pr_key).first()
    if table_item is None:
        session.close()
        return 0

    session.delete(table_item)
    session.commit()
    session.close()

    return 1


def delete_all(cursor,table_name):
    cursor.execute("""DELETE FROM "{}" """.format(table_name))
    return cursor.rowcount

def delete_all_orm(Session,table_name):
    session = Session()
    if table_name == "Driver":
        tmp = session.query(Driver).delete()
    elif table_name == "Bus":
        tmp = session.query(Bus).delete()
    elif table_name == "Route":
        tmp = session.query(Route).delete()
    elif table_name == "Ticket":
        tmp = session.query(Ticket).delete()
    elif table_name == "Passenger":
        tmp = session.query(Passenger).delete()
    else:
        tmp = session.query(Route_Bus).delete()
    
    session.commit()
    session.close()

    return tmp


def update_item(cursor, table_name, list):
    if table_name == "Bus":
        cursor.execute("""UPDATE "Bus" SET "bus_number" = %s, "sits_count" = %s
        WHERE "bus_id" = %s """, (list[1], list[2], list[0]))

    elif table_name == "Driver":
        cursor.execute("""UPDATE "Driver" SET "name" = %s, "surname" = %s
        WHERE "driver_id" = %s """, (list[1], list[2], list[0]))
    
    elif table_name == "Passenger":
        cursor.execute("""UPDATE "Passenger" SET "name" = %s, "surname" = %s, "age" = %s
        WHERE "passenger_id" = %s """, (list[1], list[2], list[3], list[0]))

    elif table_name == "Route":
        cursor.execute("""UPDATE "Route" SET "first_town" = %s, "last_town" = %s, "driver_id" = %s
        WHERE "route_id" = %s """, (list[1], list[2], list[3], list[0]))

    elif table_name == "Ticket":
        cursor.execute("""UPDATE "Ticket" SET "price" = %s, "sold_date" = %s, "route_id" = %s
        WHERE "ticket_id" = %s """, (list[1], list[2], list[3], list[0]))

    else:
        cursor.execute("""UPDATE "route_bus" SET "route_id" = %s, "bus_id" = %s
        WHERE "route_bus_id" = %s """, (list[1], list[2], list[0]))

    return cursor.rowcount


def update_item_orm(Session,table_name,list):
    session = Session()

    if table_name == "Bus":
        table_item = session.query(Bus).filter(Bus.bus_id == list[0]).first()
        if table_item is None:
            session.close()
            return 0
        table_item.bus_number, table_item.sits_count = list[1],list[2]

    elif table_name == "Driver":
        table_item = session.query(Driver).filter(Driver.driver_id == list[0]).first()
        if table_item is None:
            session.close()
            return 0
        table_item.name, table_item.surname = list[1],list[2]
    
    elif table_name == "Passenger":
        table_item = session.query(Passenger).filter(Passenger.passenger_id == list[0]).first()
        if table_item is None:
            session.close()
            return 0
        table_item.name, table_item.surname, table_item.age = list[1],list[2],list[3]

    elif table_name == "Route":
        table_item = session.query(Route).filter(Route.route_id == list[0]).first()
        if table_item is None:
            session.close()
            return 0
        table_item.first_town, table_item.last_town, table_item.driver_id = list[1],list[2],list[3]

    elif table_name == "Ticket":
        table_item = session.query(Ticket).filter(Ticket.ticket_id == list[0]).first()
        if table_item is None:
            session.close()
            return 0
        table_item.price, table_item.sold_date, table_item.route_id = list[1],list[2],list[3]

    else:
        table_item = session.query(Route_Bus).filter(Route_Bus.route_bus_id == list[0]).first()
        if table_item is None:
            session.close()
            return 0
        table_item.route_id,table_item.bus_id = list[1],list[2]
    session.commit()
    session.close()

    return 1




def connect_to_db():
    connection = psycopg2.connect(dbname="intercity", user="postgres", password="1112")
    return connection

def connect_to_db_orm():
    engine = create_engine('postgresql+psycopg2://postgres:1112@localhost:5432/intercity')
    session_class = sessionmaker(bind=engine)
    return session_class


def disconnect_from_db(connection,cursor):
    cursor.close()
    connection.close()
    print("Connection with PostgreSQL is closed")

