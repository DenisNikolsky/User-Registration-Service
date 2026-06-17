import asyncio
import json
import aio_pika
import os

RABBIT_URL = os.getenv("RABBIT_URL", "amqp://guest:guest@localhost:5672/")

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        body = json.loads(message.body)
        event = body.get("event")
        username = body.get("username")
        if event == "user_registered":
            print(f"Sending welcome to {username}...")
            await asyncio.sleep(1)
            print(f"Done for {username}")

async def main():
    connection = await aio_pika.connect_robust(RABBIT_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("user_events", durable=True)
        print("Worker started, waiting for messages...")
        await queue.consume(process_message)
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutdown")