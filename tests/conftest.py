# adapted from the Flask Tutorial app flaskr

import os
import tempfile

import pytest
from wimf import create_app
from wimf.db import get_db, init_db

# for later - open test db population script
# with open(os.path.join(os.path.dirname(__file__), 'add_test_data.sql'), 'rb') as f:
#     _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        # uncomment when we actually use a temp db
        # 'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        # uncomment when test data sql script done
        # get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
