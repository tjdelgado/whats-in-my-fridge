import pytest
from wimf.data_models import FridgeItem
from datetime import date, timedelta, datetime
def test_FridgeItem_init_minimal():
    #TODO
    assert 1 == 1
    """Tests whether constructing a FridgeItem object using 'test' as
    a name and an expiry time of 4, with two date that works for 4 day expiry."""
    # item = FridgeItem(1, "test", 4, "2023-11-20", "2023-11-24")
    # assert item.item_id == 1
    # assert item.name == "test"
    # assert item.expiry_time == 4 
    # assert item.date_added == "2023-11-20" 
    # assert item.expiry_date == "2023-11-24"

def test_FridgeItem_specify_date_added():
    #TODO
    assert 1 == 1
    """Tests what happens when we specify a date_added in the constructor."""
    # a_week_ago = date.today() - timedelta(days=7)
    # item = FridgeItem(1, "test", 1, date_added=a_week_ago)
    # assert item.item_id == 1
    # assert item.name == "test"
    # assert item.expiry_time == 1
    # assert item.expiry_date == date.today() - timedelta(days=7) + timedelta(days=1)

def test_FridgeItem_specify_added_and_expiry_date():
    """TODO"""
    assert 1 == 1
def test_FridgeItem_noExpiry_simple():
    #TODO
    assert 1 == 1
    # """Make a simple FridgeItem where expiry_time == None, verify calculation is goodj."""
    # item = FridgeItem(1, "test", None, "2023-11-20", "2023-11-24")
    # assert item.item_id == 1
    # assert item.name == "test"
    # assert item.expiry_time == 4 
    # assert item.expiry_date == "2023-11-24" 
    # assert item.date_added == "2023-11-20" 


def test_FridgeItem_noExpiry_expiry():
    #TODO
    assert 1 == 1
