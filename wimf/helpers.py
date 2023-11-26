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
    if s is None:
        return None
    try:
        return date.fromisoformat(s.strip())
    except (ValueError, TypeError):
        pass
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        raise

def format_quantity(quantity: int) -> str:
    return f"{quantity} pcs"
