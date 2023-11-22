from flask import Blueprint, current_app
from . import db
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from .data_models import FridgeItem
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired, Length
import secrets
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from wimf.data_models import FridgeItem
from wimf.helpers import db_convert_isodate


bp = Blueprint("views", __name__, url_prefix="/")

class ItemForm(FlaskForm):
    name = StringField("name of item", validators=[DataRequired(), Length(1, 60)])
    dayAdded = DateField("Day added", format="%Y-%m-%d", default=datetime.now()) 
    expiryDay = DateField("Day expiry", format="%Y-%m-%d", default=datetime.now()) 
    submit = SubmitField("Submit")

@bp.route('/', methods=["GET", "POST"])
def dashboard():
    # Default sorting parameters
    sort = request.args.get('sort', 'name')
    direction = request.args.get('direction', 'asc')

    # Database query with sorting
    mydb = db.get_db()
    query = f"SELECT * FROM ITEMS ORDER BY {sort} {direction}"
    rows = mydb.execute(query).fetchall()

    # Convert rows to FridgeItem objects
    current_items = [FridgeItem(r["id"],
                                r["name"],
                                r["expiry_time"],
                                db_convert_isodate(r["date_added"]),
                                db_convert_isodate(r["expiry_date"]))
                     for r in rows]


    c = mydb.cursor()
    form = ItemForm()
    if form.validate_on_submit():
        name = request.form["name"]
        dayAdded = request.form["dayAdded"]
        expiryDay = request.form["expiryDay"]
        newItem = FridgeItem(None, name, None, dayAdded, expiryDay)
        c.execute("INSERT INTO ITEMS (name, expiry_time, date_added, expiry_date ) VALUES (?, ?, ?, ?)", (newItem.name, newItem.expiry_time, newItem.date_added, newItem.expiry_date))  
        mydb.commit()
        return redirect(url_for("views.success"))
    else:
        print("sadge")
    return render_template("dashboard.html", current_items=current_items, form=ItemForm())

@bp.route('/success')
def success():
    return render_template("success.html") 

@bp.route('/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    mydb = db.get_db()
    print(item_id)
    c = mydb.cursor()
    c.execute("DELETE FROM ITEMS WHERE id = ?", (item_id,))
    mydb.commit() 
    return redirect(url_for("views.dashboard"))

@bp.route('<int:item_id>/edit', methods=['POST', 'GET'])
def edit_item(item_id):
    editForm = ItemForm()
    mydb = db.get_db()
    if request.method == "GET":
        item = mydb.execute("SELECT * FROM ITEMS WHERE id = ?", (item_id,)).fetchall()
        current_item = [FridgeItem(r["id"],
                                    r["name"],
                                    r["expiry_time"],
                                    db_convert_isodate(r["date_added"]),
                                    db_convert_isodate(r["expiry_date"]))
                         for r in item]


        editForm.name.data = current_item[0].name
        editForm.dayAdded.data = current_item[0].date_added
        editForm.expiryDay.data = current_item[0].expiry_date
        return render_template("edit.html", editForm=editForm) 
    else:
        if editForm.validate_on_submit():
            newName = request.form["name"]
            newDateAdded = request.form["dayAdded"]
            newExpiryDate = request.form["expiryDay"]
            updatedItem = FridgeItem(item_id, newName, None, newDateAdded, newExpiryDate)
            c = mydb.cursor()
            editQuery = """UPDATE ITEMS SET name = ? , expiry_time = ? , date_added = ?, expiry_date = ? WHERE id = ?"""
            editData = (updatedItem.name, updatedItem.expiry_time, updatedItem.date_added, updatedItem.expiry_date, item_id)
            c.execute(editQuery, editData)
            mydb.commit()
            return redirect(url_for("views.dashboard"))


@bp.route('/items')
def items():
    return "implement me!"

@bp.route('/saved_items')
def saved_items():
    return "implement me!"

@bp.route('/recipes')
def recipes():
    return "implement me!"
