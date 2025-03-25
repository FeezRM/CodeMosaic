@echo off
echo Setting up Fashion Inventory System...

:: Create virtual environment
python -m venv venv
call venv\Scripts\activate

:: Install dependencies
pip install -r requirements.txt

:: Run migrations
python manage.py migrate

echo.
echo Setup complete!
echo.
echo To run the application:
echo    python manage.py runserver
echo.
echo Create admin account:
echo    python manage.py createsuperuser
echo.
pause