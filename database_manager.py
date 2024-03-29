import mysql.connector
from mysql.connector import errorcode


class DatabaseManager:
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.database
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Invalid credentials")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database not found")
            else:

                print("Cannot connect to database: ", err)

    def disconnect(self):
        if self.connection:
            self.connection.close()
