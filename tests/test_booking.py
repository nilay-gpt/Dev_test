import os
import json
import base64

import unittest

from conf.settings import config
from utils.db import load_db
from app import start_app

app = start_app()


class TestBooking(unittest.TestCase):

    book_ride_json = {
                        "user":'1',
                        "reg_number": "KA-03 JE 1859",
                        "start_time": '1610985311',
                        "end_time": '1613146587',
                    }

    book_ride_json_negative = {
                                "user":'1',
                                "reg_number": "test Id",
                                "start_time": '1612973787',
                                "end_time": '1613146587',
                            }

    book_ride_json_wrng_dates = {
                                    "user":'1',
                                    "reg_number": "test Id",
                                    "start_time": '2612973787',
                                    "end_time": '1613146587',
                                }
    end_trip_json = {
                        "booking_id": '',
                        "end_km": 1000,
                        "current_milage":10
                    }
    start_trip_json = {
                        "booking_id": '',
                        "start_km": 600
                      }

    @classmethod
    def setUpClass(cls):
        load_db()

    def setUp(self):
        self.BOOK_API_URI = "book/ride"
        self.START_API_URI = "start/ride"
        self.END_API_URI = "end/ride"
        self.headers = {"content_type":"multipart/form-data"}


    def test_book_ride(self):

        with app.test_client() as client:
            # Checking 200
            response = client.post(self.BOOK_API_URI,
                                   data=TestBooking.book_ride_json,
                                   headers=self.headers)


            self.assertEqual(200, json.loads(response.data)['status_code'])

            # Checking 400, when car number is not valid
            response = client.post(self.BOOK_API_URI,
                                   data=TestBooking.book_ride_json_negative,
                                   headers=self.headers)
            self.assertEqual(400, json.loads(response.data)['status_code'])

            # Checking 400, when start date is bigger than end date
            response = client.post(self.BOOK_API_URI,
                                   data=TestBooking.book_ride_json_wrng_dates,
                                   headers=self.headers)
            self.assertEqual(400, json.loads(response.data)['status_code'])

    def test_start_ride(self):

        with app.test_client() as client:
            book_response = client.post(self.BOOK_API_URI,
                                   data=TestBooking.book_ride_json,
                                   headers=self.headers)
            request_data = TestBooking.start_trip_json
            request_data['booking_id'] = json.loads(book_response.data)['booking_id']
            
            # Checking 200
            start_response = client.put(self.START_API_URI,
                                   data=request_data,
                                   headers=self.headers)

            self.assertEqual(200, json.loads(start_response.data)['status_code'])


    def test_end_car(self):

        with app.test_client() as client:

            book_response = client.post(self.BOOK_API_URI,
                                   data=TestBooking.book_ride_json,
                                   headers=self.headers)
            request_data = TestBooking.start_trip_json
            request_data['booking_id'] = json.loads(book_response.data)['booking_id']
            
            start_response = client.put(self.START_API_URI,
                                   data=request_data,
                                   headers=self.headers)

            # Checking 200
            end_req_data =  TestBooking.end_trip_json
            end_req_data["booking_id"] = request_data['booking_id']
            end_response = client.put(self.END_API_URI,
                                   data=end_req_data,
                                   headers=self.headers)


            self.assertEqual(200, json.loads(end_response.data)['status_code'])

            #Checking 400: Re ending the complete trip.
            end_response = client.put(self.END_API_URI,
                                   data=end_req_data,
                                   headers=self.headers)
            self.assertEqual(400, json.loads(end_response.data)['status_code'])



if __name__ == "__main__":
    unittest.main()







