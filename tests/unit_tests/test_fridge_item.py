import pytest
from wimf.data_models import FridgeItem
from datetime import date, timedelta, datetime
def test_FridgeItem_init_minimal():
    #TODO

    today = date.today()
    oneweek = today + timedelta(days=7)
    """Tests whether constructing a FridgeItem object using 'test' as
    a name and an expiry time of 4, with two date that works for 4 day expiry."""
    item = FridgeItem(1, "test", 1, today, oneweek, 0)
    assert item.item_id == 1
    assert item.name == "test"
    assert item.quantity == 1
    assert item.date_added == today
    assert item.expiry_date == oneweek
    assert item.archived == 0

def test_FridgeItem_specify_date_added_and_expiry():
    """Tests what happens when we specify a date_added in the constructor."""
    today = date.today()
    a_week_ago = today - timedelta(days=7)
    item = FridgeItem(1, "test", 1, today, a_week_ago, 0)
    assert item.item_id == 1
    assert item.name == "test"
    assert item.date_added == today
    assert item.expiry_date == date.today() - timedelta(days=7)
    assert item.archived == 0

def test_FridgeItem_noExpiry_simple():

    """Make a simple FridgeItem where expiry_time == None, verify
    days_to_expiry returns sane values"""

    today = date.today()
    item = FridgeItem(1, "test", 1, today, None, 0)
    assert item.item_id == 1
    assert item.name == "test"
    assert item.expiry_date == None
    assert item.date_added == today
    assert item.days_to_expiry() == None
    assert item.archived == 0


def test_FridgeItem_update_expiry():
    today = date.today()
    tomorrow = date.today() + timedelta(days=1)
    item = FridgeItem(1, "test", 1, today, today, 0)
    assert item.expiry_date == today
    item.update_expiry(tomorrow)
    assert item.expiry_date == tomorrow
    assert item.days_to_expiry() == 1
    assert item.archived == 0
