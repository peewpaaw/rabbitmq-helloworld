import aio_pika

RABBITMQ_URL = "amqp://guest:guest@rabbitmq/"


async def consume_messages():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("test_queue", durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print("Received message:", message.body.decode())