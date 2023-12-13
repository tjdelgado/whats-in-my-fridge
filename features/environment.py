import os
import tempfile
from wimf import create_app, views
from wimf.db import get_db, init_db




def before_feature(context, feature):
    context.db_fd, context.db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SERVER_NAME': 'testhost:5000',
        # uncomment when we actually use a temp db
        'DATABASE': context.db_path,
        'WTF_CSRF_ENABLED': False,

    })

    with app.app_context():
        init_db()

    context.app = app
    context.client = app.test_client()


def after_feature(context, feature):
    os.close(context.db_fd)
    os.unlink(context.db_path)
