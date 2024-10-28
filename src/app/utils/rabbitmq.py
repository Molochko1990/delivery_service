import json

import aio_pika


async def send_message_to_queue(message: dict, queue_name: str = "task_queue"):
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    try:
        channel = await connection.channel()
        await channel.declare_queue(queue_name, durable=True)
        serialized_message = json.dumps(message)
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=serialized_message.encode('utf-8'),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=queue_name
        )
    finally:
        await connection.close()