from . import db
from flask import Flask, render_template, request, redirect, url_for, Blueprint, current_app
from datetime import datetime
from .data_models import FridgeItem
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, DateField, TimeField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Length, NumberRange
import secrets
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from wimf.data_models import FridgeItem
from wimf.helpers import db_convert_isodate

bp = Blueprint("views", __name__, url_prefix="/")

class ItemForm(FlaskForm):
    name = StringField("Name of Item", validators=[DataRequired(), Length(1, 60)])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)], default=1)
    dayAdded = DateField("Day Added", format="%Y-%m-%d", default=datetime.now()) 
    expiryDay = DateField("Day Expiry", format="%Y-%m-%d", default=datetime.now()) 
    tags = SelectMultipleField(label="tags", choices=[], coerce=int, validate_choice=False)
    submit = SubmitField("submit")

class TagForm(FlaskForm):
    name = StringField("Tag name", validators=[DataRequired(), Length(1, 60)])
    submit = SubmitField("submit")



@bp.route('/', methods=["GET", "POST"])
def dashboard():
    sort = request.args.get('sort', 'name')
    direction = request.args.get('direction', 'asc')
    mydb = db.get_db()
    query = f"SELECT * FROM ITEMS WHERE archived = 0 ORDER BY {sort} {direction} "
    rows = mydb.execute(query).fetchall()
    current_items = [FridgeItem(r["id"], r["name"], r["quantity"], db_convert_isodate(r["date_added"]), db_convert_isodate(r["expiry_date"]), r["archived"]) for r in rows]
    current_tags = retrieveTags()
    form = ItemForm()
    # prepopulate the tags form choices
    if request.method == "GET":
        queryTags = f"SELECT * FROM tags"
        tags = mydb.execute(queryTags).fetchall()
        form.tags.choices = [(g["id"], g["name"]) for g in tags]
    if form.validate_on_submit():
        name = form.name.data
        quantity = form.quantity.data
        dayAdded = form.dayAdded.data
        expiryDay = form.expiryDay.data
        expiryTime = (expiryDay - dayAdded).days
        tags = form.tags.data
        c = mydb.cursor()
        # Assuming you want to set expiry_time to a default value like 0
        # set archived at 0 by default
        c.execute("INSERT INTO ITEMS (name, quantity, expiry_time, date_added, expiry_date, archived) VALUES (?, ?, ?, ?, ?, ?) RETURNING id", (name, quantity, expiryTime, dayAdded, expiryDay, 0))  
        c.fetchall()
        lastId = c.lastrowid
        mydb.commit()
        addTagsToDb(lastId, tags)
        return redirect(url_for("views.success"))
    return render_template("dashboard.html", current_items=current_items, form=form, current_tags=current_tags)


# add tags
@bp.route('/tags', methods=["POST", "GET"])
def addTags():
    mydb = db.get_db()
    tagForm = TagForm()
    if request.method == "GET":
        queryTag = f"SELECT * FROM tags"
        rowsTag = mydb.execute(queryTag).fetchall()
        return render_template("tags.html", tagForm=tagForm, rowsTag=rowsTag)
    if tagForm.validate_on_submit():
        c = mydb.cursor()
        name = tagForm.name.data
        print(name)
        c.execute("INSERT INTO tags ( name ) VALUES (?)", (name,))
        mydb.commit()
        return redirect(url_for("views.dashboard"))
    return render_template("tags.html", tagForm=tagForm)


# retrive all tags
def retrieveTags():
    mydb = db.get_db()
    query = "SELECT * FROM tags INNER JOIN item_tags ON tags.id = item_tags.tag_id"
    currentTags = mydb.execute(query).fetchall()
    return currentTags

# populate the item_tags db
def addTagsToDb(rowId, tags):
    mydb = db.get_db()
    for tag in tags:
        c = mydb.cursor()
        c.execute("INSERT INTO item_tags (item_id, tag_id) VALUES (?, ?)", (rowId, tag))
        mydb.commit()
    return 0

@bp.route('/success')
def success():
    return render_template("success.html") 

@bp.route('/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    mydb = db.get_db()
    c = mydb.cursor()
    c.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
    mydb.commit() 
    return redirect(url_for("views.dashboard"))


@bp.route('/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    mydb = db.get_db()
    c = mydb.cursor()
    c.execute("DELETE FROM ITEMS WHERE id = ?", (item_id,))
    mydb.commit() 
    return redirect(url_for("views.dashboard"))

@bp.route('/<int:tag_id>/edit', methods=['POST', 'GET'])
def edit_tag(tag_id):
    editTag = TagForm()
    mydb = db.get_db()
    if request.method == "GET":
        tag = mydb.execute("SELECT * FROM tags WHERE id = ?", (tag_id,)).fetchone()
        if tag:
            editTag.name.data = tag["name"]
        return render_template("edit_tag.html", tagForm=editTag)
    else:
        if editTag.validate_on_submit():
            newName = editTag.name.data
            c = mydb.cursor()
            c.execute("UPDATE tags SET name = ? WHERE id = ?", (newName, tag_id, ))
            mydb.commit()
            return redirect(url_for("views.addTags"))
        
        
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
        return render_template("edit_item.html", editForm=editForm)
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

# archived function, let the user archived or unarchived the item they want
@bp.route('/<int:item_id>/archived/<int:archived>', methods=['POST', 'GET'])
def archived_item(item_id, archived):
    mydb = db.get_db()
    if request.method == "POST":
        c = mydb.cursor()
        c.execute("UPDATE ITEMS SET archived = ? WHERE id = ?", (archived, item_id))
        mydb.commit()
        return redirect(url_for("views.dashboard"))

    return redirect(url_for("views.success"))


@bp.route('/archived_list', methods=["GET"])
def archived_list():
    mydb = db.get_db()
    query = f"SELECT * FROM ITEMS WHERE archived = 1"
    rows = mydb.execute(query).fetchall()
    archived_items = [FridgeItem(r["id"], r["name"], r["quantity"], db_convert_isodate(r["date_added"]), db_convert_isodate(r["expiry_date"]), r["archived"]) for r in rows]
    return render_template("archived.html", archived_items=archived_items)
    

@bp.route('/items')
def items():
    return "implement me!"

@bp.route('/saved_items')
def saved_items():
    return "implement me!"

@bp.route('/recipes')
def recipes():
    return "implement me!"