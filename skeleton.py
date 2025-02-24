class InventorySystem:
    def __init__(self):
        self.authenticated = False
        self.products = []

    def authenticate(self, username, password):
        USER_NAME = "admin"
        PASSWORD = "OTU2025"
        if username == USER_NAME and password == PASSWORD:
            print("Login successful!")
            self.authenticated = True
        else:
            print("Invalid credentials")

    def add_product(self):
        name = input("Enter Product Name: ")
        category = input("Enter Category: ")
        price = input("Enter Price: ")
        stock = input("Enter Stock Quantity: ")

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            print("Invalid input. Price must be a number and stock must be an integer.")
            return

        product = {"name": name, "category": category, "price": price, "stock": stock}
        self.products.append(product)
        print("Product added successfully!")

    def remove_product(self):
        name = input("Enter Product Name to Remove: ")
        for product in self.products:
            if product["name"] == name:
                self.products.remove(product)
                print("Product removed successfully!")
                return
        print("Product not found.")

    def view_products(self):
        if not self.products:
            print("No products available.")
            return
        print("\nProduct Inventory:")
        for product in self.products:
            print(
                f"Name: {product['name']}, Category: {product['category']}, Price: {product['price']}, Stock: {product['stock']}"
            )

    def main(self):
        print("Welcome to Inventory Management System")
        while not self.authenticated:
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            self.authenticate(username, password)

        while True:
            print("\n1. Add Product")
            print("2. Remove Product")
            print("3. View Products")
            print("4. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                self.add_product()
            elif choice == "2":
                self.remove_product()
            elif choice == "3":
                self.view_products()
            elif choice == "4":
                print("Exiting...\n")
                break
            else:
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    system = InventorySystem()
    system.main()
