from sqlalchemy import Column, Integer, Text, Date, FLOAT, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,backref


class Driver(declarative_base()):
    __tablename__ = "Driver"

    driver_id = Column(Integer, primary_key=True)
    name = Column(Text)
    surname = Column(Text)
    # routes = relationship("Route", order_by="Route.route_id", back_populates="driver")  


    def __str__(self):
        return "({},{},{})\n".format(self.driver_id,self.name,self.surname)

    def __repr__(self):
        return str(self)


class Route(declarative_base()):
    __tablename__ = "Route"

    route_id = Column(Integer, primary_key=True)
    first_town = Column(Text)
    last_town = Column(Text)
    driver_id = Column(Integer,ForeignKey('Driver.driver_id'))
    driver = relationship("Driver", back_populates="routes")

    def __str__(self):
        return "({},{},{},{})\n".format(self.route_id,self.first_town,self.last_town,self.driver_id)

    def __repr__(self):
        return str(self)

class Bus(declarative_base()):
    __tablename__ = "Bus"

    bus_id = Column(Integer, primary_key=True)
    bus_number = Column(Text)
    sits_count = Column(Integer)

    def __str__(self):
        return "({},{},{})\n".format(self.bus_id,self.bus_number,self.sits_count)

    def __repr__(self):
        return str(self)


class Ticket(declarative_base()):
    __tablename__ = "Ticket"

    ticket_id = Column(Integer, ForeignKey('Passenger.passenger_id'), primary_key=True)
    price = Column(FLOAT)
    sold_date = Column(Date)
    route_id = Column(Integer,ForeignKey('Route.route_id'))

    def __str__(self):
        return "({},{},{},{})\n".format(self.ticket_id,self.price,self.sold_date,self.route_id)

    def __repr__(self):
        return str(self)


class Passenger(declarative_base()):
    __tablename__ = "Passenger"

    passenger_id = Column(Integer,primary_key=True)
    name = Column(Text)
    surname = Column(Text)
    age = Column(Integer)

    def __str__(self):
        return "({},{},{},{})\n".format(self.passenger_id,self.name,self.surname,self.age)

    def __repr__(self):
        return str(self)


class Route_Bus(declarative_base()):
    __tablename__ = "route_bus"

    route_bus_id = Column(Integer,primary_key = True)
    route_id = Column(Integer,ForeignKey('Route.route_id'))
    bus_id = Column(Integer,ForeignKey('Bus.bus_id'))

    def __str__(self):
        return "({},{},{})\n".format(self.route_bus_id,self.route_id,self.bus_id)
        
    def __repr__(self):
        return str(self)