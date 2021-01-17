"""
This file is responsible for intializing the records for ride sharing applications.
"""

from flask import Blueprint
from utils.db import terminating_sn
from data_api.migrations import InitializeData

init_blueprint = Blueprint('initialize_data', __name__)


@init_blueprint.route('/initialize/data', methods=['POST'])
def migrations():
    """
    This API is responsible for intialisibng the data for Customers, Cars, Category and price inverntory.
    """
    # initializing basic customer details.
    cust_response = InitializeData.init_customers()
    if not cust_response["success"]:
        return response['msg']

    # initializing 3 category details.
    car_resp = InitializeData.init_category()
    if not car_resp["success"]:
        return car_resp['msg']

    # initializing common price details.
    InitializeData.init_common_price()
    # initializing basic car details.
    InitializeData.init_car_details()


    return {"success": True, "msg": "Initial data migrated"}
