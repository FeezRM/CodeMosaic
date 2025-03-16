@echo off
REM Script: build_and_run.bat
REM Description: Build, run, and deploy the Fashion Inventory System.

echo Welcome to the Fashion Inventory System Setup!

REM Step 1: Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python from https://www.python.org/.
    pause
    exit /b
)

REM Step 2: Verify Python version
python --version
if %errorlevel% neq 0 (
    echo Unable to verify Python version. Please ensure Python is installed correctly.
    pause
    exit /b
)

REM Step 3: Install dependencies (if any)
echo Installing required dependencies...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo Failed to install dependencies. Please check your internet connection.
    pause
    exit /b
)

REM Step 4: Run the application
echo Starting the Fashion Inventory System...
python main.py

REM Step 5: End of script
echo Setup complete. Exiting...
pause