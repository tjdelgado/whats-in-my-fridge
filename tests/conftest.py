# file for pytest to allow functional/integration tests of endpoints
# adapted from flask tutorial code

import os
import tempfile

import pytest
from wimf import create_app, views
from wimf.db import get_db, init_db



# for later - open test db population script
# with open(os.path.join(os.path.dirname(__file__), 'add_test_data.sql'), 'rb') as f:
#     _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SERVER_NAME': 'testhost:5000',
        # uncomment after I'm done with behave
        'DATABASE': db_path,
        'WTF_CSRF_ENABLED': False
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
