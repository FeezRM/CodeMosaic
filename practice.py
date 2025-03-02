from login import Login

user = Login('ebaad', 'ebaad00192')  # Provide required arguments

user.add_login()

if user.check_login():  # Correctly call the function
    print('Success')
else:
    print('false')


user = Login('ebaad888', 'ebaad00192')  # Provide required arguments

user.add_login()

if user.check_login():  # Correctly call the function
    print('Success')
else:
    print('false')

