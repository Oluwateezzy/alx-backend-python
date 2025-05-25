import asyncio
import aiosqlite


async def async_fetch_users(db_path):
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All users:")
            for row in results:
                print(row)
            return results


async def async_fetch_older_users(db_path):
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in results:
                print(row)
            return results


async def fetch_concurrently():
    db_path = "example.db"
    # Create test database if it doesn't exist
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            email TEXT
        )
        """
        )
        # Check if table is empty
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            count = await cursor.fetchone()
            if count[0] == 0:
                # Insert test data
                users = [
                    ("Alice", 35, "alice@example.com"),
                    ("Bob", 42, "bob@example.com"),
                    ("Charlie", 28, "charlie@example.com"),
                    ("Diana", 45, "diana@example.com"),
                    ("Eve", 39, "eve@example.com"),
                ]
                await db.executemany(
                    "INSERT INTO users (name, age, email) VALUES (?, ?, ?)", users
                )
                await db.commit()

    # Run both queries concurrently
    results = await asyncio.gather(
        async_fetch_users(db_path), async_fetch_older_users(db_path)
    )
    return results


if __name__ == "__main__":
    # Run the concurrent fetch
    asyncio.run(fetch_concurrently())
