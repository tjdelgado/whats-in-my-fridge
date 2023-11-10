# code adapted from the Flask tutorial at
# https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/

# package definition for main wimf app and also "app factory" for Flask

import os

#import db handling
from . import db

from flask import Flask


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

        # stub for now - turns database rows into strings for dumb output
        retstr = ""
        for r in rows:
            for k in r.keys():
                retstr += str(k) + ": " + str(r[k]) + ', '
            retstr += "\n"
        return retstr

    db.init_app(app)

    return app
