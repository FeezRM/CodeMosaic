#!/bin/bash
echo "Setting up Fashion Inventory System..."

# Install dependencies
pip install django

# Run migrations
python manage.py migrate

echo ""
echo "Setup complete!"
echo ""
echo "To run the application:"
echo "   python manage.py runserver"
echo ""
echo "Create admin account:"
echo "   python manage.py createsuperuser"
echo ""