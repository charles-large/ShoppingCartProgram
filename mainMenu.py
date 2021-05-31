import time, stdiomask
from account import Account
from cart import Cart
from inventory import inventory
from os import system, name
from checkout import Checkout


class InvalidCredentials(Exception):
    pass
    
def quitProgram():
    print("Quitting program")
    Account.mysql_connect.close()
    quit()

def clear():

    """Clears the screen"""
  
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def mainMenu():
    clear()

    print("""    
Ecommerce Website

1. Login
2. Create Account
3. Quit
    """)

    login_prompt = input("Choice: ")
    if login_prompt.lower() == "login" or login_prompt == "1":
        clear()
        print("Enter Credentials" + ("\n" * 2))
        username = input("Username: ")
        password = stdiomask.getpass("Password: ")
        test_login_acc = Account(username, password)
        try:
            logged_in_account = test_login_acc.accountQuery()
            if logged_in_account:
               logged_in_account.cart = Cart()
               logged_in_menu(logged_in_account)
            else:
                raise InvalidCredentials
        except InvalidCredentials as e:
            print(("\n" * 3) + "Invalid Username and Password Combination")
            print("Returning to Menu")
            time.sleep(2)
            clear()
            mainMenu()
            

    elif login_prompt.lower() == "create account" or login_prompt == "2":
        clear()
        print("Enter Account Information" + ("\n" * 2))
        username = input("Username: ")
        password = input("Password: ")
        email = input("Email: ")
        try:
            temp_create_account = Account(username, password, True, email)
            try:
                temp_create_account.createAccount()
            except:
                print("A database error occured")
            print("""
Account Created Successfully

Returning to Main Menu
""")
            time.sleep(2)
            clear()
            mainMenu()
        except:
            print("An Account Creation error occured")

    elif login_prompt == "quit" or login_prompt == "3":
        quitProgram()
        
def logged_in_menu(logged_in_user):
    """Menu to add item to cart, remove item from cart, show cart, sort items, logout, exit, balance, add balance.
    This will be shown when user is validated logged in."""
    clear()
    print(f"Logged In as {logged_in_user.username}")
    print("""
1. Show Balance
2. Add to Balance
3. Show Cart
4. Add to Cart
5. Remove Item from Cart
6. Checkout
7. Logout
8. Exit
        """)
    selection_input = input("Choice: ")
    if selection_input == "Show Balance" or selection_input == "1":
        clear()
        print("Current Balance")
        print(("\n") + "$" + str(logged_in_user.balance))
        balance_continue = input("\n" + "Press Any Key to Return: ")
        logged_in_menu(logged_in_user)

    elif selection_input == "Add to Balance" or selection_input == "2":
        clear()
        print("How much money would you like to add?" + ("\n" * 2))
        amount = input("Amount: ")
        try:
            logged_in_user.addBalance(amount)
            print("Balance Updated")
            balance_continue = input("\n" + "Press Any Key to Return: ")
            logged_in_menu(logged_in_user)
        except Exception as e:
            print(e)
            print("An error occured updating your balance")
    
    elif selection_input == "Show Cart" or selection_input == "3":
        clear()
        print("Cart Contents:" + ("\n"))
        print(logged_in_user.cart.display_cart())
        balance_continue = input("\n" + "Press Any Key to Return: ")
        logged_in_menu(logged_in_user)
    
    elif selection_input == "Add to Cart" or selection_input == "4":
            clear()
            print("Inventory Contents:" + ("\n"))
            print(inventory.display_inventory() + ("\n"))
            item_selection_index = input("Select an item to add to cart: ")
            quanity = input("How many of this item to add?: ")
            clear()
            print(logged_in_user.cart.add_item_to_cart(item_selection_index, quanity))
            print("Cart: " + "\n" + logged_in_user.cart.display_cart())
            balance_continue = input("\n" + "Press Any Key to Return: ")
            logged_in_menu(logged_in_user)
    elif selection_input == "Remove Item from Cart" or selection_input == "5":
            clear()
            print("Cart Contents:" + ("\n"))
            print(logged_in_user.cart.display_cart())
            if logged_in_user.cart.display_cart() == "":
                balance_continue = input("\n" + "Press Any Key to Return: ")
            else:
                item_selection_index = input("Select an item to remove from cart: ")
                quanity = input("How many of this item to remove?: ")
                clear()
                print(logged_in_user.cart.remove_item_from_cart(item_selection_index, quanity))
                print("Cart: " + "\n" + logged_in_user.cart.display_cart())
                balance_continue = input("\n" + "Press Any Key to Return: ")
            logged_in_menu(logged_in_user)
    elif selection_input == "Checkout" or selection_input == "6":
        checkout = Checkout(logged_in_user)
        print(checkout.update_inventory())
        balance_continue = input("\n" + "Press Any Key to Return: ")
        logged_in_menu(logged_in_user)

    elif selection_input == "Logout" or selection_input == "7":
            mainMenu()
    elif selection_input == "Quit" or selection_input == "8":
        quitProgram()
        
        

mainMenu()

