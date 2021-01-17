
from sqlalchemy import exc

from utils.db import terminating_sn
from models.car import Categories, Cars, Price
from models.customers import Customers

"""
car details list:
    0 index: Registration number
    1 index: Car category
    2 index: Car color
    3 index: year of registraion.
    4 index: car current milage.
    5 index: vehicle place.
"""
cars_list = [["KA-03 JE 1859", "1", "Black", "2020", "15", "Bangalore"],
             ["KA-03 JE 1860", "2", "Blue", "1992", "10", "Delhi"],
             ["KA-03 JE 1861", "3", "White", "2010", "12", "Bangalore"],
             ["KA-03 JE 1862", "1", "Orange", "2000", "13", "Bangalore"],
             ["KA-03 JE 1863", "2", "Red", "2018", "20", "Punjab"],
             ["KA-03 JE 1864", "3", "Grey", "2021", "12", "Mumbai"],
            ]

"""
Car category list:
    0 index: Car category.
    1 index: Capacity
"""
car_category_list = [["Compact", 5],
                     ["Premium", 6],
                     ["Minivan", 12]
                    ]

"""
Customer list:
    0 index: name
    1 index: adderess
    2 index: DOB
    3 index: email
"""
customers_list = [["test1", "test_addr", "01-12-2000", "test1@gmail.com"],
                  ["test2", "test_addr", "01-06-2000", "test2@gmail.com"],
                ]

"""
Price list:
    0 index: base price.
    1 index: KM price.
"""
price_list = [2000, 30]


class InitializeData():
    def init_customers():
        """
        This function is responsible for saving the customer record in the DB.
        The list of customers is globally declared.
        args: empty
        returns: Json with status and message.
        """
        with terminating_sn() as session:
            for customer in customers_list:
                name = customer[0]
                address = customer[1]
                dob = customer[2]
                email = customer[3]
                cust = Customers(name, address, dob, email)
                session.add(cust)
            try:
                session.commit()
            except exc.IntegrityError as e:
                return {"success": False, "msg": e._message()}

        return {"success": True, "msg": "Initial Customers migrated"}


    def init_category():
        """
        This function is responsible for saving the categories record in the DB.
        The list is globally declared.
        args: empty
        returns: Json with status and message.
        """
        with terminating_sn() as session:
            for category in car_category_list:
                name = category[0]
                capacity = category[1]
                data = Categories(name, capacity)
                session.add(data)
            try:
                session.commit()
            except exc.IntegrityError as e:
                return {"success": False, "msg": e._message()}

        return {"success": True, "msg": "Initial data migrated"}


    def init_common_price():
        """
        This function is responsible for saving the price details in the DB.
        The list is globally declared.
        args: empty
        returns: Json with status and message.
        """
        with terminating_sn() as session:
            base_price = price_list[0]
            km_price = price_list[1]
            data = Price(base_price, km_price)
            session.add(data)
            session.commit()

        return {"success": True, "msg": "Initial price data migrated"}

    def init_car_details():
        """
        This function is responsible for saving the car details in the DB.
        The list is globally declared.
        args: empty
        returns: Json with status and message.
        """
        with terminating_sn() as session:
            for car in cars_list:
                reg = car[0]
                category = car[1]
                colour = car[2]
                model = car[3]
                milage = car[4]
                location = car[5]
                data = Cars(reg, category, colour, model, milage, location)
                session.add(data)
            try:
                session.commit()
            except exc.IntegrityError as e:
                return {"success": False, "msg": e._message()}

        return {"success": True, "msg": "Initial data migrated"}






