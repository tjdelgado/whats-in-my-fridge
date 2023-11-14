"""File containing classes for representing the various data encountered in the
database tables and elsewhere.

Classes:
FridgeItem: represents members of the items table in the db
TODO: StoredItem: represents members of items stored for future reference;
      corresponds to the stored_items[??] table in the DB
TODO: Recipe: represents members of the recipe table in the DB"""

from datetime import date, timedelta

class FridgeItem:
    """Class for representing members of the items table in the DB.
    Attributes:
    name: name of the item
    expiry_time: the average shelf-life of the item
    date_added: the date the item was added to the fridge. if not specified,
                defaults to the current date at time of adding
    expiry_date: the date the item expires. If not specified, defaults to
                 date of adding + expire_time days

    Methods:
    update_expiry(self, new_date): sets expiry_date to new_date
    days_to_expiry(self): returns days to expiry as an int"""
    def __init__(self, name, expiry_time: int, date_added=None, expiry_date=None):
         self.name = name
         today = date.today()
         if expiry_time < 0:
             self.expiry_time = -1
         else:
             self.expiry_time = expiry_time
         if date_added is None:
             self.date_added = today
         else:
             self.date_added = date.fromisoformat(date_added.strip())
         if expiry_date is None:
             self.expiry_date = date_added + timedelta(days=expiry_time)
         else:
             self.expiry_date = date.fromisoformat(expiry_date.strip())
    def __str__(self):
        return f"name: {self.name}, expiry_time: {self.expiry_time}, date_added: \
               {self.date_added}, expiry_date: {self.expiry_date}"
    def update_expiry(self, new_date: date):
        """Updates expiry_date to new_date.
        TODO: add sanity checking - can't set date in the past? do we care?"""
        self.expiry_date = new_date
    def days_to_expiry(self) -> int:
        """Returns number of days between expiry date and present date."""
        return (self.expiry_date - date.today()).days
