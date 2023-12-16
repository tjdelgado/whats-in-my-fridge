from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import pytest
from flask import render_template
from wimf.data_models import FridgeItem
from wimf.views import ItemForm

def test_edit_template_populated(app):
    """Tests that the editing template displays things properly."""
    assert 1 == 1 # todo - adapt archived code below
    today = date.today()
    tomorrow = date.today() + timedelta(days=1)


    with app.test_request_context("/1/edit", method="GET"):
        testform = ItemForm()

        # set fields in form
        testform.name.data = "test"
        testform.quantity.data = 89
        testform.dayAdded.data  = today
        testform.expiryDay.data = tomorrow

        templ = render_template("edit_item.html", editForm=testform)

    # parse the whole rendered template
    parsed = BeautifulSoup(templ, features="html.parser")

    # get all rows in the tbody
    form_entries = parsed.form.find_all('div')

    # we added just three items should be three rows
    assert len(form_entries) == 5

    # filter out \n again from the tr parse trees
    divs_clean = [[div for div in entry if div != '\n'] for entry in form_entries]
    assert divs_clean[0][1]['value'] == 'test'
    assert divs_clean[1][1]['value'] == '89'
    assert divs_clean[2][1]['value'] == today.isoformat()
    assert divs_clean[3][1]['value'] == tomorrow.isoformat()


def test_edit_template_badvalues(app):
    """Try and pass in Nones to the form and make sure it doesn't blow up."""
    today = date.today()
    tomorrow = date.today() + timedelta(days=1)


    with app.test_request_context("/1/edit", method="GET"):
        testform = ItemForm()

        # set fields in form
        # 70 chars to exceed limit
        testform.name.data = None
        testform.quantity.data = None
        testform.dayAdded.data  = None
        testform.expiryDay.data = None

        templ = render_template("edit_item.html", editForm=testform)

    # parse the whole rendered template
    parsed = BeautifulSoup(templ, features="html.parser")

    # get all rows in the tbody
    form_entries = parsed.form.find_all('div')

    # we added just three items should be three rows
    assert len(form_entries) == 5

    # filter out \n again from the tr parse trees
    divs_clean = [[div for div in entry if div != '\n'] for entry in form_entries]
    assert divs_clean[0][1]['value'] == '' # hopefully it made it blank instead of the absurd string
    assert divs_clean[1][1]['value'] == '' # hopefully it's the default valt
    assert divs_clean[2][1]['value'] == ''
    assert divs_clean[3][1]['value'] == ''

def test_edit_template_blank_form(app):
    """Make sure a blank form does indeed render with no data in the fields."""

    today = date.today()
    tomorrow = date.today() + timedelta(days=1)

    with app.test_request_context("/1/edit", method="GET"):
        testform = ItemForm() # blank form

        templ = render_template("edit_item.html", editForm=testform)

    # parse the whole rendered template
    parsed = BeautifulSoup(templ, features="html.parser")

    # get all rows in the tbody
    form_entries = parsed.form.find_all('div')

    # we added just three items should be three rows
    assert len(form_entries) == 5

    # filter out \n again from the tr parse trees
    divs_clean = [[div for div in entry if div != '\n'] for entry in form_entries]
    assert divs_clean[0][1]['value'] == ''
    assert divs_clean[1][1]['value'] == '1' # 1 is default quantity
    assert divs_clean[2][1]['value'] == today.isoformat()
    assert divs_clean[3][1]['value'] == today.isoformat() # today is default
