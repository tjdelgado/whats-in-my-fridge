from flask import Blueprint
from . import db
from flask import Flask, render_template, request, redirect
from .data_models import FridgeItem
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import secrets
# from . import app

bp = Blueprint("views", __name__, url_prefix="/")

@bp.route('/')
def dashboard():
    mydb = db.get_db()
    rows = mydb.execute(
        "SELECT * FROM ITEMS"
    ).fetchall()

    current_items = [FridgeItem(r["name"],
                                r["expiry_time"],
                                r["date_added"],
                                r["expiry_date"])
                     for r in rows]

    #breakpoint()
    return render_template("dashboard.html", current_items=current_items)

