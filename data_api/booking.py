from datetime import datetime

from utils.db import terminating_sn
from models.car import Categories, Cars, Price, BookingDetails
from models.customers import Customers
from constants.response_messages import bad_request_status, basic_fraud_message, input_not_valid,\
                                        bad_request_message, success_status


class BookingBasics(object):

    def get_available_cars(start_time, end_time):
        """
        This method is responsible for fetching all the available cars in the inventory.
        Args:
            start_time: Trip start date.
            end_time:  Trip end date.
        Return: 
            List of available cars at that time period.
        """
        car_data = []
        with terminating_sn() as session:
            q1= session.query(BookingDetails.car_id).filter(BookingDetails.start_time > start_time,
                                                            BookingDetails.end_time < end_time).all()
            q2= session.query(BookingDetails.car_id).filter(BookingDetails.start_time < start_time,
                                                            BookingDetails.end_time < end_time).all()
            q3= session.query(BookingDetails.car_id).filter(BookingDetails.start_time < start_time,
                                                            end_time < BookingDetails.end_time).all()
            q4= session.query(BookingDetails.car_id).filter(BookingDetails.start_time > start_time,
                                                            end_time > BookingDetails.start_time,
                                                            end_time < BookingDetails.end_time).all()

            booked_car = q1 + q2 + q3 + q4
            booked_car_set = set()
            for car in booked_car:
                booked_car_set.add(car.car_id)

            car_list = session.query(Cars).filter(Cars.id.notin_(booked_car_set)).all()

        if not car_list:
            return {"success": True, "status_code": success_status, "message":cars_not_available}

        for car in car_list:
            local_dict = {}
            local_dict['reg_number'] = car.reg_number
            local_dict['category'] = car.category
            local_dict['colour'] = car.colour
            local_dict['model'] = car.model
            local_dict['current_milage'] = car.current_milage
            local_dict['location'] = car.location

            car_data.append(local_dict)

        return car_data

    def book_ride(user, reg_number, start_time, end_time):
        """
        This method is to book the car on the mentioned dates.
        Args:
             user: user_id
             reg_number: car registraion number
             start_time: epoc time when to start the booking
             end_time: epoc time when to end the booking
        Return:
             JSON with success status.
        """
        # renting_days = (datetime.fromtimestamp(end_time) - datetime.fromtimestamp(start_time)).days
        renting_days = int((end_time-start_time)/(24*60*60))

        if renting_days <0:
            return {"success": False, "status_code": bad_request_status, "message":input_not_valid}

        with terminating_sn() as session:
            car_id = session.query(Cars.id).filter(Cars.reg_number==reg_number)

            if not car_id.all():
                return {"success": False, "status_code": bad_request_status, "message":input_not_valid}

            query = BookingDetails(rental_id = user, car_id=car_id, start_time=start_time,
                                   end_time=end_time, renting_days=renting_days)
            session.add(query)
            session.flush()
            session.commit()

        return {"success": True,
                "status_code": success_status,
                "msg": "Trip booked.",
                "booking_id": query.booking_number}


    def start_ride(booking_id, start_km):
        """
        This function is for starting the already booked trip and to move it to the intransit mode.
        Args:
             booking_id: Valid booking id.
             start_km: starting km information.
        Return:
            JSON with success status.
        """

        with terminating_sn() as session:
            query = session.query(BookingDetails).filter(BookingDetails.booking_number==int(booking_id)).\
            update({BookingDetails.start_km: float(start_km), BookingDetails.is_completed: 0})

            session.flush()
            session.commit()

        return {"success": True, "status_code": success_status, "msg": "Trip started."}

    def end_ride(booking_id, end_km, current_milage, end_time):
        """
        This function is for ending the already started trip.
        Args:
             booking_id: Valid booking id.
             end_km: ending km information.
             current_milage: car's current millage noted from the car's dashboard.
             end_time: end time of the trip.
        Return:
            JSON with success status.
        """
        with terminating_sn() as session:    
            booking_query = session.query(BookingDetails).\
                filter(BookingDetails.booking_number==int(booking_id)).\
                first()
            if not booking_query:
                raise Exception({"success": False, "status_code": bad_request_status, "message": input_not_valid})

            if booking_query.is_completed ==1:
                raise Exception({"success": False, "status_code": bad_request_status, "message": input_not_valid})

            car_id = booking_query.car_id
            start_time = booking_query.start_time

            car_query = session.query(Cars).filter(Cars.id==car_id).first()
            car_category = car_query.category
            start_km = booking_query.start_km
            number_of_days = int((end_time-start_time)/(24*60*60))
            total_km = end_km - start_km

            # To check if days and total_km are not in negative, to avoid fraud.
            FraudDetection.basic_fraud_detection(number_of_days, total_km)

            total_fare = FareCalculations.price_calculate(number_of_days, total_km, car_category)

            car_query.current_milage = current_milage
            booking_query.renting_days = number_of_days
            booking_query.end_km = end_km
            booking_query.end_km = end_km
            booking_query.is_completed = 1
            booking_query.total_fare = total_fare

            session.merge(car_query)
            session.merge(booking_query)
            session.commit()

        return {"success": True, "status_code": success_status, "msg": "Trip Completed.", "total_fare":total_fare}


class FareCalculations(object):
    """
    This class is for calculating the total trip fare.
    """
    def price_calculate(number_of_days, total_km, car_category):
        """
        This method is for calculating the total fare as per the car category.
        Args:
            number_of_days: total number of trip days.
            total_km: Total car driven in the trip.
            car_category: 
        """
        final_price = 0
        with terminating_sn() as session:
            base_price = session.query(Price.base_price).first()[0]
            km_price = session.query(Price.km_price).first()[0]

        # common for the all the categoies and only calculation for the compact category.
        trip_fare = base_price * number_of_days

        if car_category == 2:
            trip_fare = FareCalculations.premium_price(trip_fare, km_price, total_km)
        elif car_category == 3:
            trip_fare = FareCalculations.minivan_price(trip_fare, km_price, total_km)

        return trip_fare

    def premium_price(trip_fare, km_price, total_km):
        """
        This method is to add the premium rate to the base trip fare.
        Business logic: baseDayRental * numberOfDays * 1.2 + kilometerPrice * numberOfKilometers
        Args:
            trip_fare: Base trip fare.
            km_price: Per kilometer price.
            total_km: Total car driven in the trip.
        Return:
            total fare for the trip
        """

        trip_fare = trip_fare * 1.2 + (km_price * total_km)
        return trip_fare

    def minivan_price(trip_fare, km_price, total_km):
        """
        This method is to add the minivan rate to the base trip fare.
        Business logic: baseDayRental * numberOfDays * 1.7 + (kilometerPrice * numberOfKilometers * 1.5)
        Args:
            trip_fare: Base trip fare.
            km_price: Per kilometer price.
            total_km: Total car driven in the trip.
        Return:
            total fare for the trip
        """

        trip_fare = trip_fare * 1.7 + (km_price * total_km * 1.5)
        return trip_fare


class FraudDetection(object):
    def basic_fraud_detection(number_of_days, total_km):
        if number_of_days < 0 or total_km < 0:
            raise Exception({"status":bad_request_message,
                "status_code": bad_request_status,
                "message": basic_fraud_message})

