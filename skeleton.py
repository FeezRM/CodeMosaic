import csv


class InventorySystem:
    def __init__(self):
        self.authenticated = False
        self.products = []

    def authenticate(self, username, password):
        USER_NAME = "admin"
        PASSWORD = "OTU2025"
        if username == USER_NAME and password == PASSWORD:
            print("Login successful!")
            self.authenticated = True
        else:
            print("Invalid credentials")

    def add_product(self):
        # add to inventory.csv
        product_name = input("Enter Product Name: ")
        product_price = input("Enter Product Price: ")
        product_quantity = input("Enter Product Quantity: ")
        product = {
            "name": product_name,
            "price": product_price,
            "quantity": product_quantity,
        }
        self.products.append(product)

        with open("inventory.csv", mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "price", "quantity"])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(product)

        print("Product added successfully")

    def remove_product(self):
        print("Remove Product")

    def view_products(self):
        print("View Products")

    def main(self):
        print("Welcome to Inventory Management System")
        while not self.authenticated:
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            self.authenticate(username, password)

        while True:
            print("\n1. Add Product")
            print("2. Remove Product")
            print("3. View Products")
            print("4. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                self.add_product()
            elif choice == "2":
                self.remove_product()
            elif choice == "3":
                self.view_products()
            elif choice == "4":
                print("Exiting...\n")
                break
            else:
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    system = InventorySystem()
    system.main()
