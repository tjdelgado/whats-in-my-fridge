import pytest

from pytest_mock import MockerFixture
from pytest_mock import PytestMockWarning
from unittest.mock import MagicMock, call, Mock

from datetime import date

from wimf.views import *
import wimf.db

def test_delete_tag(mocker): # mocker = mocking fixture from pytest-mock
    # mock the db connection return val
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)

    test_tag_id = 1

    # make sure the call worked as expected
    assert delete_tag_query(test_tag_id) == True

    # make sure the mocked db handle had the right methods called on it
    db_mock.cursor.assert_called_once()
    db_mock.cursor().execute.assert_called_once_with("DELETE FROM tags WHERE id = ?", (test_tag_id,))
    db_mock.commit.assert_called_once()

def test_delete_item(mocker): # same as above basically
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)
    test_item_id = 1

    assert delete_item_query(test_item_id) == True

    print(db_mock.method_calls)
    print(db_mock.mock_calls)

    db_mock.cursor.assert_called_once()
    db_mock.cursor().execute.assert_called_once_with("DELETE FROM ITEMS WHERE id = ?", (test_item_id,))
    db_mock.commit.assert_called_once()

def test_retrieve_current_tags(mocker):
    # mock the db
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)

    # set return value of chained calls to the db handle
    ret_mock = Mock()
    mock_results = db_mock.execute.return_value
    mock_results.fetchall.return_value = ret_mock

    # call the fxn to test
    query = "SELECT * FROM tags INNER JOIN item_tags ON tags.id = item_tags.tag_id"
    result = retrieve_current_tags()

    # do we get the mocked return value out?
    assert result == ret_mock

    # did we get the right calls to the mocked db connection?
    calls = call.execute(query).fetchall()
    assert db_mock.mock_calls == calls.call_list()

def test_retrieve_all_tags(mocker):
    # mock the db
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)

    # set return value of chained calls to the db handle
    ret_mock = Mock()
    mock_results = db_mock.execute.return_value
    mock_results.fetchall.return_value = ret_mock

    # call the fxn to test
    query = "SELECT * FROM tags;"
    result = retrieve_all_tags()

    # do we get the mocked return value out?
    assert result == ret_mock

    # did we get the right calls to the mocked db connection?
    calls = call.execute(query).fetchall()
    assert db_mock.mock_calls == calls.call_list()

def test_add_new_tag(mocker):
    # mock the db connection return val
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)

    test_tag_name = "testtag"

    # make sure the call worked as expected
    assert add_new_tag(test_tag_name) == True

    # make sure the mocked db handle had the right methods called on it
    query = "INSERT INTO tags ( name ) VALUES (?)"
    db_mock.execute.assert_called_once_with(query, (test_tag_name,))
    db_mock.commit.assert_called_once()

def test_add_tags_jct_tbl(mocker):
    # mock the db connection return val
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)

    test_tag_item_id = Mock()
    test_tag_list = MagicMock()
    test_tag_list.__iter__.return_value = ["a", "b", "c"]

    # make sure the call worked as expected
    assert addTagsToJunctionTable(test_tag_item_id, test_tag_list) == 0

    # make sure the mocked db handle had the right methods called on it
    # check that 3 inserts happened
    query = "INSERT INTO item_tags (item_id, tag_id) VALUES (?, ?)"
    expected_exec_calls = [call(query, (test_tag_item_id, "a",)),
                           call(query, (test_tag_item_id, "b",)),
                           call(query, (test_tag_item_id, "c",)),]

    clist = db_mock.cursor().execute.call_args_list
    assert clist == expected_exec_calls

    # check that 3 commits happened
    expected_comm_calls = [call(), call(), call()]
    assert db_mock.commit.call_args_list == expected_comm_calls

def test_update_tag(mocker):
    # mock the db connection return val
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)

    test_tag_name = "test"
    test_tag_id = 1

    # make sure the call worked as expected
    assert update_tag(test_tag_id, test_tag_name) == True

    # make sure the mocked db handle had the right methods called on it
    query = "UPDATE tags SET name = ? WHERE id = ?"
    db_mock.cursor().execute.assert_called_once_with(query, \
                                                    (test_tag_name, test_tag_id,))
    db_mock.commit.assert_called_once()

