import csv
import os

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
