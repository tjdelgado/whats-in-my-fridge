# code adapted from the Flask tutorial at
# https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/

# package definition for main wimf app and also "app factory" for Flask

import os

#import db handling
from . import db


from flask import Flask, render_template, request, redirect
from wimf.data_models import FridgeItem

from wimf.helpers import db_convert_isodate


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='DEVKEY',
        DATABASE=os.path.join(app.instance_path, 'wimf.db'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that serves items table contents as strings
    @app.route('/')
    def dashboard():
        mydb = db.get_db()
        rows = mydb.execute(
            "SELECT * FROM ITEMS"
        ).fetchall()

        current_items = [FridgeItem(r["name"],
                                    r["expiry_time"],
                                    db_convert_isodate(r["date_added"]),
                                    db_convert_isodate(r["expiry_date"]))
                         for r in rows]
        #breakpoint()
        return render_template("dashboard.html", current_items=current_items)

    @app.route('/items')
    def items():
        return "implement me!"

    @app.route('/saved_items')
    def saved_items():
        return "implement me!"

    @app.route('/recipes')
    def recipes():
        return "implement me!"



    db.init_app(app)

    return app
