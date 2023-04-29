from asyncio import Queue

from telethon import TelegramClient, events

from observers.base import BaseObserver
from dto import Message


class TelegramObserver(BaseObserver):
    def __init__(self, messages_queue: Queue, session: str, api_id: int, api_hash: str):
        super().__init__(messages_queue)
        self.client = TelegramClient(session, api_id, api_hash)

    async def run(self, chat_ids: list[str | int]) -> None:
        self.client.on(events.NewMessage(chats=chat_ids, incoming=True))(self.process_message)
        await self.client.start()
        await self.client.run_until_disconnected()

    async def process_message(self, event: events.NewMessage) -> None:
        file = await self.client.download_media(event.message, file=bytes)
        a = await self.client.download_media(event.message, file='./media/')
        print(a, print(event.message.id))
        msg = Message(text=event.message.text, photo=file)
        await self.put_message_to_queue(msg)

    async def put_message_to_queue(self, message: Message) -> None:
        await self.queue.put(message)
