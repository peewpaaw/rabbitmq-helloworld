import asyncio

import aio_pika

RABBITMQ_URL = "amqp://guest:guest@rabbitmq/"


async def process_data(data: str) -> str:
    # Simulate data processing
    await asyncio.sleep(2)
    return f"Processed: {data}"


async def consume_messages():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("processing_queue", durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = message.body.decode()
                    result = await process_data(data)
                    print("Received message:", message.body.decode())
                    await send_response(result, message.correlation_id)


async def send_response(result: str, correlation_id: str):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=result.encode(), correlation_id=correlation_id),
            routing_key="response_queue",
        )