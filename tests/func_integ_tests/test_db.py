# python -m pytest tests/test_db.py
# Do the above in terminal to run
import pytest
from flask import Flask
from wimf.db import get_db, init_db
from wimf.data_models import FridgeItem
import os

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Path for the database
    db_path = os.path.join(os.path.dirname(__file__), 'test.db')

    # Create the Flask app
    app = Flask(__name__, instance_relative_config=True)
    app.config['DATABASE'] = db_path  # Direct path without 'sqlite:///' prefix

    with app.app_context():
        init_db()  # Initialize the database

    yield app

    # Teardown: remove the temporary database
    os.remove(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

def test_database_initialization(app):
    with app.app_context():
        db = get_db()
        assert db.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='items'").fetchone()[0] == 1

def test_insert_fridge_item(app):
    test_item = FridgeItem(item_id=1, name="Milk", expiry_time=7, date_added='2023-01-01', expiry_date='2023-01-08')
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO items (name, expiry_time, date_added, expiry_date) VALUES (?, ?, ?, ?)",
                   (test_item.name, test_item.expiry_time, test_item.date_added, test_item.expiry_date))
        db.commit()

        item = db.execute("SELECT * FROM items WHERE name = ?", (test_item.name,)).fetchone()
        assert item is not None
        assert item["id"] is not None 
        assert item["name"] == test_item.name
        assert item["expiry_time"] == test_item.expiry_time
