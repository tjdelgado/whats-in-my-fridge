"""Helper functions for the main body of the app --- things like date parsing and the like."""

from datetime import date

def db_convert_isodate(s: str) -> date:

    """Meant for converting dates from date columns in the db to
    python date.datetime objects. Made because SQLite seems to have
    some quirks in how it outputs TEXT columns storing iso-formatted
    dates.

    Attempts to convert a isoformat date string (ideally
    YYYY-MM-DD) to a datetime.date object. Does some simple
    sanitization of the input.

    In case the db spits out NULL (python None) then spit out a None too.
    Returns None if a ValueError/TypeError occurred.
    """

    ret = None

    if s is None: # if row field is a SQL NULL/python None
        return ret

    try:
        ret = date.fromisoformat(s.strip())
    except (ValueError, TypeError) as e:
        # e.g. if malformed or non-string input
        pass # and return none
    except Exception as e:
        # something weird happened, complain and pass exception throughq
        print(f"Unexpected {e=}, {type(e)=}")
        raise
    finally:
        return ret
