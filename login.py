import csv
import os


class Login:
    def __init__(self, username="", password=""):
        self.username = username.strip()
        self.password = password.strip()
        self.file_path = "csv_files/login_credentials.csv"
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Username", "Password"])

    def add_login(self):
        if self.check_login():
            print("❌ User already exists!")
            return False

        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.username, self.password])
        print("✅ User registered successfully!")
        return True

    def check_login(self):
        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if row and len(row) == 2:
                        stored_username, stored_password = row
                        if (
                            stored_username.strip() == self.username
                            and stored_password.strip() == self.password
                        ):
                            return True
        except FileNotFoundError:
            return False
        return False
