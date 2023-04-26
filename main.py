import asyncio
from asyncio import Queue

import config
from observers import TelegramObserver
from publishers import TelegramPublisher


async def run_observers(queue: Queue):
    await TelegramObserver(queue, config.TELEGRAM_ADMIN_SESSION_PATH, config.TELEGRAM_API_ID, config.TELEGRAM_API_HASH). \
        run('tefsdafasdf')


async def read_queue(queue: Queue):
    while True:
        msg = await queue.get()
        print(msg)
        # Цикл: сам реагирует на своё сообщение
        async with TelegramPublisher(config.TELEGRAM_BOT_TOKEN) as tg_publisher:
            await tg_publisher.send('@tefsdafasdf', msg)


async def run_publishers():
    async with TelegramPublisher(config.TELEGRAM_BOT_TOKEN) as tg_publisher:
        await tg_publisher.send('@tefsdafasdf', 'test')


async def main():
    queue = Queue()

    await asyncio.gather(
        run_observers(queue),
        read_queue(queue)
    )

asyncio.run(main())

