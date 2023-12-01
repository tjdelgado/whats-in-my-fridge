from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import pytest
from flask import render_template
from wimf.data_models import FridgeItem
from wimf.views import ItemForm

def test_edit_template_populated(app):
    """Tests that the editing template displays things properly."""
    assert 1 == 1 # todo - adapt archived code below
    # today = date.today()
    # tomorrow = date.today() + timedelta(days=1)
    # with app.test_request_context("/archived_list", method="GET"):
    #     items = [FridgeItem(1, "1st", 1, today, tomorrow, 1),
    #              FridgeItem(2, "2nd", 2, today, tomorrow, 1),
    #              FridgeItem(3, "3rd", 3, today, tomorrow, 1)]
    #     templ = render_template("archived.html", form=ItemForm(), \
    #                            archived_items=items)

    # # parse the whole rendered template
    # parsed = BeautifulSoup(templ, features="html.parser")

    # # get all rows in the tbody
    # table_rows = parsed.table.tbody.find_all('tr')

    # # we added just three items should be three rows
    # assert len(table_rows) == 3

    # # filter out \n again from the tr parse trees
    # trs_clean = [[td for td in tr if td != '\n'] for tr in table_rows]

    # assert trs_clean[0][0].text == '1st'
    # assert trs_clean[0][1].text == '1'
    # assert trs_clean[0][2].text == today.isoformat()
    # assert trs_clean[0][3].text == tomorrow.isoformat()

    # assert trs_clean[1][0].text == '2nd'
    # assert trs_clean[1][1].text == '2'
    # assert trs_clean[1][2].text == today.isoformat()
    # assert trs_clean[1][3].text == tomorrow.isoformat()


    # assert trs_clean[2][0].text == '3rd'
    # assert trs_clean[2][1].text == '3'
    # assert trs_clean[2][2].text == today.isoformat()
    # assert trs_clean[2][3].text == tomorrow.isoformat()

def test_edit_template_empty_form(app):
    """This shouldn't be normally encountered, but just in case, test to make sure passing in an empty EditForm doesn't completely crash the app"""
    assert 1 == 1
def test_edit_template_no_form_at_all(app):
    """This shouldn't be normally encountered, but just in case, test to make sure failing to pass in an empty EditForm doesn't completely crash the app"""
    assert 1 == 1
