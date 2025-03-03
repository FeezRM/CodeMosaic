from login import Login
from inventory import InventorySystem

class Main:
    def __init__(self):
        self.authenticated = False
        self.inventory = InventorySystem()

    def authenticate(self):
        """ Handles user login and registration """
        while not self.authenticated:
            print("\n1. Login")
            print("2. Register")
            print("3. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                username = input("Enter Username: ")
                password = input("Enter Password: ")
                user = Login(username, password)

                if user.check_login():
                    print("Login successful!")
                    self.authenticated = True
                    return
                else:
                    print("Invalid credentials. Try again.")

            elif choice == "2":
                username = input("Choose a Username: ")
                password = input("Choose a Password: ")
                user = Login(username, password)

                if user.add_login():
                    print("You can now log in!")
                else:
                    print("Registration failed. User may already exist.")

            elif choice == "3":
                print("\nExiting system...")
                exit()
            else:
                print("Invalid choice. Try again.")

    def main(self):
        """ Main menu after authentication """
        print("\nWelcome to Fashion Inventory Management System")
        self.authenticate()

        while True:
            print("\n1. Add Product")
            print("2. Remove Product")
            print("3. View Products")
            print("4. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                self.inventory.add_product()
            elif choice == "2":
                self.inventory.remove_product()
            elif choice == "3":
                self.inventory.view_products()
            elif choice == "4":
                print("\n👋 Exiting system...\n")
                break
            else:
                print("\n⚠ Invalid choice. Try again.")

if __name__ == "__main__":
    Main().main()
