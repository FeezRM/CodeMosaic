#!/bin/bash

# Script: build_and_run.sh
# Description: Build, run, and deploy the Fashion Inventory System.

echo "Welcome to the Fashion Inventory System Setup!"

# Step 1: Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed. Please install Python from https://www.python.org/"
    exit 1
fi

# Step 2: Verify Python version
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Unable to verify Python version. Please ensure Python is installed correctly."
    exit 1
fi

# Step 3: Install dependencies
echo "📦 Installing required dependencies..."
pip3 install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please check your internet connection."
    exit 1
fi

# Step 4: Run the application
echo "🚀 Starting the Fashion Inventory System..."
python3 main.py

# Step 5: End of script
echo "✅ Setup complete. Exiting..."