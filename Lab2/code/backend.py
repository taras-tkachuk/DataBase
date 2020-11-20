import psycopg2
from time import time

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


def select_all(cursor, table_name):

    if table_name == "Ticket":
        cursor.execute(""" SELECT ticket_id, concat(price::numeric, ' $') as price, to_char(sold_date, 'YYYY-MM-DD'), route_id from "Ticket" """)
    else:
        cursor.execute(""" SELECT * FROM "{}" """.format(table_name))

    return cursor


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
    elif table_name == "route_bus":
        cursor.execute("""DELETE FROM "route_bus" WHERE "route_bus_id" = %s """,(pr_key))

    return cursor.rowcount


def delete_all(cursor,table_name):
    cursor.execute("""DELETE FROM "{}" """.format(table_name))
    return cursor.rowcount


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


def connect_to_db():
    connection = psycopg2.connect(dbname="intercity", user="postgres", password="1112")
    return connection


def disconnect_from_db(connection,cursor):
    cursor.close()
    connection.close()
    print("Connection with PostgreSQL is closed")

def random(cursor, value):
    cursor.execute(""" INSERT INTO "Passenger" ("name","surname","age")
select chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) ||
chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int),
chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) ||
chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) ||
chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int),
trunc(random()*78)::int 
from generate_series(1,%s) """, (value))



def static_search(cursor):
    start = time()
    cursor.execute(""" SELECT name || ' ' || surname as full_name, driver_full_name, concat(price::numeric, ' $') as price, 
                        to_char(sold_date, 'YYYY-MM-DD'), first_town FROM public."Passenger" p
                    INNER JOIN (SELECT * FROM public."Ticket"
                            where sold_date BETWEEN '2019-01-01' AND '2020-01-01') t on p.passenger_id = t.ticket_id
                    INNER JOIN (SELECT route_id, first_town, driver_id FROM public."Route" 
                            where first_town LIKE '%iv%') r on r.route_id = t.route_id
                INNER JOIN (SELECT name || ' ' || surname as driver_full_name, driver_id FROM public."Driver") d on d.driver_id = r.driver_id  """)
    end = time()
    return (cursor, end - start)
