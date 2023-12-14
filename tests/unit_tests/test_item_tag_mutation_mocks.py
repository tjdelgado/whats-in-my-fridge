import pytest

from pytest_mock import MockerFixture
from pytest_mock import PytestMockWarning
from unittest.mock import MagicMock, call

from wimf.views import *
import wimf.db

def test_delete_tag(mocker): # mocker = mocking fixture from pytest-mock
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)
    test_tag_id = 1

    assert delete_tag_query(test_tag_id) == True

    print(db_mock.method_calls)
    print(db_mock.mock_calls)

    db_mock.cursor.assert_called_once()
    db_mock.cursor().execute.assert_called_once_with("DELETE FROM tags WHERE id = ?", (test_tag_id,))
    db_mock.commit.assert_called_once()

def test_delete_item(mocker): # mocker = mocking fixture from pytest-mock
    db_mock = MagicMock()
    mocker.patch('wimf.db.get_db', return_value = db_mock)
    test_item_id = 1

    assert delete_item_query(test_item_id) == True

    print(db_mock.method_calls)
    print(db_mock.mock_calls)

    db_mock.cursor.assert_called_once()
    db_mock.cursor().execute.assert_called_once_with("DELETE FROM ITEMS WHERE id = ?", (test_item_id,))
    db_mock.commit.assert_called_once()
