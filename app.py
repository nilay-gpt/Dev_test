from flask import Flask

from utils.db import load_db

from views.booking import booking_blueprint
from views.initialize_data import init_blueprint

app = Flask(__name__)


def start_app():
    # Create DB
    load_db()

    # Run Migrations
      #for now doing it via API but can be done from here also.


    # Register Blueprint
    app.register_blueprint(booking_blueprint)
    app.register_blueprint(init_blueprint)


if __name__ == '__main__':
    start_app()
    app.run(debug=True)
    # app.run()
