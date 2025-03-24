import csv
import os
from inventory import InventorySystem
from login import Login


class App:
    def __init__(self):
        self.authenticated = False
        self.inventory = InventorySystem()

    def authenticate(self):
        while not self.authenticated:
            print("\n🔐 Authentication Menu")
            print("1️⃣ Login")
            print("2️⃣ Register")
            print("3️⃣ Guest Mode")
            print("4️⃣ Exit")
            choice = input("➡️  Select an option: ")

            if choice == "1":
                username = input("👤 Enter Username: ")
                password = input("🔑 Enter Password: ")
                user = Login(username, password)

                if user.check_login():
                    print("✅ Login successful!")
                    self.authenticated = True
                    return
                else:
                    print("❌ Invalid credentials. Try again.")

            elif choice == "2":
                username = input("👤 Choose a Username: ")
                password = input("🔑 Choose a Password: ")
                user = Login(username, password)

                if user.add_login():
                    print("✅ Registration successful! You can now log in.")
                else:
                    print("❌ Registration failed. User may already exist.")

            elif choice == "3":
                print("\n👤 Guest Mode Activated: You can only view products.")
                self.authenticated = "guest"
                return

            elif choice == "4":
                print("👋 Exiting system...")
                exit()
            else:
                print("❌ Invalid choice. Try again.")

    def run(self):
        print("🛍️ Welcome to the Fashion Inventory System!")
        self.authenticate()

        while True:
            print("\n📋 Main Menu")
            print("1️⃣ View Products")
            print("2️⃣ Filter Products")

            if self.authenticated != "guest":
                print("3️⃣ Add Product")
                print("4️⃣ Remove Product")
                print("5️⃣ Modify Product Details")

            print("6️⃣ Exit")

            choice = input("\n➡️  Select an option: ")

            if choice == "1":
                self.inventory.view_products()
            elif choice == "2":
                self.inventory.filter_products()
            elif choice == "3" and self.authenticated != "guest":
                self.inventory.add_product()
            elif choice == "4" and self.authenticated != "guest":
                self.inventory.remove_product()
            elif choice == "5" and self.authenticated != "guest":
                self.inventory.modify_product_details()
            elif choice == "6":
                print("👋 Exiting system...\n")
                break
            else:
                print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    app = App()
    app.run()
