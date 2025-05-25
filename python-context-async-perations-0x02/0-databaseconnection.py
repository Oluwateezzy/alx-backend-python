import sqlite3  # Using SQLite for this example, but can be adapted for other DBs


class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # Open the database connection
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        # Handle any exceptions that might have occurred
        if exc_type is not None:
            print(f"An error occurred: {exc_val}")
        return True
