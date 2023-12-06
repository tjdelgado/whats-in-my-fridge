# adapted from the flaskr Flask tutorial app

import sqlite3

import click
from flask import current_app, g

CUR_SCHEMA_VER = 1

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """(re-)Initializes the database from scratch. Will drop all existing tables and triggers in db."""
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def migrate_db():
    db = get_db()
    c = db.cursor()

    # check schema version
    try:
        schemaquery = """PRAGMA user_version;"""
        squery_res = c.execute(schemaquery).fetchall()
    except sqlite3.OperationalError:
        print("Couldn't find user_version variable in the table. Probably due to a malformed, damaged, or uninitialized database. Consider initializing the database instead.")
        raise

    schemaver = int(squery_res[0][0])
    if schemaver < CUR_SCHEMA_VER:
        # need to update!
        print("migrating!")
        with current_app.open_resource('migrate.sql') as f:
            db.executescript(f.read().decode('utf8'))

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(migrate_db_command)

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('migrate-db')
def migrate_db_command():
    """Try and migrate the db to a new version."""
    migrate_db()
    click.echo('Migrated the database.')
