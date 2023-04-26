from aiogram import Bot

from dto import Message
from publishers.base import BasePublisher


class TelegramPublisher(BasePublisher):
    def __init__(self, token: str):
        self.bot = Bot(token=token)

    async def send(self, chat_id: str, msg: Message) -> None:
        await self.bot.send_message(chat_id=chat_id, text=msg.text)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        session = await self.bot.get_session()
        await session.close()
