import asyncio
from config import TELEGRAM_BOT_TOKEN
from publishers import TelegramPublisher


async def main():
    async with TelegramPublisher(TELEGRAM_BOT_TOKEN) as tg_publisher:
        await tg_publisher.send('@tefsdafasdf', 'test')

asyncio.run(main())
