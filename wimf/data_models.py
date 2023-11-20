"""File containing classes for representing the various data encountered in the
database tables and elsewhere.

Classes:
FridgeItem: represents members of the items table in the db
TODO: StoredItem: represents members of items stored for future reference;
      corresponds to the stored_items[??] table in the DB
TODO: Recipe: represents members of the recipe table in the DB"""

from datetime import date, timedelta, datetime

class FridgeItem:
    """Class for representing members of the items table in the DB.
    Attributes:

    name: name of the item

    expiry_time: Integer. the average shelf-life of the item. Set to None if
                 indefinite expiry. (A None value also sets expiry_date to None.)

    date_added: datetime.date. the date the item was added to the fridge. if not
                specified, defaults to the current date at time of
                adding

    expiry_date: datetime.date. the date the item expires. If not
                 specified in constructor, defaults to date of adding
                 + expire_time days. If expiry_time is None, then
                 value defaults to None, signifying "no expiry"

                 NOTE THAT A SPECIFIED EXPIRY_DATE OVERRIDES THE EXPIRY DATE
                 CALCULATED USING EXPIRY_TIME, UNLESS EXPIRY_TIME IS NONE.

                 In the latter case, expiry_date is always None.

    Methods:
    update_expiry(self, new_date): sets expiry_date to new_date

    days_to_expiry(self): returns days to expiry as an int. If
    expiry_date is None, returns None.

    """
    def __init__(self, item_id, name, expiry_time: int, date_added: date=None, expiry_date: date=None):

        self.item_id = item_id
        self.name = name
        self.expiry_time = expiry_time
        print(date_added)
        if date_added is None:
            self.date_added = date.today()
        else:
            self.date_added = date_added
        if expiry_time is not None:
            if expiry_date is None:
                self.expiry_date = self.date_added + timedelta(days=expiry_time)
            else:
                self.expiry_date = expiry_date
        else:
            # self.expiry_date = None
            d1 = datetime.strptime(expiry_date, "%Y-%m-%d")
            d2 = datetime.strptime(date_added, "%Y-%m-%d")
            self.expiry_time = (d1 - d2).days 
            self.expiry_date = expiry_date

    def __str__(self):
        return f"id: {self.item_id}, name: {self.name}, expiry_time: {self.expiry_time}, date_added: {self.date_added}, expiry_date: {self.expiry_date}"

    def update_expiry(self, new_date: date):
        """Updates expiry_date to new_date.
        TODO: add sanity checking - can't set date in the past? do we care?"""
        self.expiry_date = new_date

    def days_to_expiry(self) -> int:
        """Returns number of days between expiry date and present date."""
        if self.expiry_date is None:
            return None
        else:
            return (self.expiry_date - date.today()).days
