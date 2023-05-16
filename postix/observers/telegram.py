import asyncio
from asyncio import Queue

from aiocache import BaseCache
from telethon import TelegramClient, events

from postix.observers.base import BaseObserver
from postix.dto import Message


class TelegramObserver(BaseObserver):
    def __init__(self, messages_queue: Queue, session: str, api_id: int, api_hash: str, cache: BaseCache):
        super().__init__(messages_queue)
        self.client = TelegramClient(session, api_id, api_hash)
        self.cache = cache

    async def run(self, chat_ids: list[str | int]) -> None:
        self.client.on(events.NewMessage(chats=chat_ids, incoming=True))(self.process_message)
        await self.client.start()
        await self.client.run_until_disconnected()

    async def process_message(self, event: events.NewMessage) -> None:
        photo = await self.client.download_media(event.message, file=bytes)
        if event.grouped_id:
            album_uid = f'{event.chat_id}-{event.grouped_id}'
            cache_value = await self.cache.get(album_uid, default=[])
            await self.cache.set(album_uid, cache_value + [photo])
            if cache_value:
                return

            await asyncio.sleep(2)

            photos = await self.cache.get(album_uid)
            await self.cache.delete(album_uid)
        elif photo:
            photos = [photo]
        else:
            photos = []
        msg = Message(text=event.message.text, photos=photos)

        await self.put_message_to_queue(msg)

    async def put_message_to_queue(self, message: Message) -> None:
        await self.queue.put(message)
