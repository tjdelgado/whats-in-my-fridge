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
    def __init__(self, item_id, name, quantity, date_added, expiry_date, archived):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.date_added = date_added
        self.expiry_date = expiry_date
        self.archived = archived
        
    def __str__(self):
        return f"id: {self.item_id}, name: {self.name}, quantity: {self.quantity}, date_added: {self.date_added}, expiry_date: {self.expiry_date}"

    def update_expiry(self, new_date):
        self.expiry_date = new_date

    def days_to_expiry(self):
        if self.expiry_date is None:
            return None
        else:
            return (self.expiry_date - date.today()).days