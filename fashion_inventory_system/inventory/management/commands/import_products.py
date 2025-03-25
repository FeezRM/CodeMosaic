from django.core.management.base import BaseCommand
from inventory.models import Product
import csv
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Imports products from CSV file'

    def handle(self, *args, **options):
        # Path to your CSV file
        csv_file = os.path.join(settings.BASE_DIR, 'inventory', 'data', 'fashion_inventory.csv')
        
        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f'CSV file not found at {csv_file}'))
            return

        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Use update_or_create to handle existing products
                Product.objects.update_or_create(
                    product_id=row['Product ID'],
                    defaults={
                        'name': row['Product Name'],
                        'brand': row['Brand'],
                        'category': row['Category'],
                        'price': row['Price'],
                        'color': row['Color'],
                        'size': row['Size'],
                        'description': row['Description'],
                        'material': row['Material'],
                        'weight': row['Weight (kg)'],
                        'stock_quantity': row['Stock Quantity'],
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported/updated products'))