from io import BytesIO

from aiogram import Bot
from aiogram.types import InputMediaPhoto, InputFile

from postix.dto import Message
from postix.publishers.base import BasePublisher


class TelegramPublisher(BasePublisher):
    def __init__(self, token: str):
        self.bot = Bot(token=token)

    async def send(self, chat_id: str, msg: Message) -> None:
        if len(msg.photos) > 1:
            media = [InputMediaPhoto(media=InputFile(BytesIO(photo))) for photo in msg.photos]
            media[0].caption = msg.text
            await self.bot.send_media_group(chat_id=chat_id, media=media)
        elif len(msg.photos) == 1:
            await self.bot.send_photo(chat_id=chat_id, photo=msg.photos[0], caption=msg.text)
        else:
            await self.bot.send_message(chat_id=chat_id, text=msg.text)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        session = await self.bot.get_session()
        await session.close()
