import asyncio
import json
import os

import aio_pika
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.db.postge_session import get_db
from src.app.repositories.parcel_repository import ParcelRepository
from src.app.schemas.parcel import ParcelCreate
from src.app.services.currency_service import get_usd_exchange_rate
from src.app.utils.logging_config import logger


async def process_message(message: aio_pika.IncomingMessage):
    logger.info(f"Using database URL: {os.getenv('DATABASE_URL')}")

    async with message.process():
        parcel_data = json.loads(message.body)
        delivery_cost = (parcel_data['weight'] * 0.5 + parcel_data['content_cost'] * 0.01) * get_usd_exchange_rate()
        async for session in get_db():

            parcel_repo = ParcelRepository()
            parcel = ParcelCreate(**parcel_data)
            await parcel_repo.create_parcel(parcel, delivery_cost, parcel_data['session_id'], parcel_data['parcel_id'], session)
        logger.info("Processed message: {%s}", parcel_data)

async def main():
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    queue_name = "task_queue"

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=True)
        await queue.consume(process_message, no_ack=False)

        logger.info(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
