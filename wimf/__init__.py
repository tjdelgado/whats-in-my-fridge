# code adapted from the Flask tutorial at
# https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/

# package definition for main wimf app and also "app factory" for Flask

import os

#import db handling
from . import db
from wimf import views
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import secrets

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

    app.secret_key = secrets.token_urlsafe(16)
    Bootstrap5(app)
    CSRFProtect(app)

    db.init_app(app)
    app.register_blueprint(views.bp)

    return app