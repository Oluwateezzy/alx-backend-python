from datetime import datetime
import sqlite3
import functools


#### decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from either args or kwargs
        query = kwargs.get("query", None)
        if query is None and len(args) > 0:
            query = args[0]

        # Log the query with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Executing SQL query: {query}")

        # Call the original function
        return func(*args, **kwargs)

    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
