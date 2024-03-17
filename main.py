from user_interaction import UserInteraction
from database_manager import DatabaseManager


def main():
    # Create your database manager object with your own information
    db_manager = DatabaseManager(user='your_username', password='your_password',
                                 host='your_host', database='your_database')

    user_interaction = UserInteraction(db_manager)

    user_input = ""
    while user_input != "Quit":
        print_menu()

        user_input = input("What would you like to do?: ")
        print("\n \n")

        if user_input != "Quit":
            if user_input == "1":
                user_interaction.show_users_basic()
            elif user_input == "2":
                user_interaction.show_users_admin()
            elif user_input == "3":
                user_interaction.query_user_admin()
            elif user_input == "4":
                user_interaction.add_user()
            elif user_input == "5":
                user_interaction.delete_user()
            elif user_input == "6":
                user_interaction.update_password()
            else:
                print("I'm sorry, please enter a valid menu option.")

            print("\n \n")

    print("Program Closed.")


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


if __name__ == "__main__":
    main()