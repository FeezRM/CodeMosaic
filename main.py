from inventory import InventorySystem
from login import Login

class App:
    def __init__(self):
        self.authenticated = False
        self.inventory = InventorySystem()
    
    def authenticate(self):
        """Handles user login, registration, and guest access."""
        while not self.authenticated:
            print("\n1. Login")
            print("2. Register")
            print("3. Guest Mode")
            print("4. Exit")
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
                print("\nYou are now using the system as a Guest. You can only view products.")
                self.authenticated = "guest"
                return

            elif choice == "4":
                print("Exiting system...")
                exit()
            else:
                print("Invalid choice. Try again.")

    def run(self):
        """Main function to run the Inventory System."""
        print("Welcome to the Fashion Inventory System!")
        self.authenticate()  # Ensure user is authenticated before accessing inventory

        while True:
            print("\n1. View Products")
            if self.authenticated != "guest":
                print("2. Add Product")
                print("3. Remove Product")
            print("4. Filter Products")
            print("5. Exit")

            choice = input("Select an option: ")

            if choice == "1":
                self.inventory.view_products()
            elif choice == "2" and self.authenticated != "guest":
                self.inventory.add_product()
            elif choice == "3" and self.authenticated != "guest":
                self.inventory.remove_product()
            elif choice == "4":
                self.inventory.filter_products()
            elif choice == "5":
                print("Exiting...\n")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    app = App()
    app.run()