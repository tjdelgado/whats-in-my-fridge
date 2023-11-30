# runs a basic functional test on the dashboard
# Note that we're actually mocking a client and server with the Flask libs
# so these do count as unit tests...

from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import pytest
from flask import render_template
from wimf.data_models import FridgeItem
from wimf.views import ItemForm

def test_dashboard_table_display(app):

    # TODO need to restructure dashboard template etc to make this test make sense
    with app.test_request_context("/", method="GET"):
        a = render_template("dashboard.html",
                            form=ItemForm(),
                            current_items=[FridgeItem(1,
                                                      "test",
                                                      0,
                                                      date.today(),
                                                      date.today())])
    assert a is not None
    #  TODO: make test better!
