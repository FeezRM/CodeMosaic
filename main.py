import csv
import os

import csv
import os

class Login:
    def __init__(self, username="", password=""):
        self.username = username.strip()
        self.password = password.strip()
        self.file_path = "csv_files/login_credentials.csv"
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """ Ensures the login CSV file exists with headers """
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Username", "Password"])  # Add header row

    def add_login(self):
        """ Registers a new user """
        if self.check_login():
            print("User already exists!")
            return False

        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.username, self.password])  # Store credentials
            print("User registered successfully!")
            return True

    def check_login(self):
        """ Checks if the entered username & password match an existing user """
        try:
            with open(self.file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header row
                for row in reader:
                    if row and len(row) == 2:
                        stored_username, stored_password = row
                        if stored_username.strip() == self.username and stored_password.strip() == self.password:
                            return True
        except FileNotFoundError:
            return False
        return False


class InventorySystem:
    def __init__(self):
        self.file_path = "csv_files/fashion_inventory.csv"
        self.fieldnames = ["Product ID", "Product Name", "Brand", "Category", "Price", "Color", "Size"]
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Ensures the CSV file exists with correct headers."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.fieldnames)  # Write headers

    def add_product(self):
        """Adds a product to inventory.csv where user can put info in one line"""
        print("\nEnter product details in the following format:")
        print("Product_ID Product_Name Brand Category Price Color Size")
        print("Example: 25 Shoes Nike Men's 20 Red L")

        product_input = input("\n Enter product details: ").strip().split()

            # Ensure the correct number of inputs
        if len(product_input) != 7:
            print("\nInvalid input! Please enter exactly 7 values separated by spaces.")
            return
        
        product_id, product_name, brand, category, price, color, size = product_input

        product = {
            "Product ID": product_id,
            "Product Name": product_name.title(),
            "Brand": brand.title(),
            "Category": category.title(),
            "Price": price,
            "Color": color.title(),
            "Size": size.title()
        }

            # Append product to CSV file
        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            if file.tell() == 0:  # If file is empty, write header
                writer.writeheader()
            writer.writerow(product)

        print("\nProduct added successfully!")

    def remove_product(self):
        """Removes a product by Product ID."""
        print("\nEnter the Product ID of the item you want to remove:")
        product_id = input("Product ID: ").strip()

        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                products = list(reader)

            updated_products = [p for p in products if p["Product ID"] != product_id]

            if len(updated_products) == len(products):
                print("\nProduct not found! Ensure you entered the correct Product ID.")
                return

            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(updated_products)

            print("\nProduct removed successfully!")

        except FileNotFoundError:
            print("\nInventory file not found!")

    def view_products(self):
        """Displays all products in inventory."""
        print("\nCurrent Inventory:")
        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                products = list(reader)
                
                if not products:
                    print("No products available.")
                else:
                    for product in products:
                        print(f"ID: {product['Product ID']}, Name: {product['Product Name']}, "
                              f"Brand: {product['Brand']}, Category: {product['Category']}, "
                              f"Price: {product['Price']}, Color: {product['Color']}, Size: {product['Size']}")
        except FileNotFoundError:
            print("No inventory file found.")

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
            print("4. Exit")

            choice = input("Select an option: ")

            if choice == "1":
                self.inventory.view_products()
            elif choice == "2" and self.authenticated != "guest":
                self.inventory.add_product()
            elif choice == "3" and self.authenticated != "guest":
                self.inventory.remove_product()
            elif choice == "4":
                print("Exiting...\n")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    app = App()
    app.run()
