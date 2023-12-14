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

import sqlite3

from wimf.data_models import FridgeItem
from wimf.helpers import *

bp = Blueprint("views", __name__, url_prefix="/")

@bp.route('/', methods=["GET", "POST"])
def dashboard():
    sort = request.args.get('sort', 'name')
    direction = request.args.get('direction', 'asc')

    rows = get_current_items(sort, direction)
    current_items = [FridgeItem(r["id"], r["name"], r["quantity"], db_convert_isodate(r["date_added"]), db_convert_isodate(r["expiry_date"]), r["archived"]) for r in rows]

    current_tags = retrieve_current_tags()
    form = ItemForm()

    # prepopulate the tags form choices
    if request.method == "GET":
        tags = retrieve_all_tags()
        form.tags.choices = [(g["id"], g["name"]) for g in tags]

    if form.validate_on_submit():
        add_new_item(form)
        return redirect(url_for("views.success"))

    return render_template("dashboard.html", current_items=current_items, form=form, current_tags=current_tags)


# add tags
@bp.route('/tags', methods=["POST", "GET"])
def addTags():
    tagForm = TagForm()
    if request.method == "GET":
        rowsTag = retrieve_all_tags()
        return render_template("tags.html", tagForm=tagForm, rowsTag=rowsTag)

    if tagForm.validate_on_submit():
        name = tagForm.name.data
        add_new_tag(name)
        return redirect(url_for("views.dashboard"))
    return render_template("tags.html", tagForm=tagForm)

@bp.route('/success')
def success():
    return render_template("success.html")

@bp.route('/<int:tag_id>/delete_tag', methods=["POST"])
def delete_tag(tag_id):
    delete_tag_query(tag_id)
    return redirect(url_for("views.dashboard"))

@bp.route('/<int:item_id>/delete_item', methods=['POST', 'GET'])
def delete_item(item_id):
    delete_item_query(item_id)
    return redirect(url_for("views.dashboard"))

@bp.route('/<int:tag_id>/listbytag', methods=['POST', 'GET'])
def list_by_tag(tag_id):
    tagName = tag_name(tag_id)
    allId = listing_id(tag_id)
    current_items = [FridgeItem(r["id"], r["name"], r["quantity"], db_convert_isodate(r["date_added"]), db_convert_isodate(r["expiry_date"]), r["archived"]) for r in allId]
    return render_template("items_by_tag.html", current_items=current_items, tagName=tagName)

@bp.route('/<int:tag_id>/editTag', methods=['POST', 'GET'])
def edit_tag(tag_id):
    editTag = TagForm()
    if request.method == "GET":
        tag = get_tag(tag_id)
        if tag:
            editTag.name.data = tag["name"]
        return render_template("edit_tag.html", tagForm=editTag)

    else:
        if editTag.validate_on_submit():
            newName = editTag.name.data
            update_tag(tag_id, newName)
            return redirect(url_for("views.addTags"))

@bp.route('/<int:item_id>/editItem', methods=['POST', 'GET'])
def edit_item(item_id):
    editForm = ItemForm()
    if request.method == "GET":
        item = retrieve_item(item_id)
        tags = retrieve_all_tags()

        if item:
            populate_edit_form(editForm, item, tags)
        return render_template("edit_item.html", editForm=editForm)

    else:
        if editForm.validate_on_submit():
            update_item(editForm, item_id)
            return redirect(url_for("views.dashboard"))

# archived function, let the user archived or unarchived the item they want
@bp.route('/<int:item_id>/archived/<int:archived>', methods=['POST', 'GET'])
def archived_item(item_id, archived):
    if request.method == "POST":
        change_archived_status(item_id, archived)
        return redirect(url_for("views.dashboard"))

    return redirect(url_for("views.success"))


@bp.route('/archived_list', methods=["GET"])
def archived_list():
    rows = get_archived_items()
    archived_items = [FridgeItem(r["id"], r["name"], r["quantity"], db_convert_isodate(r["date_added"]), db_convert_isodate(r["expiry_date"]), r["archived"]) for r in rows]
    return render_template("archived.html", archived_items=archived_items)
