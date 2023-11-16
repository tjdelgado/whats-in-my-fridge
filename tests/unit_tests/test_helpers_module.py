import pytest
from wimf.helpers import db_convert_isodate
from datetime import date, timedelta

def test_db_convert_isodate_happy():
    """tests happy paths of a function meant to convert the output of
    columns in the DB containing dates in YYYY-MM-DD to python
    datetime.date objects.

    Namely, when the date is None, and when the datestr is indeed
    well-formed in YYYY-MM-DD format
    """

    # well formatted str
    assert db_convert_isodate('2023-12-12') == date.fromisoformat('2023-12-12')

    # None as input
    assert db_convert_isodate(None) == None

    # wellformed string with whitespace
    assert db_convert_isodate(' 2023-12-12 ') == date.fromisoformat('2023-12-12')

def test_db_convert_isodate_failures():
    """tests not-happy paths of a function meant to convert the output of
    columns in the DB containing dates in YYYY-MM-DD to python
    datetime.date objects.

    Namely, when the datestr is *neither* None, *nor* in YYYY-MM-DD
    format.
    """

    # malformed datestr
    assert db_convert_isodate('20223-12-12') == None

    # test behavior with a not-string
    assert db_convert_isodate(4) == None
