from behave import given, when, then
from bs4 import BeautifulSoup

@given('we have an item X on the dashboard')
def step_impl(context):
    # item is the default 'milk' item in the schema
    html = context.client.get('/').data

    # parse the whole rendered template
    parsed = BeautifulSoup(html, features="html.parser")

    # get all rows in the tbody
    table_rows = parsed.find_all('tr')

    found_milk = False

    for r in table_rows:
        cols = [td for td in r if td != '\n']
        for c in cols:
            if c.text == 'milk':
                found_milk = True
            else: pass

    assert found_milk is True


@when('we call the delete endpoint on item X')
def step_impl(context):
    context.client.post('/2/delete_item')
    assert True

@then('item X no longer appears in the dashboard')
def step_impl(context):

    html = context.client.get('/').data

    # parse the whole rendered template
    parsed = BeautifulSoup(html, features="html.parser")

    # get all rows in the tbody
    table_rows = parsed.find_all('tr')

    found_milk = False

    for r in table_rows:
        cols = [td for td in r if td != '\n']
        for c in cols:
            if c.text == 'milk':
                found_milk = True
            else: pass

    assert found_milk is False
