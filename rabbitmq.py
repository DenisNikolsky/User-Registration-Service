import aio_pika
import json
from aio_pika import ExchangeType
import os

RABBIT_URL = os.getenv("RABBIT_URL", "amqp://guest:guest@localhost:5672/")

async def publish_new_user(username: str):
    connection = await aio_pika.connect_robust(RABBIT_URL)

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("user_event", durable=True)

        message_body = ({
            "event": "user_registered",
            "username": username
        }).encode()

        message = aio_pika.Message(
            body=message_body,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT)

        await channel.default_exchange.publish(message, routing_key=queue.name)

        print(f"Sent user register event for {username}")
