from mysql.connector import connection
from inventory import inventory
import smtplib



class Checkout():

    """Checks out user cart, updates inventory, send email"""
    
    
    def __init__(self, account):
        self.account = account
        self.cart = account.cart
        

    def update_inventory(self):
        """Update inventory quanity for removed cart items and updates user balance"""
        if self.account.cart == {}:
            return "\n" + "Nothing in Cart"
        self.account.total = 0
        for num in self.account.cart.values():
            self.account.total += (num.quanity * num.price)

        if self.account.total > self.account.balance:
            return f"Not enough money to purchase. Need ${self.account.total} and have ${self.account.balance}."
        else:
            for item in self.account.cart.keys():
                if (inventory[item].quanity - self.account.cart[item].quanity) < 0:
                    return f"There is not enough in stock for {item}. Current stock is {inventory[item].quanity}"
                else:
                    try:
                        inventory[item].quanity = (inventory[item].quanity - self.account.cart[item].quanity)
                        self.account.addBalance((-(self.account.total)))

                    except Exception as e:
                        return e
            Checkout.email_user(self.account)
            self.cart.clear()
            return "\n" + "Items Purchased Sucessfully"

    def email_user(self):
        """Sends email to user with items purchased"""
        items_purchased = ['<br>'.join(f'Name: {item.name}, Quanity:{item.quanity}, Price:{item.price}' for item in self.cart.values())]

        smtpServer = "192.168.0.7"
        FROM = "testpython@test.com"
        TO = "bla@test.com"
        MSG = f"""
<!DOCTYPE html>
<html>
<body>
Subject: Purchase Sucessfull python

Items Purchased: <br> <br> {''.join(items_purchased)}

Total: ${self.total}

Balance: ${self.balance}

</body>
</html>
        """
        server = smtplib.SMTP(smtpServer,1025)
        server.sendmail(FROM, TO, MSG) 
        server.quit()
