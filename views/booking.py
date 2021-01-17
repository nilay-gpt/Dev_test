"""
This file is responsible for externail APIs for booking.
"""

from flask import Blueprint
from flask import request

import json
import time

from data_api.booking import BookingBasics
from constants.response_messages import bad_request_status, req_param_missing


booking_blueprint = Blueprint('booking', __name__)


@booking_blueprint.route('/get/rides', methods=['GET'])
def get_rides():
    """
    This API is responsible for intialisibng the data for Customers, Cars and price inverntory.
    """
    data = request.values.to_dict()
    try:
        start_date = int(data['start_date'])
        end_date = int(data['end_date'])
    except KeyError:
        return {"status": bad_request_status, "message": req_param_missing}

    ride_details = BookingBasics.get_available_cars(start_date, end_date)


    return {"success": True, "available_cars": ride_details}

@booking_blueprint.route('/book/ride', methods=['POST'])
def book_ride():
    """
    This API is for booking the ride from the mentioned dates.
    NOTE: As this feature supports the future booking also so this
            will not start the trip.
    """
    user = request.form.get('user')
    reg_number = request.form.get('reg_number')
    start_time = int(request.form.get('start_time'))
    end_time = int(request.form.get('end_time'))

    response = BookingBasics.book_ride(user, reg_number, start_time, end_time)


    return response


@booking_blueprint.route('/start/ride', methods=['PUT'])
def start_ride():
    """
    This API is for starting the already booked ride.
    """
    booking_id = request.form.get('booking_id')
    start_km = request.form.get('start_km')

    response = BookingBasics.start_ride(booking_id, start_km)


    return response

@booking_blueprint.route('/end/ride', methods=['PUT'])
def end_ride():
    """
    This API is for starting the already booked ride.
    """
    end_time = int(time.time())
    # end_time = 1611764187

    booking_id = request.form.get('booking_id')
    try:
        end_km = float(request.form.get('end_km'))
    except:
        return False
    current_milage = request.form.get('current_milage')
    try:
        response = BookingBasics.end_ride(booking_id, end_km, current_milage, end_time)
    except Exception as exp:
        return exp.args[0]

    return response


