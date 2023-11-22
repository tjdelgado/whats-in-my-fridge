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

    item_id: Unique identifier for the item.

    name: Name of the item.

    expiry_time: Integer. The average shelf-life of the item. Set to None if
                 indefinite expiry. (A None value also sets expiry_date to None.)

    date_added: datetime.date. The date the item was added to the fridge. If not
                specified, defaults to the current date at the time of adding.

    expiry_date: datetime.date. The date the item expires. If not specified in 
                 constructor, defaults to date of adding + expire_time days. If 
                 expiry_time is None, then value defaults to None, signifying 
                 "no expiry".

    quantity: Integer. The quantity of the item in the fridge.

    Methods:
    update_expiry(self, new_date): Sets expiry_date to new_date.

    days_to_expiry(self): Returns days to expiry as an int. If expiry_date is 
                          None, returns None.

    """
    def __init__(self, item_id, name, expiry_time: int, date_added: date=None, expiry_date: date=None, quantity: int=1):
        self.item_id = item_id
        self.name = name
        self.expiry_time = expiry_time
        self.quantity = quantity  # New attribute for quantity

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
            if expiry_date is not None:
                self.expiry_date = expiry_date
                self.expiry_time = (expiry_date - self.date_added).days
            else:
                self.expiry_date = None

    def __str__(self):
        return f"id: {self.item_id}, name: {self.name}, expiry_time: {self.expiry_time}, date_added: {self.date_added}, expiry_date: {self.expiry_date}, quantity: {self.quantity}"

    def update_expiry(self, new_date: date):
        """Updates expiry_date to new_date."""
        self.expiry_date = new_date

    def days_to_expiry(self) -> int:
        """Returns number of days between expiry date and present date."""
        if self.expiry_date is None:
            return None
        else:
            return (self.expiry_date - date.today()).days
