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
    This API is responsible for intialisibng the data for Customers, Cars and price inverntory.
    """
    # cust_response = InitializeData.init_customers()
    # if not cust_response["success"]:
    #     return response['msg']
    # car_resp = InitializeData.init_category()
    # if not car_resp["success"]:
    #     return car_resp['msg']

    InitializeData.init_common_price()
    # InitializeData.init_car_details()


    return {"success": True, "msg": "Initial data migrated"}
