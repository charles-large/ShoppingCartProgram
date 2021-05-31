from mysql.connector import connection 
import hashlib
import random

class Account():

    """Creates a user account taking a username, password, email.
    An instance of a cart class will be created and each new user will have  
    a hash, two salts and starting balance of $0 created."""

    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    

    def __init__(self, username, passwd, newaccount=False, email=None, salt=None, salt2=None, cart=None, balance=0):
        
        if newaccount:
            """For New Accounts"""
            self.balance = balance
            self.username = username
            self.__email = email
            self.__salt = ''.join(random.choice(Account.ALPHABET) for i in range(8))
            self.__salt2 = ''.join(random.choice(Account.ALPHABET) for i in range(8))
            self.__passwd = Account.hashPassword(self, passwd)
        elif not newaccount and salt == None:
            """Creating temp account for query comparison"""
            self.__passwd =  passwd.encode()
            self.username = username
        else:
            """For Other Account (Comparison)"""
            self.__passwd =  passwd
            self.balance = balance
            self.username = username
            self.__email = email
            self.__salt = salt
            self.__salt2 = salt2

            

    def hashPassword(self, passwd):
        """Hashes password and adds salts"""
        binary_password = passwd.encode()
        presalt_hashed_passwd = hashlib.sha256(binary_password).hexdigest()
        salted_passwd = self.__salt + presalt_hashed_passwd + self.__salt2
        return salted_passwd
    
    
    def compareHash(self, salt, salt2):
        """Takes hash of password and adds salts from database"""
        presalt_hashed_passwd = hashlib.sha256(self.__passwd).hexdigest()
        salted_passwd = salt + presalt_hashed_passwd + salt2
        return salted_passwd

    def addBalance(self, amount):
        updated_balance = int(self.balance) + int(amount)
        self.balance = updated_balance
        cursor = Account.mysql_connect.cursor()
        data = (f"UPDATE User_Data SET balance=\"{updated_balance}\" WHERE username=\"{self.username}\"")
        try:
            cursor.execute(data)
            Account.mysql_connect.commit()
        except:
            Account.mysql_connect.rollback()
        finally:
            cursor.close()

    def createAccount(self):
        mysql_connect = connection.MySQLConnection(user='clarge', password='Applesauce34!', host='192.168.0.7', database='Shopping_Cart')
        """Upload mysql data for customer to server"""
        cursor = Account.mysql_connect.cursor()
        data = (f"INSERT INTO User_Data VALUES (\"{self.username}\", \"{(self.__passwd)}\", \"{(self.__salt)}\", \"{self.__email}\", \"{self.balance}\", \"{self.__salt2}\");")
        try:
            cursor.execute(data)
            Account.mysql_connect.commit()
        except:
            Account.mysql_connect.rollback()
        finally:
            cursor.close()
    
    
    def accountQuery(self):
        mysql_connect = connection.MySQLConnection(user='clarge', password='Applesauce34!', host='192.168.0.7', database='Shopping_Cart')
        """Query the database with a given username, returns account information"""
        cursor = Account.mysql_connect.cursor()
        query = f"SELECT username, hashed_passwd, email, salt, salt2, balance FROM User_Data WHERE username=\"{self.username}\""
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            temp_result = [x for x in result[0]]
            account_compare = Account(temp_result[0], (temp_result[1]), False, temp_result[2],
            (temp_result[3]), (temp_result[4]), None, temp_result[5])
            return self.accountVerification(account_compare)
        except:
            print("A login with that username is not valid")
            menu()
        finally:
            cursor.close()
        
        

    def accountVerification(self, other_account):
        """Verifies if the passwords match"""
        if Account.compareHash(self, other_account.__salt, other_account.__salt2) == other_account.__passwd:
            return other_account
        else:
            return False
            
          




