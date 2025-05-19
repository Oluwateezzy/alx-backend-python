import mysql.connector
import sys


def stream_users_in_batches(batch_size):
    """Stream users in batches from database"""
    try:
        with mysql.connector.connect(
            host="localhost", user="root", password="", database="ALX_prodev"
        ) as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM user_data")
                while batch := cursor.fetchmany(batch_size):
                    yield batch
    except mysql.connector.Error as err:
        print(f"Database error: {err}", file=sys.stderr)


def batch_processing(batch_size):
    """Yield users over 25 from batched stream"""
    for batch in stream_users_in_batches(batch_size):
        yield from (user for user in batch if user["age"] > 25)
