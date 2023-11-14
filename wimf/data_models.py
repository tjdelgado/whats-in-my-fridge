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
    expire_time: the average shelf-life of the item
    date_added: the date the item was added to the fridge. if not specified,
                defaults to the current date at time of adding
    expiry_date: the date the item expires. If not specified, defaults to
                 date of adding + expire_time days

    Methods:
    update_expiry(self, new_date): sets expiry_date to new_date"""
    def __init__(self, name, expire_time, date_added=None, expiry_date=None):
         self.name = name
         self.expire_time = expire_time
         if date_added is None:
             self.date_added = date.today()
         else:
             self.date_added = date_added
         if expiry_date is None:
             self.expiry_date = date.today() + timedelta(days=expire_time)
         else:
             self.expiry_date = None
     def update_expiry(self, new_date):
          self.expiry_date = new_date
