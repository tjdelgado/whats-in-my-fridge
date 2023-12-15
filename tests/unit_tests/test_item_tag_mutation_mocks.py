import pytest

from pytest_mock import MockerFixture
from pytest_mock import PytestMockWarning
from unittest.mock import MagicMock, call, Mock

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
    #query = "SELECT * FROM tags WHERE id = ?"
    #calls = call.cursor().execute(query, (test_id,)).fetchone()
    #assert db_mock.mock_calls == calls.call_list()
