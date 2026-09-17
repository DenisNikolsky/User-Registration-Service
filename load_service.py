import asyncio
import httpx
import random
from faker import Faker
from itertools import product
import string
import secrets
from random import randint

alphabet = string.ascii_letters + string.digits
fake = Faker()
client = httpx.Client()

async def send_request(client):
    username = fake.user_name()
    password = "".join(secrets.choice(alphabet) for i in range(8))
    response = await client.post(
        "http://127.0.0.1:8000/users/",
        data={"name": username,
              "age": randint(19, 45),
        "password": password},
    )

    return {"status": response.status_code}

async def generate_load(count: int):
    async with httpx.AsyncClient() as client:
        tasks = []
        for i in range(count):
            tasks.append(send_request(client))

        await asyncio.gather(*tasks)

