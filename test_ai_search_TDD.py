import unittest
import os
import csv
from inventory import InventorySystem
from unittest.mock import patch

class TestAISearchRecommendation(unittest.TestCase):

    def setUp(self):
        """Set up test environment before each test"""
        self.inventory = InventorySystem()
        self.inventory.file_path = "test_fashion_inventory.csv"
        self.inventory.ensure_file_exists()

        self.sample_products = [
            {"Product ID": "101", "Product Name": "Running Shoes", "Brand": "Nike"},
            {"Product ID": "102", "Product Name": "Basketball Sneakers", "Brand": "Adidas"},
            {"Product ID": "103", "Product Name": "Casual Loafers", "Brand": "Puma"}
        ]

        with open(self.inventory.file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.inventory.fieldnames)
            writer.writerows(self.sample_products)

    def tearDown(self):
        """Clean up test file after each test"""
        if os.path.exists(self.inventory.file_path):
            os.remove(self.inventory.file_path)

    def test_ai_suggestion_exact_match(self):
        """Test AI recommendation when the search term exactly matches a product"""
        recommendations = self.inventory.ai_search_recommendation("Running Shoes")
        self.assertEqual(recommendations, ["Running Shoes"])

    def test_ai_suggestion_typo(self):
        """Test AI recommendation when there is a minor typo in the search query"""
        recommendations = self.inventory.ai_search_recommendation("Runing Shoes")
        self.assertIn("Running Shoes", recommendations)

    def test_ai_suggestion_partial_match(self):
        """Test AI recommendation for a partial word match"""
        recommendations = self.inventory.ai_search_recommendation("Sneakers")
        self.assertIn("Basketball Sneakers", recommendations)

    def test_ai_suggestion_no_match(self):
        """Test AI recommendation when there are no close matches"""
        recommendations = self.inventory.ai_search_recommendation("Leather Boots")
        self.assertEqual(recommendations, [])

if __name__ == "__main__":
    unittest.main()