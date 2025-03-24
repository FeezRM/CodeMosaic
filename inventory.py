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
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(self.fieldnames)

    def add_product(self):
        print("\n➕ Add a New Product:")
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

        with open(self.file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(product_data)

        print("\n✅ Product added successfully!")

    def remove_product(self):
        print("\n🗑️ Remove a Product:")
        product_id = input("Enter Product ID to remove: ").strip()

        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                products = list(reader)

            updated_products = [p for p in products if p["Product ID"] != product_id]

            if len(updated_products) == len(products):
                print("\n❌ Product not found. Please check the Product ID.")
                return

            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(updated_products)

            print("\n✅ Product removed successfully!")

        except FileNotFoundError:
            print("\n❌ Inventory file not found!")

    def view_products(self):
        print("\n📦 Current Inventory:\n")
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
                    print(f"   📜 Description: {product['Description']}\n")
                    print("-" * 160)

        except FileNotFoundError:
            print("\n❌ No inventory file found!")

    def filter_products(self):
        print("\n🔍 Filter products by one or more criteria:")
        filters = {}
        price_range = {}

        # Get price range if specified
        min_price = input("➡️  Minimum Price (press Enter to skip): ").strip()
        max_price = input("➡️  Maximum Price (press Enter to skip): ").strip()

        if min_price or max_price:
            price_range["min"] = float(min_price) if min_price else 0
            price_range["max"] = float(max_price) if max_price else float("inf")

        # Get other filters
        for key in self.fieldnames:
            if key != "Description" and key != "Price":
                value = input(f"➡️  {key} (press Enter to skip): ").strip()
                if value:
                    filters[key] = value.title()

        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                products = list(reader)

            filtered_products = []
            for product in products:
                # Check price range if specified
                price_match = True
                if price_range:
                    try:
                        product_price = float(product["Price"])
                        if not (
                            price_range["min"] <= product_price <= price_range["max"]
                        ):
                            price_match = False
                    except ValueError:
                        price_match = False

                # Check other filters
                other_filters_match = all(
                    product[key] == value for key, value in filters.items()
                )

                if price_match and other_filters_match:
                    filtered_products.append(product)

            if not filtered_products:
                print("\n❌ No products match the filter criteria.")
            else:
                print("\n✅ Matching Products:\n")
                print("=" * 160)
                print(
                    f"{'ID':<5} {'Name':<20} {'Brand':<12} {'Category':<20} {'Price':<8} "
                    f"{'Color':<12} {'Size':<5} {'Stock':<8} {'Weight (kg)':<12} {'Material':<15}"
                )
                print("=" * 160)

                for product in filtered_products:
                    print(
                        f"{product['Product ID']:<5} {product['Product Name']:<20} {product['Brand']:<12} "
                        f"{product['Category']:<20} ${product['Price']:<7} {product['Color']:<12} {product['Size']:<5} "
                        f"{product['Stock Quantity']:<8} {product['Weight (kg)']:<12} {product['Material']:<15}"
                    )
                    print(f"   📜 Description: {product['Description']}\n")
                    print("-" * 160)

        except FileNotFoundError:
            print("❌ Inventory file not found!")
        except ValueError:
            print("❌ Invalid price format. Please enter numbers for price range.")

    def modify_product_details(self):
        print("\n✏️ Modify Product Details:")
        product_id = input("Product ID: ").strip()

        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                products = list(reader)

            for product in products:
                if product["Product ID"] == product_id:
                    print("\n📄 Current Product Details:")
                    for key, value in product.items():
                        print(f"{key}: {value}")

                    print(
                        "\n🔁 Enter new details (press Enter to keep existing value):"
                    )
                    for key in self.fieldnames:
                        if key == "Product ID":
                            continue
                        new_value = input(f"{key} ({product[key]}): ").strip()
                        if new_value:
                            product[key] = new_value.title()

                    with open(self.file_path, mode="w", newline="") as file:
                        writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                        writer.writeheader()
                        writer.writerows(products)

                    print("\n✅ Product details updated successfully!")
                    return

            print("\n❌ Product not found. Check Product ID.")

        except FileNotFoundError:
            print("\n❌ Inventory file not found!")
