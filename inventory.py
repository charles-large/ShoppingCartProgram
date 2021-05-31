
from products import Products

class Inventory(dict):

    """Class that acts as a dict for storing and altering the inventory. The inventory will stay as 
    a dictionary within the class."""

    def __init__(self):
        
        self.__dict__ = self 
    
    def copy(self):
        return super().copy()

    def display_inventory(self):
        """Displays list of inventory items"""
        
        def number_generator():
            """Generates next value for list numbering"""
            num = 1
            while True:
                yield num
                num += 1
        gen = number_generator()
        inventory_list = [(f"{next(gen)}. Name: {value.name}, Price: {value.price}, Category: {value.category}, Quanity: {value.quanity}") for key, value in self.items()]
        inventory_str = "\n".join(inventory_list)
        return inventory_str


    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError as e:
            return e

    def __setitem__(self, key, value):
        super().__setitem__(key, value)

inventory = Inventory()

products = [Products("Regular Shirt", 30, "Clothes", 500), Products("iPod", 200, "Electronics", 3), Products("Vaccuum", 125, "Home and Garden", 2)]

for x in products:
    inventory[x.name] = x

print(inventory.display_inventory())