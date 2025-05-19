import mysql.connector


def stream_users():
    """
    Generator function that streams rows from user_data table one by one
    Yields:
        dict: A dictionary representing a single user row
    """
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost", user="root", password="", database="ALX_prodev"
        )

        # Use a server-side cursor for efficient fetching
        cursor = connection.cursor(dictionary=True)

        # Execute the query
        cursor.execute("SELECT * FROM user_data")

        # Yield rows one by one
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        # Clean up resources
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals():
            connection.close()
