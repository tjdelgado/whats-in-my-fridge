import pytest
from wimf.data_models import FridgeItem
from datetime import date, timedelta
def test_FridgeItem_init_minimal():
    """Tests whether constructing a FridgeItem object using 'test' as
    a name and an expiry time of 1, with no other params works as expected."""
    item = FridgeItem("test", 1)
    assert item.name == "test"
    assert item.expiry_time == 1
    assert item.date_added == date.today()
    assert item.expiry_date == date.today() + timedelta(days=1)

def test_FridgeItem_specify_date_added():
    """Tests what happens when we specify a date_added in the constructor."""
    a_week_ago = date.today() - timedelta(days=7)
    item = FridgeItem("test", 1, date_added=a_week_ago)
    assert item.name == "test"
    assert item.expiry_time == 1
    assert item.expiry_date == date.today() - timedelta(days=7) + timedelta(days=1)

def test_FridgeItem_specify_added_and_expiry_date():
    """TODO"""
    assert 1 == 1
def test_FridgeItem_noExpiry_simple():
    """Make a simple FridgeItem where expiry_time == None, verify behavior."""
    item = FridgeItem("test", None)
    assert item.name == "test"
    assert item.expiry_time == None
    assert item.expiry_date == None
    assert item.date_added == date.today()

def test_FridgeItem_noExpiry_dateadded():
    #TODO
    assert 1 == 1

def test_FridgeItem_noExpiry_expiry():
    #TODO
    assert 1 == 1
