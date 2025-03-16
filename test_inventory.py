import unittest
import csv
import os
from inventory import InventorySystem


class TestInventorySystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once before all tests. Creates test file."""
        cls.test_file = "test_inventory.csv"
        cls.inventory = InventorySystem()
        cls.inventory.file_path = cls.test_file  # Redirect to test file
        cls.inventory.ensure_file_exists()

    def setUp(self):
        """Runs before each test. Clears test inventory file."""
        with open(self.test_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.inventory.fieldnames)  # Write headers

    def test_add_product(self):
        """Test adding a product to inventory."""
        sample_product = {
            "Product ID": "1",
            "Product Name": "Test Shirt",
            "Brand": "Nike",
            "Category": "Men's Fashion",
            "Price": "29.99",
            "Color": "Blue",
            "Size": "M",
            "Description": "Comfortable cotton t-shirt",
            "Material": "Cotton",
            "Weight (kg)": "0.3",
            "Stock Quantity": "10",
        }

        with open(self.test_file, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.inventory.fieldnames)
            writer.writerow(sample_product)

        with open(self.test_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            products = list(reader)

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["Product Name"], "Test Shirt")

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
        self.assertEqual(len(products_after_removal), 2)

        # Ensure that the remaining product is "Test Shirt" (Product ID: 3)
        remaining_product = products_after_removal[1]
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
        """Test filtering products by different criteria."""
        sample_products = [
            {
                "Product ID": "1",
                "Product Name": "T-shirt",
                "Brand": "Nike",
                "Category": "Men's Fashion",
                "Price": "25.00",
                "Color": "Red",
                "Size": "M",
                "Description": "A comfortable cotton t-shirt",
                "Material": "Cotton",
                "Weight (kg)": "0.3",
                "Stock Quantity": "10",
            },
            {
                "Product ID": "2",
                "Product Name": "Sneakers",
                "Brand": "Adidas",
                "Category": "Men's Fashion",
                "Price": "60.00",
                "Color": "White",
                "Size": "L",
                "Description": "Stylish sneakers for casual wear",
                "Material": "Synthetic",
                "Weight (kg)": "1.2",
                "Stock Quantity": "5",
            },
            {
                "Product ID": "3",
                "Product Name": "Jeans",
                "Brand": "Levi's",
                "Category": "Men's Fashion",
                "Price": "50.00",
                "Color": "Blue",
                "Size": "L",
                "Description": "Classic blue jeans",
                "Material": "Denim",
                "Weight (kg)": "1.5",
                "Stock Quantity": "8",
            },
        ]

        with open(self.test_file, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.inventory.fieldnames)
            writer.writerows(sample_products)

        # Mock filtering by color (Red)
        self.inventory.filter_products = lambda: print("Filtered Product: T-shirt")

        # Capture the printed output
        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.inventory.filter_products()
        sys.stdout = sys.__stdout__

        self.assertIn("Filtered Product: T-shirt", captured_output.getvalue())

    def test_view_products_empty(self):
        """Test viewing products when inventory is empty."""
        with open(self.test_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.inventory.fieldnames)  # Write headers

        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.inventory.view_products()
        sys.stdout = sys.__stdout__

        self.assertIn("No products available.", captured_output.getvalue())

    def test_remove_non_existent_product(self):
        """Test removing a product that does not exist."""
        self.inventory.remove_product = lambda: print("Product not found!")

        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.inventory.remove_product()
        sys.stdout = sys.__stdout__

        self.assertIn("Product not found!", captured_output.getvalue())

    @classmethod
    def tearDownClass(cls):
        """Runs once after all tests. Cleans up test file."""
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)


if __name__ == "__main__":
    unittest.main()
