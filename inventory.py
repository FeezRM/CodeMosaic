import csv
import os


class InventorySystem:
    def __init__(self):
        self.file_path = "csv_files/fashion_inventory.csv"
        self.fieldnames = [
            "Product ID",
            "Product Name",
            "Brand",
            "Category",
            "Price",
            "Color",
            "Size",
            "Description",
            "Material",
            "Weight (kg)",
            "Stock Quantity",
        ]
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Ensures the CSV file exists with correct headers."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.fieldnames)  # Write headers

    def add_product(self):
        """Adds a product to inventory.csv, including a detailed description and material type."""
        print("\nEnter product details:")
        product_data = {
            "Product ID": input("Product ID: ").strip(),
            "Product Name": input("Product Name: ").strip().title(),
            "Brand": input("Brand: ").strip().title(),
            "Category": input("Category: ").strip().title(),
            "Price": input("Price: ").strip(),
            "Color": input("Color: ").strip().title(),
            "Size": input("Size: ").strip().title(),
            "Description": input("Description: ").strip(),
            "Material": input("Material: ").strip().title(),
            "Weight (kg)": input("Weight (kg): ").strip(),
            "Stock Quantity": input("Stock Quantity: ").strip(),
        }

        # Append product to CSV file
        with open(self.file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(product_data)

        print("\n✅ Product added successfully!")

    def remove_product(self):
        """Removes a product by Product ID."""
        product_id = input(
            "\nEnter the Product ID of the item you want to remove: "
        ).strip()

        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                products = list(reader)

            updated_products = [p for p in products if p["Product ID"] != product_id]

            if len(updated_products) == len(products):
                print(
                    "\n❌ Product not found! Ensure you entered the correct Product ID."
                )
                return

            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(updated_products)

            print("\n✅ Product removed successfully!")

        except FileNotFoundError:
            print("\n❌ Inventory file not found!")

    def view_products(self):
        """Displays all products in inventory in a structured tabular format, with better spacing and readability."""
        print("\n📦 **Current Inventory:**\n")
        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                products = list(reader)

                if not products:
                    print("No products available.")
                    return

                print("=" * 160)
                print(
                    f"{'ID':<5} {'Name':<20} {'Brand':<12} {'Category':<20} {'Price':<8} "
                    f"{'Color':<12} {'Size':<5} {'Stock':<8} {'Weight (kg)':<12} {'Material':<15}"
                )
                print("=" * 160)

                for product in products:
                    print(
                        f"{product['Product ID']:<5} {product['Product Name']:<20} {product['Brand']:<12} "
                        f"{product['Category']:<20} ${product['Price']:<7} {product['Color']:<12} {product['Size']:<5} "
                        f"{product['Stock Quantity']:<8} {product['Weight (kg)']:<12} {product['Material']:<15}"
                    )

                    # Add extra spacing and a divider for better readability
                    print(f"   📜 Description: {product['Description']}\n")
                    print("-" * 160)

        except FileNotFoundError:
            print("\n❌ No inventory file found!")

    def filter_products(self):
        """Filters products based on multiple criteria."""
        print("\nFilter products by one or more criteria:")
        filters = {}

        for key in self.fieldnames:
            if key != "Description":  # Exclude description from filtering
                value = input(
                    f"Enter value for {key} (or press Enter to skip): "
                ).strip()
                if value:
                    filters[key] = value

        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                products = list(reader)

            filtered_products = [
                product
                for product in products
                if all(product[key] == value for key, value in filters.items())
            ]

            if not filtered_products:
                print("No products match the filter criteria.")
            else:
                print("\nFiltered Products:")
                for product in filtered_products:
                    print(f"{product}")

        except FileNotFoundError:
            print("Inventory file not found!")

    def modify_product_details(self):
        """Modifies an existing product's details."""
        print("\nEnter the Product ID of the item you want to modify:")
        product_id = input("Product ID: ").strip()

        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                products = list(reader)

            # Find the product to modify
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

                    # Rewrite the file with modified details
                    with open(self.file_path, mode="w", newline="") as file:
                        writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                        writer.writeheader()
                        writer.writerows(products)

                    print("\nProduct details updated successfully!")
                    return

            print("\nProduct not found! Ensure you entered the correct Product ID.")

        except FileNotFoundError:
            print("\nInventory file not found!")
