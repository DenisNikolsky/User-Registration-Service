import bcrypt
from fastapi import HTTPException
import aiosqlite
from limits import UserResponse
from cache import get_user_from_cache, delete_user_from_cache, set_user_to_cache
from rabbitmq import publish_new_user
import asyncio

async def create_db():
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS users
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            age INTEGER,
            password TEXT NOT NULL
            )
            '''
        )
        await db.commit()

async def create_new_user(user_data):
    try:
        secret_pass = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        async with aiosqlite.connect("users.db") as db:
            await db.execute(
                "INSERT INTO users (name, age, password) VALUES (?, ?, ?)", (user_data.name, user_data.age, secret_pass)
            )
            await db.commit()
            await delete_user_from_cache(user_data.name)

            asyncio.create_task(publish_new_user(user_data.name))

            return {"message": f"User {user_data.name} created successfully"}
    except aiosqlite.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists!")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error occured in creating user: {e}")


async def find_user(user_name) -> UserResponse:
    cache = await get_user_from_cache(user_name)
    if cache:
        return UserResponse(name=cache["name"], age=cache["age"])

    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT name, age FROM users WHERE name = ?", (user_name,)) as cursor:
            user = await cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail=f"User {user} does not exist!")

    user_data = {"name": user[0], "age": user[1]}

    await set_user_to_cache(user_name, user_data, ttl=60)

    return UserResponse(name=user[0], age=user[1])

async def show_all_persons():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT name, age FROM users") as cursor:
            rows = await cursor.fetchall()

        if not rows:
            return []
        return [UserResponse(name=row[0], age=row[1]) for row in rows]