def test_get_tag(mocker):
    # mock the db
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)

    # set return value of chained calls to the db handle
    ret_mock = Mock()
    mock_results = db_mock.cursor().execute.return_value
    mock_results.fetchone.return_value = ret_mock

    test_id = Mock()

    # call the fxn to test
    result = get_tag(test_id)

    # do we get the mocked return value out?
    assert result == ret_mock

    # did we get the right calls to the mocked db connection?
    # TODO: fix the below later
    query = "SELECT * FROM tags WHERE id = ?"
    db_mock.cursor().execute.assert_called_once_with(query, \
                                                    (test_id,))

def test_get_archived_items(mocker):
    # mock the db
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)

    # set return value of chained calls to the db handle
    ret_mock = Mock()
    mock_results = db_mock.execute.return_value
    mock_results.fetchall.return_value = ret_mock

    # call the fxn to test
    query = "SELECT * FROM ITEMS WHERE archived = 1"
    result = get_archived_items()

    # do we get the mocked return value out?
    assert result == ret_mock

    # did we get the right calls to the mocked db connection?
    calls = call.execute(query).fetchall()
    assert db_mock.mock_calls == calls.call_list()

def test_change_archived_status(mocker):
    # mock the db connection return val
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)

    test_status = Mock()
    test_item_id = Mock()

    # make sure the call worked as expected
    assert change_archived_status(test_item_id, test_status) == True

    # make sure the mocked db handle had the right methods called on it
    query = "UPDATE ITEMS SET archived = ? WHERE id = ?"
    db_mock.cursor().execute.assert_called_once_with(query, \
                                                    (test_status, test_item_id))
    db_mock.commit.assert_called_once()

def test_retrieve_item(mocker):
    # mock the db
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)

    # set return value of chained calls to the db handle
    ret_mock = Mock()
    mock_results = db_mock.execute.return_value
    mock_results.fetchone.return_value = ret_mock

    test_id = Mock()

    # call the fxn to test
    result = retrieve_item(test_id)

    # do we get the mocked return value out?
    assert result == ret_mock

    # did we get the right calls to the mocked db connection?
    # TODO: fix the below later
    query = "SELECT * FROM ITEMS WHERE id = ?"
    db_mock.execute.assert_called_once_with(query, (test_id,))

def test_update_item(mocker):
    # mock the db connection return val
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)

    test_form = MagicMock()
    test_form.name.data = MagicMock()
    test_form.quantity.data = MagicMock()
    test_form.dayAdded.data = MagicMock()
    test_form.expiryDay.data = MagicMock()

    newName = test_form.name.data
    newQuantity = test_form.quantity.data
    newDateAdded = test_form.dayAdded.data
    newExpiryDate = test_form.expiryDay.data

    test_item_id = Mock()

    # make sure the call worked as expected
    assert update_item(test_form, test_item_id) == True

    # make sure the mocked db handle had the right methods called on it
    query = "UPDATE ITEMS SET name = ?, quantity = ?, date_added = ?, expiry_date = ? WHERE id = ?"
    query_params = (newName, newQuantity, newDateAdded, newExpiryDate, test_item_id)

    db_mock.cursor().execute.assert_called_with(query, query_params)
    db_mock.commit.assert_called_once()


def test_populate_edit_form(mocker):
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)
    mocker.patch('wimf.helpers.db_convert_isodate', return_value = '2023-12-31')

    # gotta mock dict-addressable result row
    test_item = MagicMock()
    mock_item_data = {"name": Mock(),
                      "quantity": Mock(),
                      "date_added": Mock(),
                      "expiry_date": Mock()}
    def get_item_field(key):
        return mock_item_data[key]
    test_item.__getitem__.side_effect = get_item_field

    test_tags = []

    test_form = MagicMock()

    assert populate_edit_form(test_form, test_item, test_tags) == True

    assert test_form.name.data == mock_item_data["name"]
    assert test_form.quantity.data == mock_item_data["quantity"]
    assert test_form.dayAdded.data == '2023-12-31'
    assert test_form.expiryDay.data == '2023-12-31'

