import time
import sqlite3
import functools


def with_db_connection(func):
    """Decorator that automatically handles database connections"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()

    return wrapper


def retry_on_failure(retries=3, delay=2):
    """Decorator that retries database operations on failure"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except (sqlite3.OperationalError, sqlite3.DatabaseError) as e:
                    last_exception = e
                    if attempt < retries:
                        time.sleep(delay)
                        continue
                    raise last_exception

        return wrapper

    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
