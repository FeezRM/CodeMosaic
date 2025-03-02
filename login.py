import csv
import os

class Login:
    def __init__(self, username="", password=""):
        self.username = username
        self.password = password

    def add_login(self):
        file_exists = os.path.exists('login_credentials.csv')
        
        # Check if the credentials already exist
        if self.check_login():
            print("User already exists!")
            return

        # Open the file in append mode, create it if it doesn't exist
        with open('login_credentials.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Write a header if the file is new or empty
            if not file_exists or os.stat('login_credentials.csv').st_size == 0:
                writer.writerow(["Username", "Password"])
            
            writer.writerow([self.username, self.password])
            print("User added successfully!")

    def check_login(self):
        try:
            with open('login_credentials.csv', mode='r') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header row
                for row in reader:
                    if row == [self.username, self.password]:
                        return True
        except FileNotFoundError:
            return False
        return False
