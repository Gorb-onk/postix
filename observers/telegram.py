from asyncio import Queue

from telethon import TelegramClient, events

from observers.base import BaseObserver


class TelegramObserver(BaseObserver):
    def __init__(self, messages_queue: Queue, session: str, api_id: int, api_hash: str):
        super().__init__(messages_queue)
        self.client = TelegramClient(session, api_id, api_hash)

    async def run(self, chat_id: str) -> None:
        self.client.on(events.NewMessage(chats=chat_id, incoming=True))(self.process_message)
        await self.client.start()
        await self.client.run_until_disconnected()

    async def process_message(self, event: events.NewMessage) -> None:
        await self.put_message_to_queue(event.raw_text)

    async def put_message_to_queue(self, message: str) -> None:
        await self.queue.put(message)
