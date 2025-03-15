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

    
    def filter_products(self):
        """Filters products based on multiple criteria specified in a single input."""
        print("\nFilter products by one or more criteria:")
        print("1. Product ID")
        print("2. Product Name")
        print("3. Brand")
        print("4. Category")
        print("5. Price")
        print("6. Color")
        print("7. Size")
        print("8. Apply Filters")
        print("9. Cancel")

        # Ask for filter options in a single input
        filter_choices = input("Enter filter options (e.g., '6 7' for Color and Size): ").strip().split()

        filters = {}  # Dictionary to store filter criteria
        for choice in filter_choices:
            if choice == "1":  # Filter by Product ID
                product_id = input("Enter the Product ID to filter by: ").strip()
                filters["Product ID"] = product_id

            elif choice == "2":  # Filter by Product Name
                product_name = input("Enter the Product Name to filter by: ").strip().title()
                filters["Product Name"] = product_name

            elif choice == "3":  # Filter by Brand
                brand = input("Enter the Brand to filter by: ").strip().title()
                filters["Brand"] = brand

            elif choice == "4":  # Filter by Category
                category = input("Enter the Category to filter by: ").strip().title()
                filters["Category"] = category

            elif choice == "5":  # Filter by Price
                try:
                    price = float(input("Enter the Price to filter by: ").strip())
                    filters["Price"] = price
                except ValueError:
                    print("Invalid price input. Please enter a numeric value.")
                    return

            elif choice == "6":  # Filter by Color
                color = input("Enter the Color to filter by: ").strip().title()
                filters["Color"] = color

            elif choice == "7":  # Filter by Size
                size = input("Enter the Size to filter by: ").strip().title()
                filters["Size"] = size

            elif choice == "8":  # Apply Filters
                if not filters:
                    print("No filters selected. Please add at least one filter.")
                    return
                break

            elif choice == "9":  # Cancel
                print("Filtering canceled.")
                return

            else:
                print(f"Invalid filter option: {choice}. Please try again.")
                return

        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                products = list(reader)

            if not products:
                print("No products available to filter.")
                return

            # Apply all filters
            filtered_products = products
            for key, value in filters.items():
                if key == "Price":
                    filtered_products = [p for p in filtered_products if float(p[key]) == value]
                else:
                    filtered_products = [p for p in filtered_products if p[key] == value]

            if not filtered_products:
                print("No products match the filter criteria.")
            else:
                print("\nFiltered Products:")
                for product in filtered_products:
                    print(
                        f"ID: {product['Product ID']}, Name: {product['Product Name']}, "
                        f"Brand: {product['Brand']}, Category: {product['Category']}, "
                        f"Price: {product['Price']}, Color: {product['Color']}, Size: {product['Size']}"
                    )

        except FileNotFoundError:
            print("Inventory file not found!")
                        

