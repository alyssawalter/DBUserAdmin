import mysql.connector
from mysql.connector import errorcode
import tabulate

"""
FUNCTION to print the main menu - used in main loop. 
"""
def print_menu():

    menu = "Please Enter 1, 2, 3, 4, 5, 6, or Quit.\n" \
           "1 - Show Users (basic)\n" \
           "2 - Show All Users (admin)\n" \
           "3 - Query One User (admin)\n" \
           "4 - Add New User\n" \
           "5 - Delete User\n" \
           "6 - Update User Password\n" \
           "Quit - Close the Program\n"

    print(menu)

"""
OPTION 1 FUNCTION: Show Users (Basic)
"""
def show_users_basic():

    """
    ESTABLISH CONNECTION TO DATABASE
    """
    try:
        cm_connection = mysql.connector.connect(
            user='CS509',
            password='CS509',
            host='127.0.0.1',
            database='demo509'
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid credentials")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            print("Cannot connect to database: ", err)

    else:
        # Operation 1: Display all users - form the query, execute the query, print results
        user_cursor = cm_connection.cursor()
        user_query = "SELECT * FROM UserTableView"  # Query: Selecting all columns from the UserTableView

        user_cursor.execute(user_query)  # Executing the query

        # Getting the column names
        column_names = [i[0] for i in user_cursor.description]

        # Getting the data from the VIEW - UserTableView
        data = user_cursor.fetchall()

        # Print the data in a table format using tabulate import
        print(tabulate.tabulate(data, headers=column_names))

        user_cursor.close()

    cm_connection.close()  # Last line of function



"""
OPTION 2 FUNCTION: Show Users (Admin)
"""
def show_users_admin():
    user_query = "SELECT * FROM UserTable"  # Query: Selecting all columns from the UserTable

    """
    ESTABLISH CONNECTION TO DATABASE
    """
    try:
        cm_connection = mysql.connector.connect(
            user='CS509',
            password='CS509',
            host='127.0.0.1',
            database='demo509'
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid credentials")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            print("Cannot connect to database: ", err)

    else:
        # Operation 2: Display all users, admin
        user_cursor = cm_connection.cursor()

        user_cursor.execute(user_query)  # Executing the query

        # Getting the column names
        column_names = [i[0] for i in user_cursor.description]

        # Getting the data from the VIEW - UserTableView
        data = user_cursor.fetchall()

        # Print the data in a table format using tabulate import
        print(tabulate.tabulate(data, headers=column_names))

        user_cursor.close()

    cm_connection.close()  # Last line of function



"""
OPTION 3 FUNCTION: Query One User (admin)
"""
def query_user_admin():

    print("Okay, let's find a user for you.")
    username = input("What is the username of the user you are searching for?: ")
    print("\nSearching...\n\n")

    # Query: Selecting all columns from the UserTable
    user_query = "SELECT FirstName, LastName, UserName, AES_DECRYPT(Password, 'encryption_key'), "
    user_query += "JobTitle FROM UserTable WHERE UserName = '"+username+"';"

    """
    ESTABLISH CONNECTION TO DATABASE
    """
    try:
        cm_connection = mysql.connector.connect(
            user='CS509',
            password='CS509',
            host='127.0.0.1',
            database='demo509'
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid credentials")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            print("Cannot connect to database: ", err)

    else:
        # Operation 3: Display one user, admin
        user_cursor = cm_connection.cursor()

        try:
            user_cursor.execute(user_query)  # Executing the query

        except mysql.connector.Error as err:
            print(f"Error in query: (err)")

        else:
            # Getting the column names
            column_names = [i[0] for i in user_cursor.description]

            # Getting the data from the VIEW - UserTableView
            data = user_cursor.fetchall()

            if len(data) == 0:
                print("\nSorry, there was no user found with that username.")
                return
            else:

                # Print the data in a table format using tabulate import
                print(tabulate.tabulate(data, headers=column_names))

            user_cursor.close()
            cm_connection.close()

"""
FUNCTION used in OPTION 4 - ADD USER: creates unique username 
"""
def create_username(firstname: str, lastname: str) -> str:
    attempt = firstname[0].lower() + lastname.lower()
    username = attempt

    try:
        cm_connection = mysql.connector.connect(
            user='CS509',
            password='CS509',
            host='127.0.0.1',
            database='demo509'
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid credentials")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            print("Cannot connect to database: ", err)

    else:
        user_cursor = cm_connection.cursor()

        i = 1
        while True:
            user_cursor.execute("SELECT COUNT(*) FROM UserTable WHERE Username = %s", (username,))
            matches = user_cursor.fetchone()[0]
            if matches == 0:
                user_cursor.close()
                cm_connection.close()
                break
            username += str(i)
            i += 1

        user_cursor.close()
        cm_connection.close()
        return username

"""
OPTION 4 FUNCTION: Add New User 
"""
def add_user():

    """
    ESTABLISH CONNECTION TO DATABASE
    """
    try:
        cm_connection = mysql.connector.connect(
            user='CS509',
            password='CS509',
            host='127.0.0.1',
            database='demo509'
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid credentials")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            print("Cannot connect to database: ", err)

    else:
        print("Okay, let's add a new user!\nPlease input the following information.")

        firstname = input("First Name: ")
        lastname = input("Last Name: ")
        jobtitle = input("Job Title: ")
        password = input("New Password: ")

        print("\nChecking for a valid username...")
        username = create_username(firstname, lastname)

        print("\nHere is a unique username for " + firstname + ": " + username)

        # Query to insert the new user into UserTable
        insert_query = "INSERT INTO UserTable (FirstName, LastName, UserName, Password, JobTitle) "
        insert_query += "VALUES (%s, %s, %s, AES_ENCRYPT(%s, 'encryption_key'), %s)"

        try:
            user_cursor = cm_connection.cursor()
            # Executing the query
            user_cursor.execute(insert_query, (firstname, lastname, username, password, jobtitle))
            cm_connection.commit()
            print("\nThis user has successfully been added.")
            user_cursor.close()
        except mysql.connector.Error as err:
            print("\nEmployee not added.")
            print("Error: {}".format(err))
        cm_connection.close()

"""
FUNCTION used in OPTION 5 - DELETE USER: checks to make sure there is a user with given username
"""
def user_exists(username: str) -> bool:
    # Query: Selecting specific username from the UserTable
    user_query = "SELECT UserName FROM UserTable WHERE UserName = %s;"

    """
    ESTABLISH CONNECTION TO DATABASE
    """
    try:
        cm_connection = mysql.connector.connect(
            user='CS509',
            password='CS509',
            host='127.0.0.1',
            database='demo509'
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid credentials")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            print("Cannot connect to database: ", err)

    else:
        user_cursor = cm_connection.cursor()

        try:
            user_cursor.execute(user_query, (username,))

        except mysql.connector.Error as err:
            print(f"Error in query: (err)")

        else:
            data = user_cursor.fetchall()

            if len(data) == 0:
                user_cursor.close()
                cm_connection.close()
                return False
            else:
                user_cursor.close()
                cm_connection.close()
                return True



"""
OPTION 5 FUNCTION: Delete User
"""
def delete_user():
    """
    ESTABLISH CONNECTION TO DATABASE
    """
    try:
        cm_connection = mysql.connector.connect(
            user='CS509',
            password='CS509',
            host='127.0.0.1',
            database='demo509'
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid credentials")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            print("Cannot connect to database: ", err)

    else:
        print("Okay, let's delete a user.")
        username = input("What user would you like to delete?\nUsername: ")

        if user_exists(username) is True:
            confirm = (input("Are you sure you want to delete this user?\n(Y) or (N): ")).lower()

            if confirm == 'y':
                # Query to delete the user specified
                delete_query = "DELETE FROM UserTable WHERE Username = %s;"

                user_cursor = cm_connection.cursor()

                user_cursor.execute(delete_query, (username,))
                cm_connection.commit()

                print("\nThe user has been successfully deleted.\n")
                user_cursor.close()
                cm_connection.close()
            else:
                print("\nOkay, we'll go back to the main menu.\n")
        else:
            print("\nError. Username does not exist.\n")


"""
FUNCTION used in OPTION 6 - UPDATE PASSWORD: Checks to make sure given password is same as current password
"""
def check_password(username: str, cur_pass: str) ->bool:
    """
    ESTABLISH CONNECTION TO DATABASE
    """
    try:
        cm_connection = mysql.connector.connect(
            user='CS509',
            password='CS509',
            host='127.0.0.1',
            database='demo509'
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid credentials")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            print("Cannot connect to database: ", err)

    else:
        # Query to confirm the user's current password
        select_query = "SELECT AES_DECRYPT(Password, 'encryption_key') FROM UserTable WHERE UserName = %s;"

        user_cursor = cm_connection.cursor()

        # Executing the query
        user_cursor.execute(select_query, (username,))

        result = (user_cursor.fetchone()[0]).decode('utf-8')

        if result is not None and cur_pass == result:
            user_cursor.close()
            cm_connection.close()
            return True
        else:
            user_cursor.close()
            cm_connection.close()
            return False


"""
OPTION 6 FUNCTION: Update Password
"""
def update_password():

    """
    ESTABLISH CONNECTION TO DATABASE
    """
    try:
        cm_connection = mysql.connector.connect(
            user='CS509',
            password='CS509',
            host='127.0.0.1',
            database='demo509'
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid credentials")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            print("Cannot connect to database: ", err)

    else:
        print("Okay, let's update a password!")
        username = input("What user would you like to change a password for?\nUsername: ")

        cur_pass = input("Current Password: ")
        if check_password(username, cur_pass) is True:
            new_pass = input("New Password: ")

            # Query to update the password for the user specified
            update_query = "UPDATE UserTable SET password = AES_ENCRYPT(%s, 'encryption_key') WHERE Username = %s;"

            user_cursor = cm_connection.cursor()

            user_cursor.execute(update_query, (new_pass, username,))
            cm_connection.commit()

            print("\nThe password has been successfully updated.")
            user_cursor.close()
            cm_connection.close()
        else:
            print("\nError. Password given does not match current password.")


"""
MAIN LOOP FOR INTERACTING WITH USERS
"""

# initializing variable to contain user input
user_input = ""
print_menu()

# Creating a while loop to continue program use until the user quits
while user_input != "Quit":

    user_input = input("What would you like to do?: ")
    print("\n \n")

    if user_input != "Quit":
        if user_input == "1":
            show_users_basic()
        elif user_input == "2":
            show_users_admin()
        elif user_input == "3":
            query_user_admin()
        elif user_input == "4":
            add_user()
        elif user_input == "5":
            delete_user()
        elif user_input == "6":
            update_password()
        else:
            print("I'm sorry, please enter a valid menu option.")

        print("\n \n")
        print_menu()

print("Program Closed.")
