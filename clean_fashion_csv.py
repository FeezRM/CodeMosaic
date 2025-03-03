import pandas as pd

# Load the CSV file
file_path = "fashion_products.csv"  # Update with your file path
df = pd.read_csv(file_path)

# Keep only the required columns
df = df[["Product Name", "Brand", "Category", "Price", "Color", "Size"]]

# Save the modified CSV file
df.to_csv("fashion_inventory.csv", index=False)

print("CSV file has been updated successfully!")
