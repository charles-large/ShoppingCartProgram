from inventory import inventory
import copy


class Cart(dict):

    """Class that operates as dictionary that will store user items inside that they
    add to cart."""

    def __init__(self):
        self.__dict__ = self
        
    def __setitem__(self, key, value):
        """Defines item in dict. Allows assignment in bracket notation."""
        super().__setitem__(key, value)
    
    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError as e:
            return e

    def __delitem__(self, key):
        super().__delitem__(key)
    
    def display_cart(self):
        """Displays list of cart items"""
        def number_generator():
            """Generates next value for list numbering"""
            num = 1
            while True:
                yield num
                num += 1
        gen = number_generator()
        cart_list = [(f"{next(gen)}. Name: {value.name}, Price: {value.price}, Category: {value.category}, Quanity: {value.quanity}") for key, value in self.items()]
        cart_str = "\n".join(cart_list)
        return cart_str

    def clear(self):
        return super().clear()

    def add_item_to_cart(self, index, quanity):
        """Gets item to add to cart from user input based on display_inventory"""
        try:
            inventory_item = list(inventory)[int(index)-1]
            """Check if quanity of item is at least 1"""
            if inventory[inventory_item].quanity >= 1:
                """Checks if request quanity matches in stock values"""
                if (inventory[inventory_item].quanity - int(quanity)) < 0:
                    return "Unsupported Stock Quanity" + "\n" 
                else:
                    """If this item is already in cart, adjust quanity"""
                    if inventory_item in self.keys():
                        self[inventory_item].quanity = self[inventory_item].quanity + int(quanity)
                    else:
                        """Add item to cart, adjust quanity"""
                        self[inventory_item] = copy.deepcopy(inventory[inventory_item])
                        self[inventory_item].quanity = int(quanity)
                    return "Added Item to Cart" + "\n"
            else:
                return "There are none left in stock"
        except IndexError:
            return "Invalid Option" + "\n"
        except ValueError:
            return "Entry must be a number in list" + "\n"
        
    def remove_item_from_cart(self, index, quanity):
        """Gets item to add to cart from user input based on display_inventory"""
        try:
            inventory_item = list(self)[int(index)-1]
            """Checks if item is in cart"""
            if inventory_item in self.keys():
                """If quanity specified is not within cart"""
                if self[inventory_item].quanity < int(quanity):
                    return "Too much quanity specified"
                """Check if quanity of item is at least 1"""
                if self[inventory_item].quanity >= 1:
                    """If quanity of item removed is less than or equal to 0 -> delete"""
                    if (self[inventory_item].quanity - int(quanity)) <= 0:
                        del self[inventory_item]
                    elif (self[inventory_item].quanity - int(quanity)) > 0:
                        """If quanity above 0, adjust cart quanity to new value"""
                        self[inventory_item].quanity = self[inventory_item].quanity - int(quanity)
                    return "Updated Cart" + "\n"       
            else:
                return "There are no items that match in cart"
        except IndexError:
            return "Invalid Option" + "\n"
        except ValueError:
            return "Entry must be a number in list" + "\n"

