"""Helper functions for the main body of the app --- things like date parsing and the like."""

from datetime import date
from wimf import db
import sqlite3
from wimf.data_models import ItemForm, TagForm

def db_convert_isodate(s: str) -> date:

    """Meant for converting dates from date columns in the db to
    python date.datetime objects. Made because SQLite seems to have
    some quirks in how it outputs TEXT columns storing iso-formatted
    dates.

    Attempts to convert a isoformat date string (ideally
    YYYY-MM-DD) to a datetime.date object. Does some simple
    sanitization of the input.

    In case the db spits out NULL (python None) then spit out a None too.
    Returns None if a ValueError/TypeError occurred.
    """
    if s is None:
        return None
    try:
        return date.fromisoformat(s.strip())
    except (ValueError, TypeError, AttributeError):
        return None
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        raise

def format_quantity(quantity: int) -> str:
    return f"{quantity} pcs"

def delete_tag_query(tag_id: int) -> bool:
    mydb = db.get_db()
    c = mydb.cursor()
    c.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
    mydb.commit()
    return True

def delete_item_query(item_id: int) -> bool:
    mydb = db.get_db()
    c = mydb.cursor()
    c.execute("DELETE FROM ITEMS WHERE id = ?", (item_id,))
    mydb.commit()
    return True

def retrieve_current_tags() -> list[sqlite3.Row]:
    mydb = db.get_db()
    query = "SELECT * FROM tags INNER JOIN item_tags ON tags.id = item_tags.tag_id"
    currentTags = mydb.execute(query).fetchall()
    return currentTags

def retrieve_all_tags() -> list[sqlite3.Row]:
    mydb = db.get_db()
    query = "SELECT * FROM tags;"
    tags = mydb.execute(query).fetchall()
    return tags

def add_new_tag(name: str) -> bool:
    mydb = db.get_db()
    query = "INSERT INTO tags ( name ) VALUES (?)"
    mydb.execute(query, (name,))
    mydb.commit()
    return True

# populate the item_tags db
def addTagsToJunctionTable(rowId, tags) -> int:
    mydb = db.get_db()
    for tag in tags:
        c = mydb.cursor()
        c.execute("INSERT INTO item_tags (item_id, tag_id) VALUES (?, ?)", (rowId, tag))
        mydb.commit()
    return 0

def update_tag(id: int, new_name: str) -> bool:
    mydb = db.get_db()
    c = mydb.cursor()
    c.execute("UPDATE tags SET name = ? WHERE id = ?", (new_name, id, ))
    mydb.commit()
    return True

#### below needs to have tests written for them
# retrive tags of all items in the items table
def get_tag(id: int) -> sqlite3.Row:
    mydb = db.get_db()
    c = mydb.cursor()
    return c.execute("SELECT * FROM tags WHERE id = ?", (id,)).fetchone()

def get_archived_items() -> list[sqlite3.Row]:
    mydb = db.get_db()
    query = f"SELECT * FROM ITEMS WHERE archived = 1"
    rows = mydb.execute(query).fetchall()
    return rows

def change_archived_status(item_id: int, archived: int) -> bool:
    mydb = db.get_db()
    c = mydb.cursor()
    c.execute("UPDATE ITEMS SET archived = ? WHERE id = ?", (archived, item_id))
    mydb.commit()
    return True

def retrieve_item(item_id: int) -> sqlite3.Row:
    mydb = db.get_db()
    item = mydb.execute("SELECT * FROM ITEMS WHERE id = ?", (item_id,)).fetchone()
    return item

def listing_id(tag_id) -> sqlite3.Row:
    mydb = db.get_db()
    c = mydb.cursor()
    allId = c.execute("SELECT * FROM ITEMS INNER JOIN item_tags ON item_tags.item_id = ITEMS.id WHERE item_tags.tag_id = ?", (tag_id,)).fetchall()
    return allId

def tag_name(tag_id) -> sqlite3.Row :
    mydb = db.get_db()
    c = mydb.cursor()
    tagName = c.execute("SELECT name FROM tags where id = ?", (tag_id,)).fetchone()
    return tagName

def update_item(editForm: ItemForm, item_id: int) -> bool:
    mydb = db.get_db()
    newName = editForm.name.data
    newQuantity = editForm.quantity.data
    newDateAdded = editForm.dayAdded.data
    newExpiryDate = editForm.expiryDay.data
    tags = editForm.tags.data
    remove_tags_item(item_id)
    addTagsToJunctionTable(item_id, tags)
    c = mydb.cursor()
    c.execute("UPDATE ITEMS SET name = ?, quantity = ?, date_added = ?, expiry_date = ? WHERE id = ?", (newName, newQuantity, newDateAdded, newExpiryDate, item_id))
    mydb.commit()
    return True

def remove_tags_item(item_id) -> bool:
    mydb = db.get_db()
    c = mydb.cursor()
    c.execute("DELETE FROM item_tags WHERE item_id = ?", (item_id,))
    return True

def populate_edit_form(editForm: ItemForm,
                       item: sqlite3.Row,
                       tags: list[sqlite3.Row]) -> bool:
    editForm.name.data = item["name"]
    editForm.quantity.data = item["quantity"]
    editForm.dayAdded.data = db_convert_isodate(item["date_added"])
    editForm.expiryDay.data = db_convert_isodate(item["expiry_date"])
    editForm.tags.choices = [(g["id"], g["name"]) for g in tags]
    return True

def get_current_items(sort: str, direction: str) -> list[sqlite3.Row]:
    mydb = db.get_db()
    query = f"SELECT * FROM ITEMS WHERE archived = 0 ORDER BY {sort} {direction} "
    rows = mydb.execute(query).fetchall()
    return rows

def add_new_item(form: ItemForm) -> bool:
    mydb = db.get_db()
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

    addTagsToJunctionTable(lastId, tags)

    return True

# used as a filter for the jinja templates to select appropriate style for rows
def expiry_status(days_to_expiry):
    if days_to_expiry is None:
        return ''
    elif days_to_expiry <= 0:
        return 'expired'
    elif days_to_expiry <= 3:
        return 'expiring-soon'
    else:
        return ''
