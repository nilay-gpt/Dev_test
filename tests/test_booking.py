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
                        "start_time": '1612973787',
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

    @classmethod
    def setUpClass(cls):
        load_db()

    def setUp(self):
        self.BOOK_API_URI = "book/ride"
        self.START_API_URI = "start/ride"
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
            # Checking 200
            response = client.post(self.BOOK_API_URI,
                                   data=TestBooking.book_ride_json,
                                   headers=self.headers)
            data = {
                    "booking_id": json.loads(response.data)['booking_id'],
                    "start_km": 1000
                    }

            response = client.put(self.START_API_URI,
                                   data=data,
                                   headers=self.headers)

            self.assertEqual(200, json.loads(response.data)['status_code'])


    # def test_end_car(self):



if __name__ == "__main__":
    unittest.main()







