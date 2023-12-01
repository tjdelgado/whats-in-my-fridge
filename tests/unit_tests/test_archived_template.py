from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import pytest
from flask import render_template
from wimf.data_models import FridgeItem
from wimf.views import ItemForm

def test_archive_template_view_empty(app):
    """Tests that the archive template appropriately says there's
    nothing in the fridge when current_items is empty."""

    with app.test_request_context("/archived_list", method="GET"):
        items = []
        templ = render_template("archived.html", form=ItemForm(), \
                               archived_items=items)

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

    assert p_elts[0].text == 'Nothing in the archive!'

def test_archive_template_view(app):
    """Tests that the archive template displays things properly."""

    today = date.today()
    tomorrow = date.today() + timedelta(days=1)
    with app.test_request_context("/archived_list", method="GET"):
        items = [FridgeItem(1, "1st", 1, today, tomorrow, 1),
                 FridgeItem(2, "2nd", 2, today, tomorrow, 1),
                 FridgeItem(3, "3rd", 3, today, tomorrow, 1)]
        templ = render_template("archived.html", form=ItemForm(), \
                               archived_items=items)

    # parse the whole rendered template
    parsed = BeautifulSoup(templ, features="html.parser")

    # get all rows in the tbody
    table_rows = parsed.table.tbody.find_all('tr')

    # we added just three items should be three rows
    assert len(table_rows) == 3

    # filter out \n again from the tr parse trees
    trs_clean = [[td for td in tr if td != '\n'] for tr in table_rows]

    assert trs_clean[0][0].text == '1st'
    assert trs_clean[0][1].text == '1'
    assert trs_clean[0][2].text == today.isoformat()
    assert trs_clean[0][3].text == tomorrow.isoformat()

    assert trs_clean[1][0].text == '2nd'
    assert trs_clean[1][1].text == '2'
    assert trs_clean[1][2].text == today.isoformat()
    assert trs_clean[1][3].text == tomorrow.isoformat()


    assert trs_clean[2][0].text == '3rd'
    assert trs_clean[2][1].text == '3'
    assert trs_clean[2][2].text == today.isoformat()
    assert trs_clean[2][3].text == tomorrow.isoformat()
