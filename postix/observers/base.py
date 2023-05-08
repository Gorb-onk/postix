from abc import abstractmethod, ABC
from asyncio import Queue


class BaseObserver(ABC):
    def __init__(self, messages_queue: Queue):
        self.queue = messages_queue

    @abstractmethod
    async def run(self, chat_id: str) -> None:
        pass

    async def put_message_to_queue(self, message: str) -> None:
        await self.queue.put(message)
