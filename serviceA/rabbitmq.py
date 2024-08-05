import aio_pika

RABBITMQ_URL = "amqp://guest:guest@rabbitmq/"


async def send_message(message: str, correlation_id: str):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        #queue = await channel.declare_queue("processing_queue", durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode(), correlation_id=correlation_id),
            routing_key="processing_queue",
        )


async def receive_response(correlation_id: str):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("response_queue", durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    if message.correlation_id == correlation_id:

                        print(message.body.decode())
                        break
                    #print(message.body.decode())
                    #if message.correlation_id == correlation_id:
                    #    responses[correlation_id].set_result({"result": message.body.decode()})
                    #    break