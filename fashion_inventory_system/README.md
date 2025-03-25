# Fashion Inventory System

## Prerequisites

- Python 3.8+
- pip
- SQLite (included with Python)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fashion-inventory-system.git
   cd fashion-inventory-system

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3. Install dependencies:    
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser(admin account):
    ```bash
    python manage.py createsuperuser
    ```

6. Start the development server:
    ```bash
    python manage.py runserver
    ```

Then open http://localhost:8000 in your browser.