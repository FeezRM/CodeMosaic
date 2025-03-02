import csv
import os

class InventorySystem:
    def __init__(self):
        self.file_path = "csv_files/fashion_inventory.csv"
        self.fieldnames = ["Product Name", "Brand", "Category", "Price", "Color", "Size"]
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """ Ensures the inventory CSV file exists with headers """
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.fieldnames)  # Write headers

    def add_product(self):
        """ Adds a product to inventory """
        print("\nEnter product details:")
        product_name = input("Product Name: ").strip()
        brand = input("Brand: ").strip()
        category = input("Category: ").strip()
        price = input("Price: ").strip()
        color = input("Color: ").strip()
        size = input("Size: ").strip()

        product = {
            "Product Name": product_name,
            "Brand": brand,
            "Category": category,
            "Price": price,
            "Color": color,
            "Size": size
        }

        with open(self.file_path, mode="a", newline="\n") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(product)

        print("Product added successfully!")

    def remove_product(self):
        """ Removes a product by exact match of all attributes """
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
                products = list(reader)

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

            updated_products = [p for p in products if p != product_to_remove]

            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(updated_products)

            print("\nProduct removed successfully!")

        except FileNotFoundError:
            print("\nInventory file not found!")

    def view_products(self):
        """ Displays all products in inventory """
        print("\nCurrent Inventory:")
        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                products = list(reader)
                
                if not products:
                    print("No products available.")
                else:
                    for product in products:
                        print(f"{product['Product Name']} | {product['Brand']} | {product['Category']} | ${product['Price']} | {product['Color']} | {product['Size']}")
        except FileNotFoundError:
            print("\nNo inventory file found!")
