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

    """Tests the dashboard template's table rendering logic to make
    sure that inputted items are rendered appropriately."""

    # need request_context to simulate a request so we can call render_template
    with app.test_request_context("/", method="GET"):
        # this is similar to the render_template call in the dashboard endpoint
        items = [FridgeItem(1, "test", 0, date.today(), date.today())]
        templ = render_template("dashboard.html", form=ItemForm(), \
                               current_items=items)

    # parse the whole rendered template
    parsed = BeautifulSoup(templ, features="html.parser")

    # get all rows in the tbody
    table_rows = parsed.table.tbody.find_all('tr')

    # we added just one item so should be just one row
    assert len(table_rows) == 1

    # for some reason BS4 parses newlines as elements in the DOM
    # so we'll filter them out
    cols = [td for td in table_rows[0] if td != '\n']

    assert cols[0].text == 'test'
    assert cols[1].text == '0'
    assert cols[2].text == date.today().isoformat()
    assert cols[3].text == date.today().isoformat()

    #breakpoint()
    assert templ is not None
    #  TODO: make test better!

def test_dashboard_highlight_expiring_soon(app):
    # TODO
    assert 1 == 1

def test_dashboard_highlight_expired(app):
    # TODO
    assert 1 == 1

def test_dashboard_no_expiry_render(app):
    # TODO
    assert 1 == 1
