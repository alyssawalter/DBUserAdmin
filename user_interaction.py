import tabulate
import mysql.connector


class UserInteraction:
    def __init__(self, db):
        """
        Initialize the UserInteraction object.

        Args:
            db: DatabaseManager object used for database interaction.
        """
        self.db = db

    def show_users_basic(self):
        """
        Display basic information about users.

        Retrieves basic information about users from the database
        and displays it in tabular format using the tabulate library.

        Raises:
            mysql.connector.Error: If an error occurs while executing the SQL query.
        """
        self.db.connect()
        cursor = self.db.connection.cursor()
        try:
            cursor.execute("SELECT * FROM UserTableView")
            column_names = [i[0] for i in cursor.description]
            data = cursor.fetchall()
            print(tabulate.tabulate(data, headers=column_names))
        except mysql.connector.Error as err:
            print("Error occurred:", err)
        finally:
            cursor.close()
            self.db.disconnect()

    def show_users_admin(self):
        """
        Display detailed information about users (admin only).

        Retrieves detailed information about all users from the database
        and displays it in tabular format using the tabulate library.

        Raises:
            mysql.connector.Error: If an error occurs while executing the SQL query.
        """
        self.db.connect()
        cursor = self.db.connection.cursor()
        try:
            cursor.execute("SELECT * FROM UserTable")  # Query: Selecting all columns from the UserTable
            column_names = [i[0] for i in cursor.description]  # Getting the column names
            data = cursor.fetchall()  # Getting the data from the VIEW - UserTableView
            print(tabulate.tabulate(data, headers=column_names))  # Print the data in a table format using tabulate
        except mysql.connector.Error as err:
            print("Error occurred:", err)
        finally:
            cursor.close()
            self.db.disconnect()

    def query_user_admin(self):
        """
        Query detailed information about a specific user (admin only).

        Prompts the user to enter a username, then retrieves detailed
        information about that user from the database and displays it
        in tabular format using the tabulate library.

        Raises:
            mysql.connector.Error: If an error occurs while executing the SQL query.
        """
        print("Okay, let's find a user for you.")
        username = input("What is the username of the user you are searching for?: ")
        print("\nSearching...\n\n")

        self.db.connect()
        cursor = self.db.connection.cursor()

        user_query = "SELECT FirstName, LastName, UserName, AES_DECRYPT(Password, 'encryption_key'), JobTitle " \
                     "FROM UserTable WHERE UserName = %s"

        try:
            cursor.execute(user_query, (username,))  # Executing the query
            data = cursor.fetchall()  # Getting the data from the VIEW - UserTableView
            column_names = [i[0] for i in cursor.description]   # Getting the column names
            if len(data) == 0:
                print("\nSorry, there was no user found with that username.")
            else:
                print(tabulate.tabulate(data, headers=column_names))  # Print the data in a table format
        except mysql.connector.Error as err:
            print("Error occurred:", err)
        finally:
            cursor.close()
            self.db.disconnect()

    def _create_username(self, firstname: str, lastname: str) -> str:
        """
        Create a unique username for a new user.

        Generates a unique username based on the user's first name and last name.

        Args:
            firstname: The first name of the user.
            lastname: The last name of the user.

        Returns:
            A unique username for the new user.
        """
        attempt = firstname[0].lower() + lastname.lower()
        username = attempt

        self.db.connect()
        cursor = self.db.connection.cursor()
        try:
            i = 1
            while True:
                cursor.execute("SELECT COUNT(*) FROM UserTable WHERE Username = %s", (username,))
                # Ensure that the username is unique
                matches = cursor.fetchone()[0]
                if matches == 0:
                    break
                # If there is a match, add a number to the end and test for matches again
                username += str(i)
                i += 1
        except mysql.connector.Error as err:
            print("Error occurred while creating username:", err)
        finally:
            cursor.close()
            self.db.disconnect()
        return username

    def add_user(self):
        """
        Add a new user to the database.

        Prompts the user to enter details for a new user (first name, last name,
        job title, and password), generates a unique username, and adds the
        user to the database.

        Raises:
            mysql.connector.Error: If an error occurs while executing the SQL query.
        """
        print("Okay, let's add a new user!\nPlease input the following information.")

        firstname = input("First Name: ")
        lastname = input("Last Name: ")
        jobtitle = input("Job Title: ")
        password = input("New Password: ")
        print("\nChecking for a valid username...")

        username = self._create_username(firstname, lastname)
        print("\nHere is a unique username for " + firstname + ": " + username)

        self.db.connect()
        cursor = self.db.connection.cursor()

        # Query to insert the new user into UserTable
        insert_query = "INSERT INTO UserTable (FirstName, LastName, UserName, Password, JobTitle) " \
                       "VALUES (%s, %s, %s, AES_ENCRYPT(%s, 'encryption_key'), %s)"
        try:
            # Executing the query
            cursor.execute(insert_query, (firstname, lastname, username, password, jobtitle))
            self.db.connection.commit()
            print("\nThis user has successfully been added.")
        except mysql.connector.Error as err:
            print("\nEmployee not added.")
            print("Error: {}".format(err))
        finally:
            cursor.close()
            self.db.disconnect()

    def _user_exists(self, username: str) -> bool:
        """
        Checks if a user with the specified username exists in the database.

        Args:
            username: The username to check.

        Returns:
            True if the user exists, False otherwise.
        """
        self.db.connect()
        cursor = self.db.connection.cursor()

        # Query: Selecting specific username from the UserTable
        user_query = "SELECT UserName FROM UserTable WHERE UserName = %s;"

        try:
            # Execute query and fetch data
            cursor.execute(user_query, (username,))
            data = cursor.fetchall()
        except self.db.connector.Error as err:
            print(f"Error in query searching for username: {err}")
        else:
            if len(data) == 0:
                return False
            else:
                return True
        finally:
            cursor.close()
            self.db.disconnect()

    def delete_user(self):
        """
        Delete a user from the database.

        Prompts the user to enter the username of the user to delete,
        verifies the username, and deletes the user from the database.

        Raises:
            mysql.connector.Error: If an error occurs while executing the SQL query.
        """
        print("Okay, let's delete a user.")
        username = input("What user would you like to delete?\nUsername: ")

        # Check to make sure the username exists in the table
        if self._user_exists(username) is True:
            # Double check they want to delete a user from the table
            confirm = (input("Are you sure you want to delete this user?\n(Y) or (N): ")).lower()
            if confirm == 'y':
                # Query to delete the user specified
                delete_query = "DELETE FROM UserTable WHERE Username = %s;"

                self.db.connect()
                user_cursor = self.db.connection.cursor()

                try:
                    # Execute the query
                    user_cursor.execute(delete_query, (username,))
                    self.db.connection.commit()
                    print("\nThe user has been successfully deleted.\n")
                except self.db.connector.Error as err:
                    print("Error deleting user:", err)
                finally:
                    user_cursor.close()
                    self.db.disconnect()
            else:
                print("\nOkay, we'll go back to the main menu.\n")  # Cancel deletion process
        else:
            print("\nError. Username does not exist.\n")

    def _check_password(self, username: str, cur_pass: str) -> bool:
        """
        Checks if the entered password matches the current password
        for the specified user in the database.

        Args:
            username: The username of the user.
            cur_pass: The entered password.

        Returns:
            True if the entered password matches the current password,
            False otherwise.
        """
        self.db.connect()
        cursor = self.db.connection.cursor()

        # Query to confirm the user's current password
        select_query = "SELECT AES_DECRYPT(Password, 'encryption_key') FROM UserTable WHERE UserName = %s;"

        try:
            # Executing the query
            cursor.execute(select_query, (username,))
            result = (cursor.fetchone()[0]).decode('utf-8')
        except self.db.connector.Error as err:
            print("Error checking password:", err)
        else:
            # Make sure the correct password for the user was entered
            if result is not None and cur_pass == result:
                return True
            else:
                return False
        finally:
            cursor.close()
            self.db.disconnect()

    def update_password(self):
        """
         Update a user's password in the database.

        Prompts the user to enter the username and current password
        for the user whose password should be updated, verifies the
        current password, and updates the password in the database.

        Raises:
            mysql.connector.Error: If an error occurs while executing the SQL query.
        """
        print("Okay, let's update a password!")
        username = input("What user would you like to change a password for?\nUsername: ")
        cur_pass = input("Current Password: ")

        still_attempting = True

        while still_attempting:
            # The old password must be entered before changing it
            if self._check_password(username, cur_pass) is True:
                new_pass = input("New Password: ")

                self.db.connect()
                cursor = self.db.connection.cursor()

                # Query to update the password for the user specified
                update_query = "UPDATE UserTable SET password = AES_ENCRYPT(%s, 'encryption_key') WHERE Username = %s;"

                try:
                    # Execute query
                    cursor.execute(update_query, (new_pass, username,))
                    self.db.connection.commit()
                    print("\nThe password has been successfully updated.")
                except self.db.connector.Error as err:
                    print("Error updating password:", err)
                finally:
                    still_attempting = False  # Password was changed or there was an error that prevented the change
                    cursor.close()
                    self.db.disconnect()
            else:
                print("\nError. Password given does not match current password."
                      "\nTry again or type 'BACK' to go back.")
                cur_pass = input("Current Password: ")
                if cur_pass == 'BACK':
                    still_attempting = False
