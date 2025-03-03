import csv
import os

class Login:
    def __init__(self, username="", password=""):
        self.username = username.strip()
        self.password = password.strip()
        self.file_path = "csv_files/login_credentials.csv"
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """ Ensures the CSV file exists and has headers """
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Username", "Password"])  # Add header row

    def add_login(self):
        """ Adds a new user to the credentials file """
        if self.check_login():  # Prevent duplicate accounts
            print("User already exists!")
            return False

        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.username, self.password])  # Store credentials
            print("User registered successfully!")
            return True

    def check_login(self):
        """ Verifies if the username and password match a stored record """
        try:
            with open(self.file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header row
                for row in reader:
                    if row and len(row) == 2:  # Ensure valid row structure
                        stored_username, stored_password = row
                        if stored_username.strip() == self.username and stored_password.strip() == self.password:
                            return True
        except FileNotFoundError:
            return False
        return False


class InventorySystem:
    def __init__(self):
        self.authenticated = False
        self.products = []
        self.file_path = "csv_files/fashion_inventory.csv"
        self.fieldnames = ["Product Name", "Brand", "Category", "Price", "Color", "Size"]
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """ Ensures the CSV file exists with correct headers """
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.fieldnames)  # Write headers

    def authenticate(self):
        """ Handles user login, registration, and guest access """
        while not self.authenticated:
            print("\n1. Login")
            print("2. Register")
            print("3. Guest")
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

    def add_product(self):
        """ Adds a product to inventory with validation and duplicate checking """
        print("\nEnter product details:")

        product = {}
        for field in self.fieldnames:
            while True:
                value = input(f"{field}: ").strip()

                # Validate price input
                if field == "Price" and not value.replace('.', '', 1).isdigit():
                    print("Invalid price! Enter a valid number.")
                    continue

                # Ensure no empty fields
                if not value:
                    print(f"{field} cannot be empty. Please enter a valid value.")
                    continue

        # Check for duplicate product
        if self.is_duplicate(product):
            print("\n⚠️ Product already exists in inventory. Duplicate entry not added.")
            return

        # Add product to the inventory
        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(product)

        print("✅ Product added successfully!")

    def is_duplicate(self, product):
        """ Checks if a product already exists in the inventory """
        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if all(row[field] == product[field] for field in self.fieldnames):
                        return True
        except FileNotFoundError:
            return False
        return False

    def remove_product(self):
        """ Removes a product from the inventory """
        print("\nEnter details of the product you want to remove:")
        product_name = input("Product Name: ").strip()
        brand = input("Brand: ").strip()
        category = input("Category: ").strip()
        price = input("Price: ").strip()
        color = input("Color: ").strip()
        size = input("Size: ").strip()

        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                products = list(reader)  # Read all products into a list

            product_to_remove = {
                "Product Name": product_name,
                "Brand": brand,
                "Category": category,
                "Price": price,
                "Color": color,
                "Size": size
            }

            if product_to_remove not in products:
                print("\nProduct not found! Make sure you entered exact details.")
                return

            # Keep only products that do NOT match the full entry
            updated_products = [p for p in products if p != product_to_remove]

            # Write back updated products
            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()  # Write header first
                writer.writerows(updated_products)  # Write remaining products

            print("\n✅ Product removed successfully!")

        except FileNotFoundError:
            print("\n⚠️ Inventory file not found!")

    def view_products(self):
        """ Displays all products in inventory """
        print("\n📦 Current Inventory:")
        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                products = list(reader)

                if not products:
                    print("ℹ️ No products available.")
                else:
                    for product in products:
                        print(f"Name: {product['Product Name']}, Brand: {product['Brand']}, Category: {product['Category']}, "
                              f"Price: {product['Price']}, Color: {product['Color']}, Size: {product['Size']}")
        except FileNotFoundError:
            print("⚠️ No inventory file found!")

    def main(self):
        """ Main function to run the Inventory System """
        print("Welcome to Inventory Management System")
        self.authenticate()  # Ensure user is authenticated before accessing inventory

        while True:
            print("\n1. View Products")
            if self.authenticated != "guest":
                print("2. Add Product")
                print("3. Remove Product")
            print("4. Exit")

            choice = input("Select an option: ")

            if choice == "1":
                self.view_products()
            elif choice == "2" and self.authenticated != "guest":
                self.add_product()
            elif choice == "3" and self.authenticated != "guest":
                self.remove_product()
            elif choice == "4":
                print("Exiting...\n")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    system = InventorySystem()
    system.main()
