import asyncio
import aiosqlite


async def async_fetch_users():
    db_path = "users.db"
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All users:")
            for row in results:
                print(row)
            return results


async def async_fetch_older_users():
    db_path = "users.db"
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in results:
                print(row)
            return results


async def fetch_concurrently():
    # Run both queries concurrently
    results = await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    return results


asyncio.run(fetch_concurrently())
