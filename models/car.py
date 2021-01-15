from sqlalchemy import Column, Index, ForeignKeyConstraint

from sqlalchemy.dialects.sqlite import CHAR, FLOAT, INTEGER, TEXT

from models.base import Base


class Cars(Base):
    __tablename__ = 'car_details'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    reg_number = Column(CHAR(50), unique=True)
    category = Column(INTEGER)
    colour = Column(CHAR(50))
    model = Column(CHAR(50))
    current_milage = Column(FLOAT)
    location = Column(CHAR(50))


    __table_args__ = (
        Index('car_id_index', 'id'),
        Index('location_index', 'location'),
        ForeignKeyConstraint(['category'], ['categories.id'])
    )

    def __init__(self, reg_number, category, colour, model, current_milage, location):
        self.reg_number = reg_number
        self.category = category
        self.colour = colour
        self.model = model
        self.current_milage = current_milage
        self.location = location


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    category = Column(CHAR(100), unique=True)
    capacity = Column(INTEGER)

    __table_args__ = (
        Index('cat_id_index', 'id'),
        Index('category_index', 'category'),
    )

    def __init__(self, category, capacity):
        self.category = category
        self.capacity = capacity


class Price(Base):
    __tablename__ = 'price'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    base_price = Column(FLOAT)
    km_price = Column(FLOAT)


    __table_args__ = (
        Index('price_id_index', 'id'),
    )

    def __init__(self, base_price, km_price):
        self.base_price = base_price
        self.km_price = km_price


class BookingDetails(Base):
    __tablename__ = 'booking_details'
    booking_number = Column(INTEGER, primary_key=True, autoincrement=True)
    rental_id = Column(INTEGER)
    car_id = Column(INTEGER)
    start_time = Column(INTEGER)
    end_time = Column(INTEGER)
    renting_days = Column(INTEGER)
    start_km = Column(FLOAT)
    end_km = Column(FLOAT)
    is_completed = Column(INTEGER) #0- in-transit, 1- completed
    total_fare = Column(FLOAT)


    __table_args__ = (
        Index('booking_id_index', 'booking_number'),
        ForeignKeyConstraint(['rental_id'], ['customers.id']),
        ForeignKeyConstraint(['car_id'], ['car_details.id'])
    )

    def __init__(self, rental_id, car_id, start_time, end_time, renting_days):
        self.rental_id = rental_id
        self.car_id = car_id
        self.start_time = start_time
        self.end_time = end_time
        self.renting_days = renting_days
