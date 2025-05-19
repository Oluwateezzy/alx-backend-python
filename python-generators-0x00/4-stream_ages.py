#!/usr/bin/python3
import mysql.connector
import sys


def stream_user_ages():
    """
    Generator that streams user ages one by one from the database
    Yields:
        int: User age
    """
    try:
        connection = mysql.connector.connect(
            host="localhost", user="root", password="", database="ALX_prodev"
        )
        cursor = connection.cursor()

        # Only select age column to minimize data transfer
        cursor.execute("SELECT age FROM user_data")

        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row[0]  # Yield just the age

    except mysql.connector.Error as err:
        print(f"Database error: {err}", file=sys.stderr)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals():
            connection.close()


def calculate_average_age():
    """
    Calculates average age using the streaming generator
    Returns:
        float: Average age of all users
    """
    total = 0
    count = 0

    # Single loop through all ages
    for age in stream_user_ages():
        total += age
        count += 1

    if count == 0:
        return 0.0  # Avoid division by zero

    return total / count


if __name__ == "__main__":
    average = calculate_average_age()
    print(f"Average age of users: {average:.2f}")
