import asyncio
from asyncio import Queue

from telethon import TelegramClient, events

from observers.base import BaseObserver
from dto import Message


class TelegramObserver(BaseObserver):
    albums = {}

    def __init__(self, messages_queue: Queue, session: str, api_id: int, api_hash: str):
        super().__init__(messages_queue)
        self.client = TelegramClient(session, api_id, api_hash)

    async def run(self, chat_ids: list[str | int]) -> None:
        self.client.on(events.NewMessage(chats=chat_ids, incoming=True))(self.process_message)
        await self.client.start()
        await self.client.run_until_disconnected()

    async def process_message(self, event: events.NewMessage) -> None:
        photo = await self.client.download_media(event.message, file=bytes)
        if event.grouped_id:
            pair = (event.chat_id, event.grouped_id)
            if pair in self.albums:
                self.albums[pair].append(photo)
                return
            self.albums[pair] = [photo]
            await asyncio.sleep(2)
            photos = self.albums.pop(pair)
        else:
            photos = [photo]
        msg = Message(text=event.message.text, photos=photos)

        await self.put_message_to_queue(msg)

    async def put_message_to_queue(self, message: Message) -> None:
        await self.queue.put(message)
