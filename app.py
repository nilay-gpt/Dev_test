from flask import Flask

from utils.db import load_db
from utils.db import terminating_sn

from views.booking import booking_blueprint
from data_api.migrations import InitializeData
from models.car import Categories

app = Flask(__name__)


def start_app():
    # Create DB
    load_db()

    # Register Blueprint
    app.register_blueprint(booking_blueprint)
    return app

def init_db():
    # Run Migrations
    with terminating_sn() as session:
        category = session.query(Categories).first()
        if not category:
            InitializeData.init_customers()
            InitializeData.init_category()
            InitializeData.init_common_price()
            InitializeData.init_car_details()

if __name__ == '__main__':
    start_app()
    init_db()
    app.run(debug=True)
    # app.run()
