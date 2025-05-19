import csv
import uuid
import mysql.connector
from mysql.connector import errorcode


def connect_db():
    """Connect to the MySQL server"""
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None


def create_database(connection):
    """Create the ALX_prodev database if it doesn't exist"""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        return False
    finally:
        cursor.close()
    return True


def connect_to_prodev():
    """Connect to the ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host="localhost", user="root", password="", database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None


def create_table(connection):
    """Create the user_data table if it doesn't exist"""
    cursor = connection.cursor()
    table_description = (
        "CREATE TABLE IF NOT EXISTS `user_data` ("
        "  `user_id` VARCHAR(36) PRIMARY KEY,"
        "  `name` VARCHAR(255) NOT NULL,"
        "  `email` VARCHAR(255) NOT NULL,"
        "  `age` DECIMAL(10,0) NOT NULL,"
        "  INDEX `idx_user_id` (`user_id`)"
        ") ENGINE=InnoDB"
    )
    try:
        cursor.execute(table_description)
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table already exists.")
        else:
            print(f"Failed creating table: {err}")
        return False
    finally:
        cursor.close()
    return True


def insert_data(connection, csv_file):
    """Insert data from CSV file into the database"""
    cursor = connection.cursor()
    try:
        with open(csv_file, mode="r") as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                # Check if user_id already exists
                cursor.execute(
                    "SELECT user_id FROM user_data WHERE user_id = %s",
                    (row["user_id"],),
                )
                if cursor.fetchone() is None:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) "
                        "VALUES (%s, %s, %s, %s)",
                        (row["user_id"], row["name"], row["email"], int(row["age"])),
                    )
        connection.commit()
        print(f"Data inserted successfully from {csv_file}")
    except Exception as err:
        print(f"Error inserting data: {err}")
        return False
    finally:
        cursor.close()
    return True


def stream_rows(connection, batch_size=1):
    """
    Generator that streams rows from the user_data table one by one
    Args:
        connection: MySQL database connection
        batch_size: Number of rows to fetch at a time (default 1)
    Yields:
        dict: A dictionary representing a single row
    """
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM user_data")
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            for row in rows:
                yield row
    finally:
        cursor.close()
