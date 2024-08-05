import aio_pika

RABBITMQ_URL = "amqp://guest:guest@rabbitmq/"


async def send_message(message: str):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("test_queue", durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=queue.name,
        )