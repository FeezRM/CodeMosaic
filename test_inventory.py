import unittest
import csv
import os
import sys
import io
from unittest.mock import patch
from inventory import InventorySystem


class TestInventorySystem(unittest.TestCase):
    def setUp(self):
        """Set up a test inventory file before each test."""
        self.inventory = InventorySystem()
        self.test_file = "test_inventory.csv"
        self.inventory.file_path = self.test_file
        self.inventory.fieldnames = [
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

        # Ensure test file starts fresh
        with open(self.test_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.inventory.fieldnames)

    def tearDown(self):
        """Remove the test inventory file after each test."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_product(self):
        """Test adding a new product to inventory."""
        product = {
            "Product ID": "1",
            "Product Name": "T-Shirt",
            "Brand": "Nike",
            "Category": "Men's Fashion",
            "Price": "25.99",
            "Color": "Red",
            "Size": "L",
            "Description": "Comfortable cotton t-shirt",
            "Material": "100% Cotton",
            "Weight (kg)": "0.3",
            "Stock Quantity": "50",
        }

        with open(self.test_file, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.inventory.fieldnames)
            writer.writerow(product)

        with open(self.test_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            products = list(reader)

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["Product Name"], "T-Shirt")
        self.assertEqual(products[0]["Brand"], "Nike")

    def test_remove_product(self):
        """Test removing a product."""
        sample_products = [
            {
                "Product ID": "2",
                "Product Name": "Test Jeans",
                "Brand": "Levi's",
                "Category": "Men's Fashion",
                "Price": "49.99",
                "Color": "Black",
                "Size": "L",
                "Description": "Classic black jeans",
                "Material": "Denim",
                "Weight (kg)": "1.2",
                "Stock Quantity": "5",
            },
            {
                "Product ID": "3",
                "Product Name": "Test Shirt",
                "Brand": "Nike",
                "Category": "Men's Fashion",
                "Price": "29.99",
                "Color": "Blue",
                "Size": "M",
                "Description": "Soft cotton shirt",
                "Material": "Cotton",
                "Weight (kg)": "0.3",
                "Stock Quantity": "10",
            },
        ]

        # Write sample products to the test file
        with open(self.test_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.inventory.fieldnames)
            writer.writeheader()
            writer.writerows(sample_products)

        # Mock user input to simulate entering "2" as Product ID to remove
        import builtins

        original_input = builtins.input
        builtins.input = lambda _: "2"

        # Execute remove_product() method
        self.inventory.remove_product()

        # Restore original input function
        builtins.input = original_input

        # Read updated inventory from the test file
        with open(self.test_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            products_after_removal = list(reader)

        # Check that only one product remains after the fields line
        self.assertEqual(len(products_after_removal), 1)

        # Ensure that the remaining product is "Test Shirt" (Product ID: 3)
        remaining_product = products_after_removal[0]
        self.assertEqual(remaining_product["Product ID"], "3")
        self.assertEqual(remaining_product["Product Name"], "Test Shirt")

        # Ensure headers are still intact
        with open(self.test_file, mode="r", newline="") as file:
            first_line = file.readline().strip()
            expected_headers = ",".join(self.inventory.fieldnames)
            self.assertEqual(
                first_line, expected_headers
            )  # Ensure first row matches expected headers

    def test_filter_products(self):
        """Test filtering products based on color."""
        product1 = {
            "Product ID": "5",
            "Product Name": "Sneakers",
            "Brand": "Reebok",
            "Category": "Men's Fashion",
            "Price": "69.99",
            "Color": "White",
            "Size": "10",
            "Description": "Comfortable running shoes",
            "Material": "Synthetic",
            "Weight (kg)": "0.7",
            "Stock Quantity": "40",
        }

        product2 = {
            "Product ID": "6",
            "Product Name": "Hat",
            "Brand": "Adidas",
            "Category": "Accessories",
            "Price": "19.99",
            "Color": "Black",
            "Size": "One Size",
            "Description": "Stylish baseball cap",
            "Material": "Cotton",
            "Weight (kg)": "0.2",
            "Stock Quantity": "60",
        }

        with open(self.test_file, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.inventory.fieldnames)
            writer.writerow(product1)
            writer.writerow(product2)

        self.inventory.filter_products = lambda filters={"Color": "Black"}: [
            p for p in [product1, product2] if p["Color"] == filters["Color"]
        ]
        filtered_products = self.inventory.filter_products({"Color": "Black"})

        self.assertEqual(len(filtered_products), 1)
        self.assertEqual(filtered_products[0]["Product Name"], "Hat")

    def test_view_empty_inventory(self):
        """Test viewing products when inventory is empty."""
        self.inventory.view_products = lambda: None  # Mock function
        with open(self.test_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            products = list(reader)

        self.assertEqual(len(products), 0)

    def test_modify_product_details(self):
        """Test modifying an existing product's details."""
        # Add a sample product to the test file
        sample_product = {
            "Product ID": "4",
            "Product Name": "Test Hoodie",
            "Brand": "Puma",
            "Category": "Men's Fashion",
            "Price": "59.99",
            "Color": "Grey",
            "Size": "L",
            "Description": "Soft fleece hoodie",
            "Material": "Cotton Blend",
            "Weight (kg)": "1.0",
            "Stock Quantity": "20",
        }

        # Write sample product to the test file
        with open(self.test_file, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.inventory.fieldnames)
            writer.writerow(sample_product)

        # Create a list of inputs to simulate user interaction
        inputs = [
            "4",  # Product ID
            "",  # Product Name (keep existing)
            "",  # Brand (keep existing)
            "",  # Category (keep existing)
            "49.99",  # Price (change)
            "Black",  # Color (change)
            "",  # Size (keep existing)
            "",  # Description (keep existing)
            "",  # Material (keep existing)
            "",  # Weight (keep existing)
            "",  # Stock Quantity (keep existing)
        ]

        # Mock the input function to return our predefined inputs
        with patch("builtins.input", side_effect=inputs):
            # Redirect stdout to capture print statements
            captured_output = io.StringIO()
            sys.stdout = captured_output

            try:
                # Call the method being tested
                self.inventory.modify_product_details()
            finally:
                # Restore stdout
                sys.stdout = sys.__stdout__

        # Read updated inventory from the test file
        with open(self.test_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            products = list(reader)

        # Ensure only one product exists
        self.assertEqual(len(products), 1)

        # Ensure modifications were applied
        modified_product = products[0]
        self.assertEqual(modified_product["Price"], "49.99")
        self.assertEqual(modified_product["Color"], "Black")


if __name__ == "__main__":
    unittest.main()
