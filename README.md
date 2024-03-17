# Database User Administration System

This project is a simple database user administration system implemented in Python using MySQL as the database backend. It provides a command-line interface for performing basic CRUD operations such as displaying user information, adding new users, deleting users, and updating passwords.
The application incorporates robust security measures, including AES encryption for storing passwords and the use of parameterized queries to prevent SQL injection attacks.

## Features
- View basic user information
- Admin-level access to view all users
- Query specific user details
- Add new users with unique usernames
- Delete existing users
- Update user passwords

## Usage
### Prerequisites
- Python 3.x
- MySQL database

### Installation
1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/alyssawalter/DBUserAdmin.git
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Update the database connection details in the `main.py` file:
   ```python
   db_manager = DatabaseManager(user='your_username', password='your_password', host='your_host', database='your_database')
   ```
### Running the Tool
Navigate to the project directory and run main.py:
```bash
python3 main.py
```

## File Structure
- `main.py`: Main script to run the user interaction loop.
- `database_manager.py`: Class for managing database connections.
- `user_interaction.py`: Class containing methods for user interactions and database operations.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License
This project is not licensed.
