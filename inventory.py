import csv
import os

class InventorySystem:
    def __init__(self):
        self.file_path = "csv_files/fashion_inventory.csv"
        self.fieldnames = ["Product ID", "Product Name", "Brand", "Category", "Price", "Color", "Size", "Description"]
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Ensures the CSV file exists with correct headers."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.fieldnames)  # Write headers

    def add_product(self):
        """Adds a product to inventory.csv, including a description."""
        print("\nEnter product details:")
        product_id = input("Product ID: ").strip()
        product_name = input("Product Name: ").strip().title()
        brand = input("Brand: ").strip().title()
        category = input("Category: ").strip().title()
        price = input("Price: ").strip()
        color = input("Color: ").strip().title()
        size = input("Size: ").strip().title()
        description = input("Description: ").strip()

        product = {
            "Product ID": product_id,
            "Product Name": product_name,
            "Brand": brand,
            "Category": category,
            "Price": price,
            "Color": color,
            "Size": size,
            "Description": description,
        }

        with open(self.file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(product)

        print("\n✅ Product added successfully!")

    def modify_product_details(self):
        """Modifies an existing product's details, including description."""
        print("\nEnter the Product ID of the item you want to modify:")
        product_id = input("Product ID: ").strip()

        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                products = list(reader)

            for product in products:
                if product["Product ID"] == product_id:
                    print("\nCurrent product details:")
                    for key, value in product.items():
                        print(f"{key}: {value}")

                    print("\nEnter new details (press Enter to keep existing value):")
                    for key in self.fieldnames:
                        if key == "Product ID":
                            continue  # Product ID should remain unchanged
                        new_value = input(f"{key} ({product[key]}): ").strip()
                        if new_value:
                            product[key] = new_value.title()

                    with open(self.file_path, mode="w", newline="") as file:
                        writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                        writer.writeheader()
                        writer.writerows(products)

                    print("\n✅ Product details updated successfully!")
                    return

            print("\n❌ Product not found! Ensure you entered the correct Product ID.")

        except FileNotFoundError:
            print("\n❌ Inventory file not found!")

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

        filter_choices = input("Enter filter options (e.g., '6 7' for Color and Size): ").strip().split()

        filters = {}
        for choice in filter_choices:
            if choice == "1":
                filters["Product ID"] = input("Enter the Product ID to filter by: ").strip()
            elif choice == "2":
                filters["Product Name"] = input("Enter the Product Name to filter by: ").strip().title()
            elif choice == "3":
                filters["Brand"] = input("Enter the Brand to filter by: ").strip().title()
            elif choice == "4":
                filters["Category"] = input("Enter the Category to filter by: ").strip().title()
            elif choice == "5":
                try:
                    filters["Price"] = float(input("Enter the Price to filter by: ").strip())
                except ValueError:
                    print("Invalid price input. Please enter a numeric value.")
                    return
            elif choice == "6":
                filters["Color"] = input("Enter the Color to filter by: ").strip().title()
            elif choice == "7":
                filters["Size"] = input("Enter the Size to filter by: ").strip().title()
            elif choice == "8":
                if not filters:
                    print("No filters selected. Please add at least one filter.")
                    return
                break
            elif choice == "9":
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
