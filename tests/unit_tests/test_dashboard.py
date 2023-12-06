# runs a basic functional test on the dashboard
# Note that we're actually mocking a client and server with the Flask libs
# so these do count as unit tests...


from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import pytest
from flask import render_template
from wimf.data_models import FridgeItem
from wimf.views import ItemForm

def test_dashboard_template_view_empty(app):
    """Tests that the archive template appropriately says there's
    nothing in the fridge when current_items is empty."""

    with app.test_request_context("/", method="GET"):
        items = []
        templ = render_template("dashboard.html", form=ItemForm(), \
                               current_items=items)

    # parse the whole rendered template
    parsed = BeautifulSoup(templ, features="html.parser")

    # get all rows in the tbody
    table_rows = parsed.find_all('tr')

    # should be no rows
    assert len(table_rows) == 0

    # get all <p> in the page
    p_elts = parsed.find_all('p')

    # should be exactly 1
    assert len(p_elts) == 1

    assert p_elts[0].text == 'Nothing in the fridge!'


def test_dashboard_table_display(app):

    """Tests the dashboard template's table rendering logic to make
    sure that inputted items are rendered appropriately."""

    # need request_context to simulate a request so we can call render_template
    with app.test_request_context("/", method="GET"):
        # this is similar to the render_template call in the dashboard endpoint
        items = [FridgeItem(1, "test", 0, date.today(), date.today(), 0)]
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


def test_dashboard_highlight_expiring_soon(app):
    """Make items with 1-3 days left til expiry are highlighted in
    yellow / have appropriate styling applied"""
    today = date.today()
    tomorrow = date.today() + timedelta(days=1)
    twodays = date.today() + timedelta(days=2)
    threedays = date.today() + timedelta(days=3)

    with app.test_request_context("/", method="GET"):
        # this is similar to the render_template call in the dashboard endpoint
        items = [FridgeItem(1, "tomorrow", 0, today, tomorrow, 0),
                 FridgeItem(2, "twodays", 0, today, twodays, 0),
                 FridgeItem(3, "threedays", 0, today, threedays, 0)]
        templ = render_template("dashboard.html", form=ItemForm(), \
                               current_items=items)

    # parse the whole rendered template
    parsed = BeautifulSoup(templ, features="html.parser")

    # get all rows in the tbody
    table_rows = parsed.table.tbody.find_all('tr')

    # we added just three items should be three rows
    assert len(table_rows) == 3

    assert table_rows[0]["class"] == ['expiring-soon']
    assert table_rows[1]["class"] == ['expiring-soon']
    assert table_rows[2]["class"] == ['expiring-soon']


def test_dashboard_dont_highlight_not_exp_soon(app):
    """Make sure items with 4+ left til expiry are NOT highlighted in
    any special way."""

    today = date.today()
    oneweek = date.today() + timedelta(days=7)

    with app.test_request_context("/", method="GET"):
        # this is similar to the render_template call in the dashboard endpoint
        items = [FridgeItem(1, "nextweek", 0, today, oneweek, 0)]
        templ = render_template("dashboard.html", form=ItemForm(), \
                               current_items=items)

    # parse the whole rendered template
    parsed = BeautifulSoup(templ, features="html.parser")

    # get all rows in the tbody
    table_rows = parsed.table.tbody.find_all('tr')

    # we added just 1 item; should be one row
    assert len(table_rows) == 1

    # should be no class styles applied
    assert table_rows[0]["class"] == []

def test_dashboard_highlight_expired(app):
    """Make sure items with 0 or fewer days til expiry are highlighted
    as expired"""

    today = date.today()
    yesterday = date.today() + timedelta(days=-1)

    with app.test_request_context("/", method="GET"):
        # this is similar to the render_template call in the dashboard endpoint
        items = [FridgeItem(1, "today", 0, today, today, 0),
                 FridgeItem(1, "yesterday", 0, today, yesterday, 0)]
        templ = render_template("dashboard.html", form=ItemForm(), \
                               current_items=items)

    # parse the whole rendered template
    parsed = BeautifulSoup(templ, features="html.parser")

    # get all rows in the tbody
    table_rows = parsed.table.tbody.find_all('tr')

    # we added just 2 items; should be 2 rows
    assert len(table_rows) == 2

    # should have 'expired' class style applied
    assert table_rows[0]["class"] == ['expired']
    assert table_rows[1]["class"] == ['expired']


def test_dashboard_no_expiry_render(app):
    """Make sure items with no expiry date render properly and have no
    highlighting."""

    today = date.today()

    with app.test_request_context("/", method="GET"):
        # this is similar to the render_template call in the dashboard endpoint
        items = [FridgeItem(1, "indefinite", 0, today, None, 0)]
        templ = render_template("dashboard.html", form=ItemForm(), \
                               current_items=items)

    # parse the whole rendered template
    parsed = BeautifulSoup(templ, features="html.parser")

    # get all rows in the tbody
    table_rows = parsed.table.tbody.find_all('tr')

    # we added just 1 items; should be 1 row
    assert len(table_rows) == 1

    # should be no class styles applied
    assert table_rows[0]["class"] == []

    cols = [td for td in table_rows[0] if td != '\n']
    assert cols[3].text == 'N/A'

def test_dashboard_h1_title(app):
    """Tests that the dashboard template has an h1 tag with 'What's in my fridge'."""

    with app.test_request_context("/", method="GET"):
        # Render the template with any necessary data. 
        # Here, an empty list is passed for current_items as it's not relevant to this test.
        templ = render_template("dashboard.html", form=ItemForm(), current_items=[])

    # Parse the rendered template
    parsed = BeautifulSoup(templ, features="html.parser")

    # Find the h1 tag
    h1_tag = parsed.find('h1')

    # Check if the h1 tag exists and has the correct text
    assert h1_tag is not None, "h1 tag not found in the template"
    assert h1_tag.text.strip() == "What's in my fridge", "h1 tag does not have the correct text"

def test_dashboard_table_headers(app):
    """Tests that the dashboard table headers are correctly abbreviated."""

    with app.test_request_context("/", method="GET"):
        # Provide a mock item to ensure headers are rendered
        mock_items = [FridgeItem(1, "MockItem", 1, date.today(), date.today())]
        templ = render_template("dashboard.html", form=ItemForm(), current_items=mock_items)

    # Parse the rendered template
    parsed = BeautifulSoup(templ, features="html.parser")

    # Find the table headers within the thead element
    headers = [th.text.strip() for th in parsed.thead.find_all('th')]

    # Define the expected headers
    expected_headers = ["Name", "Qty", "Added", "Expires", "Edit", "Delete", "Archived"]

    # Check if the headers in the template match the expected headers
    assert headers == expected_headers, f"Headers do not match. Found: {headers}"
