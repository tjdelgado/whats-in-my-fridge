from flask import Blueprint, current_app
from . import db
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from .data_models import FridgeItem
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
import secrets
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from wimf.data_models import FridgeItem
from wimf.helpers import db_convert_isodate

bp = Blueprint("views", __name__, url_prefix="/")

class ItemForm(FlaskForm):
    name = StringField("Name of item", validators=[DataRequired(), Length(1, 60)])
    dayAdded = DateField("Day added", format="%Y-%m-%d", default=datetime.now())
    expiryDay = DateField("Day expiry", format="%Y-%m-%d", default=datetime.now())
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField("Submit")

@bp.route('/', methods=["GET", "POST"])
def dashboard():
    mydb = db.get_db()
    rows = mydb.execute("SELECT * FROM ITEMS").fetchall()

    current_items = []
    for r in rows:
        quantity = r['quantity'] if 'quantity' in r.keys() else 1  # Default to 1 if quantity column is missing
        current_item = FridgeItem(r["id"], r["name"], r["expiry_time"],
                                  db_convert_isodate(r["date_added"]),
                                  db_convert_isodate(r["expiry_date"]),
                                  quantity)
        current_items.append(current_item)

    form = ItemForm()
    if form.validate_on_submit():
        name = form.name.data
        dayAdded = form.dayAdded.data
        expiryDay = form.expiryDay.data
        quantity = form.quantity.data
        newItem = FridgeItem(None, name, None, dayAdded, expiryDay, quantity)
        c = mydb.cursor()
        c.execute("INSERT INTO ITEMS (name, expiry_time, date_added, expiry_date, quantity) VALUES (?, ?, ?, ?, ?)", 
                  (newItem.name, newItem.expiry_time, newItem.date_added, newItem.expiry_date, newItem.quantity))
        mydb.commit()
        return redirect(url_for("views.success"))
    else:
        print("Form submission failed")
    return render_template("dashboard.html", current_items=current_items, form=form)

@bp.route('<int:item_id>/edit', methods=['POST', 'GET'])
def edit_item(item_id):
    editForm = ItemForm()
    mydb = db.get_db()

    if request.method == "GET":
        item = mydb.execute("SELECT * FROM ITEMS WHERE id = ?", (item_id,)).fetchone()
        if item:
            # Check if 'quantity' column exists and handle it accordingly
            quantity = item['quantity'] if 'quantity' in item.keys() else 1

            current_item = FridgeItem(item["id"], item["name"], item["expiry_time"], 
                                      db_convert_isodate(item["date_added"]), 
                                      db_convert_isodate(item["expiry_date"]), 
                                      quantity)
            editForm.name.data = current_item.name
            editForm.dayAdded.data = current_item.date_added
            editForm.expiryDay.data = current_item.expiry_date
            editForm.quantity.data = current_item.quantity
            return render_template("edit.html", editForm=editForm, item_id=item_id)
    else:
        if editForm.validate_on_submit():
            newName = editForm.name.data
            newDateAdded = editForm.dayAdded.data
            newExpiryDate = editForm.expiryDay.data
            newQuantity = editForm.quantity.data
            c = mydb.cursor()
            editQuery = "UPDATE ITEMS SET name = ?, expiry_time = ?, date_added = ?, expiry_date = ?, quantity = ? WHERE id = ?"
            c.execute(editQuery, (newName, None, newDateAdded, newExpiryDate, newQuantity, item_id))
            mydb.commit()
            return redirect(url_for("views.dashboard"))

    return redirect(url_for("views.edit_item", item_id=item_id))

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

@bp.route('/items')
def items():
    return "implement me!"

@bp.route('/saved_items')
def saved_items():
    return "implement me!"

@bp.route('/recipes')
def recipes():
    return "implement me!"
