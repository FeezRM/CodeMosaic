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

            print("\nProduct removed successfully!")

        except FileNotFoundError:
            print("\nInventory file not found!")

    def filter_products(self):
        """ Filters products based on user criteria """
        print("\nEnter filter criteria (leave blank to skip a criterion):")
        brand = input("Brand: ").strip()
        category = input("Category: ").strip()
        price_min = input("Minimum Price: ").strip()
        price_max = input("Maximum Price: ").strip()
        color = input("Color: ").strip()
        size = input("Size: ").strip()
        
        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                products = list(reader)
                
                filtered_products = []
                for product in products:
                    if brand and product['Brand'].lower() != brand.lower():
                        continue
                    if category and product['Category'].lower() != category.lower():
                        continue
                    if price_min and float(product['Price']) < float(price_min):
                        continue
                    if price_max and float(product['Price']) > float(price_max):
                        continue
                    if color and product['Color'].lower() != color.lower():
                        continue
                    if size and product['Size'].lower() != size.lower():
                        continue
                    
                    filtered_products.append(product)
                
                if filtered_products:
                    print("\nFiltered Products:")
                    for product in filtered_products:
                        print(f"{product['Product Name']} | {product['Brand']} | {product['Category']} | ${product['Price']} | {product['Color']} | {product['Size']}")
                else:
                    print("\nNo products matched the given criteria.")
        
        except FileNotFoundError:
            print("\nInventory file not found!")

    def main(self):
        """ Main function to run the Inventory System """
        print("Welcome to Inventory Management System")
        while True:
            print("\n1. View Products")
            print("2. Filter Products")
            print("3. Add Product")
            print("4. Remove Product")
            print("5. Exit")

            choice = input("Select an option: ")

            if choice == "1":
                self.view_products()
            elif choice == "2":
                self.filter_products()
            elif choice == "3":
                self.add_product()
            elif choice == "4":
                self.remove_product()
            elif choice == "5":
                print("Exiting...\n")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    system = InventorySystem()
    system.main()
