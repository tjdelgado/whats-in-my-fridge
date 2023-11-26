from . import db
from flask import Flask, render_template, request, redirect, url_for, Blueprint, current_app
from datetime import datetime
from .data_models import FridgeItem
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
import secrets
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from wimf.data_models import FridgeItem
from wimf.helpers import db_convert_isodate

bp = Blueprint("views", __name__, url_prefix="/")

class ItemForm(FlaskForm):
    name = StringField("Name of Item", validators=[DataRequired(), Length(1, 60)])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)], default=1)
    dayAdded = DateField("Day Added", format="%Y-%m-%d", default=datetime.now()) 
    expiryDay = DateField("Day Expiry", format="%Y-%m-%d", default=datetime.now()) 
    submit = SubmitField("Submit")

@bp.route('/', methods=["GET", "POST"])
def dashboard():
    sort = request.args.get('sort', 'name')
    direction = request.args.get('direction', 'asc')
    mydb = db.get_db()
    query = f"SELECT * FROM ITEMS ORDER BY {sort} {direction}"
    rows = mydb.execute(query).fetchall()
    current_items = [FridgeItem(r["id"], r["name"], r["quantity"], db_convert_isodate(r["date_added"]), db_convert_isodate(r["expiry_date"])) for r in rows]
    form = ItemForm()
    if form.validate_on_submit():
        name = form.name.data
        quantity = form.quantity.data
        dayAdded = form.dayAdded.data
        expiryDay = form.expiryDay.data
        c = mydb.cursor()
        # Assuming you want to set expiry_time to a default value like 0
        c.execute("INSERT INTO ITEMS (name, quantity, expiry_time, date_added, expiry_date) VALUES (?, ?, ?, ?, ?)", (name, quantity, 0, dayAdded, expiryDay))  
        mydb.commit()
        return redirect(url_for("views.success"))
    return render_template("dashboard.html", current_items=current_items, form=form)

@bp.route('/success')
def success():
    return render_template("success.html") 

@bp.route('/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    mydb = db.get_db()
    c = mydb.cursor()
    c.execute("DELETE FROM ITEMS WHERE id = ?", (item_id,))
    mydb.commit() 
    return redirect(url_for("views.dashboard"))

@bp.route('/<int:item_id>/edit', methods=['POST', 'GET'])
def edit_item(item_id):
    editForm = ItemForm()
    mydb = db.get_db()
    if request.method == "GET":
        item = mydb.execute("SELECT * FROM ITEMS WHERE id = ?", (item_id,)).fetchone()
        if item:
            editForm.name.data = item["name"]
            editForm.quantity.data = item["quantity"]
            editForm.dayAdded.data = db_convert_isodate(item["date_added"])
            editForm.expiryDay.data = db_convert_isodate(item["expiry_date"])
        return render_template("edit.html", editForm=editForm)
    else:
        if editForm.validate_on_submit():
            newName = editForm.name.data
            newQuantity = editForm.quantity.data
            newDateAdded = editForm.dayAdded.data
            newExpiryDate = editForm.expiryDay.data
            c = mydb.cursor()
            c.execute("UPDATE ITEMS SET name = ?, quantity = ?, date_added = ?, expiry_date = ? WHERE id = ?", (newName, newQuantity, newDateAdded, newExpiryDate, item_id))
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