def test_get_current_items(mocker):
    # mock the db
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)

    # set return value of chained calls to the db handle
    ret_mock = Mock()
    mock_results = db_mock.execute.return_value
    mock_results.fetchall.return_value = ret_mock

    # call the fxn to test
    t_sort = "name"
    t_direction = "asc"
    query = f"SELECT * FROM ITEMS WHERE archived = 0 ORDER BY {t_sort} {t_direction}"
    result = get_current_items(t_sort, t_direction)

    # do we get the mocked return value out?
    assert result == ret_mock

    # did we get the right calls to the mocked db connection?
    calls = call.execute(query).fetchall()
    assert db_mock.mock_calls == calls.call_list()

def test_get_current_items_invalid_col(mocker):
    # test behavior if invalid column name passed in url

    # mock the db
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)

    # set return value of chained calls to the db handle
    ret_mock = Mock()
    mock_results = db_mock.execute.return_value
    mock_results.fetchall.return_value = ret_mock

    # call the fxn to test
    t_sort = "this is not a column"
    t_direction = "asc"

    expected_query = f"SELECT * FROM ITEMS WHERE archived = 0 ORDER BY expiry_time {t_direction}"
    result = get_current_items(t_sort, t_direction)

    # do we get the mocked return value out?
    assert result == ret_mock

    # did we get the right calls to the mocked db connection?
    calls = call.execute(expected_query).fetchall()
    assert db_mock.mock_calls == calls.call_list()

def test_get_current_items_invalid_sort(mocker):
    # test behavior if invalid sort dir passed in url

    # mock the db
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)

    # set return value of chained calls to the db handle
    ret_mock = Mock()
    mock_results = db_mock.execute.return_value
    mock_results.fetchall.return_value = ret_mock

    # call the fxn to test
    t_sort = "expiry_time"
    t_direction = "this is not a sort"

    expected_query = f"SELECT * FROM ITEMS WHERE archived = 0 ORDER BY {t_sort} "
    result = get_current_items(t_sort, t_direction)

    # do we get the mocked return value out?
    assert result == ret_mock

    # did we get the right calls to the mocked db connection?
    calls = call.execute(expected_query).fetchall()
    assert db_mock.mock_calls == calls.call_list()

def test_get_current_items_invalid_col_and_sort(mocker):
    # test behavior if invalid column name and sort dir passed in url

    # mock the db
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)

    # set return value of chained calls to the db handle
    ret_mock = Mock()
    mock_results = db_mock.execute.return_value
    mock_results.fetchall.return_value = ret_mock

    # call the fxn to test
    t_sort = "this is not a column"
    t_direction = "this is not a sort"

    expected_query = f"SELECT * FROM ITEMS WHERE archived = 0 ORDER BY expiry_time "
    result = get_current_items(t_sort, t_direction)

    # do we get the mocked return value out?
    assert result == ret_mock

    # did we get the right calls to the mocked db connection?
    calls = call.execute(expected_query).fetchall()
    assert db_mock.mock_calls == calls.call_list()


def test_add_new_item(mocker):
    # mock methods that need mocking
    db_mock = MagicMock()
    jct_table_fxn_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)
    mocker.patch('wimf.helpers.addTagsToJunctionTable',
                 jct_table_fxn_mock)

    # data for populating itemForm and for query
    test_today = date.today()
    test_name = "name"
    test_qty = 1
    test_tags = []
    test_expiry_time = 0
    test_is_archived = 0

    # populate the mocked ItemForm
    test_form = MagicMock()
    test_form.name.data = test_name
    test_form.quantity.data = test_qty
    test_form.dayAdded.data = test_today
    test_form.expiryDay.data = test_today
    test_form.tags.data = test_tags

    assert add_new_item(test_form) == True

    query = "INSERT INTO ITEMS (name, quantity, expiry_time, date_added, expiry_date, archived) VALUES (?, ?, ?, ?, ?, ?) RETURNING id"
    params = (test_name, test_qty, test_expiry_time, test_today, test_today,\
              test_is_archived)

    db_mock.cursor().execute.assert_called_once_with(query, params)
    db_mock.commit.assert_called_once()
    jct_table_fxn_mock.assert_called_once_with(db_mock.cursor().lastrowid,
                                               test_tags)

def test_expiry_status(mocker):
    assert expiry_status(None) == ''
    assert expiry_status(0) == 'expired'
    assert expiry_status(-1) == 'expired'
    assert expiry_status(1) == 'expiring-soon'
    assert expiry_status(3) == 'expiring-soon'
    assert expiry_status(4) == ''
