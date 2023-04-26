import asyncio
from asyncio import Queue

import config
from observers import TelegramObserver
from publishers import TelegramPublisher
from message_processor import MessageProcessor


async def run_observers(queue: Queue, channels: list[str | int]) -> None:
    await TelegramObserver(queue, config.TELEGRAM_ADMIN_SESSION_PATH, config.TELEGRAM_API_ID, config.TELEGRAM_API_HASH). \
        run(channels)


async def process_queue(queue: Queue, processor: MessageProcessor):
    while True:
        msg = await queue.get()
        await processor.process(msg)


async def main():
    source_channels = [1757653513]
    target_channels = ['@tefsdafasdf']

    queue = Queue()
    publisher = TelegramPublisher(config.TELEGRAM_BOT_TOKEN)
    message_processor = MessageProcessor(publisher, target_channels)
    await asyncio.gather(
        run_observers(queue, source_channels),
        process_queue(queue, message_processor)
    )

asyncio.run(main())

