from flask import Blueprint, current_app
from . import db
from flask import Flask, render_template, request, redirect
from .data_models import FridgeItem
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import secrets

from wimf.data_models import FridgeItem
from wimf.helpers import db_convert_isodate

# from wimf import app

bp = Blueprint("views", __name__, url_prefix="/")

class ItemForm(FlaskForm):
    name = StringField("name of item", validators=[DataRequired(), Length(1, 60)])
    submit = SubmitField("Submit")

@bp.route('/', methods=["GET", "POST"])
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
		
    form = ItemForm()
    if form.validate_on_submit():
        print(form.name.data)
    else:
        print("sadge")
    return render_template("dashboard.html", current_items=current_items, form=form)

@bp.route('/items')
def items():
    return "implement me!"

@bp.route('/saved_items')
def saved_items():
    return "implement me!"

@bp.route('/recipes')
def recipes():
    return "implement me!"
