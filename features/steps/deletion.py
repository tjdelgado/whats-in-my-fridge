from behave import given, when, then
from bs4 import BeautifulSoup

@given('that "{item}" is on the dashboard')
def step_impl(context, item):
    # items are some of the default items in the schema
    html = context.client.get('/').data

    # parse the whole rendered template
    parsed = BeautifulSoup(html, features="html.parser")

    # get all rows in the tbody
    table_rows = parsed.find_all('tr')

    found_item = False

    for r in table_rows:
        cols = [td for td in r if td != '\n']
        for c in cols:
            if c.text == item:
                found_item = True
            else: pass

    assert found_item


@when('I delete the "{item}" from the dashboard')
def step_impl(context, item):
    # hardcoding to avoid clicking on the item / don't have easy item id lookup from web interface...
    if item == 'milk':
        context.client.post('/2/delete_item')
    elif item == 'rotten eggs':
        context.client.post('/1/delete_item')
    else:
        pass
    assert True

@then('"{item}" will no longer appear in the dashboard')
def step_impl(context, item):

    # items are some of the default items in the schema
    html = context.client.get('/').data

    # parse the whole rendered template
    parsed = BeautifulSoup(html, features="html.parser")

    # get all rows in the tbody
    table_rows = parsed.find_all('tr')

    found_item = False

    for r in table_rows:
        cols = [td for td in r if td != '\n']
        for c in cols:
            if c.text == item:
                found_item = True
            else: pass

    assert not found_item
