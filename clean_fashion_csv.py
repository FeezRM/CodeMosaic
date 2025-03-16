import pandas as pd

# Load the CSV file
file_path = "csv_files/fashion_products.csv"  # Update with your file path
df = pd.read_csv(file_path)

# Keep only the required columns
df = df[
    [
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
]

# Save the modified CSV file
df.to_csv("fashion_inventory.csv", index=False)

print("CSV file has been updated successfully!")
