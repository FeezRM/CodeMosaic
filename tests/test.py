import pytest, csv, os
from login import *
from inventory import *

# temp login file for testing
@pytest.fixture
def temp_login_file(tmpdir):
    file_path = tmpdir.join("login_credentials.csv") # creates a temp file path

    with open(file_path, 'w') as file:
        file.write('Username,Password\n')
        file.write("test_admin,test_admin123\n")  
    return file_path # return for tests

# test if login file is created when it doesnt exist
def test_ensure_file_exists(temp_login_file):
    login = Login()
    assert os.path.exists(login.file_path)

# test adding a user who already exists
def test_add_login_user_already_exists(temp_login_file):
    login = Login("test_admin", "test_admin123")
    login.file_path = temp_login_file # points to temp file
    assert not login.add_login() # should return false because user exists

# test adding a new user
def test_add_login_new_user(temp_login_file):
    login = Login("user_test", "test_pass")
    login.file_path = temp_login_file
    assert login.add_login() # should return true because user is new

# test successful login
def test_check_login_success(temp_login_file):
    login = Login("test_admin", "test_admin123")
    login.file_path = temp_login_file
    assert login.check_login() # should return true as login is success

# test login failure with incorrect credentials
def test_check_login_fail(temp_login_file):
    login = Login("wrong_user", "wrong_pass")
    login.file_path = temp_login_file
    assert not login.check_login() # should return false as login fails

@pytest.fixture
def temp_inventory_file(tmpdir):
    file_path = tmpdir.join("fashion_inventory.csv") 

    with open(file_path, 'w') as file:
        file.write("Product ID,Product Name,Brand,Category,Price,Color,Size\n")
        file.write("1,Shirt,Nike,Men,20,Red,L\n") # test product
    return file_path 

def test_ensure_file_exists(temp_inventory_file):
    inventory = InventorySystem()
    assert os.path.exists(inventory.file_path)

def test_add_product(temp_inventory_file, monkeypatch): # monkeypatch is a tech to add/modify the behaviour of our code without changing the original source code
    inventory = InventorySystem()  
    inventory.file_path = temp_inventory_file  

    # simulate user input for adding a product using monkey patch
    monkeypatch.setattr("builtins.input", lambda _: "2 Pants Adidas Men 30 Blue M")
    inventory.add_product()  

    with open(temp_inventory_file, "r") as file:
        data = file.readlines()
    assert len(data) > 1  # should have more than just the header, like the product is added

def test_remove_product_exists(temp_inventory_file, monkeypatch):
    inventory = InventorySystem()  
    inventory.file_path = temp_inventory_file  

    monkeypatch.setattr("builtins.input", lambda _: "1")
    inventory.remove_product()  

    with open(temp_inventory_file, "r") as file:
        data = file.readlines()
    assert len(data) == 1  # only headers should remain, meaning product is removed 

def test_remove_product_not_found(temp_inventory_file, monkeypatch):
    """Test attempting to remove a non-existent product."""
    inventory = InventorySystem() 
    inventory.file_path = temp_inventory_file  

    monkeypatch.setattr("builtins.input", lambda _: "99")
    inventory.remove_product()  

    with open(temp_inventory_file, "r") as file:
        data = file.readlines()
    assert len(data) == 2  # inventory should remain unchanged, meaning product is not found



