#!/bin/bash
echo "Setting up Fashion Inventory System..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

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